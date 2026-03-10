from __future__ import annotations

import json
import uuid

from typing import TYPE_CHECKING

from IPython.core.display import HTML
from typeguard import typechecked

from scadpy.color.constants import BLACK, WHITE

if TYPE_CHECKING:
    from scadpy import Color, Solid


_TEMPLATE = """\
<div id="{viewer_id}" style="width:100%;aspect-ratio:1/1;"></div>
<script>
(function () {{
  // --- Global deduped Three.js loader (shared across all viewers on the page) ---
  if (!window.__scadpy_loader) {{
    var _scripts = [
      'https://cdn.jsdelivr.net/npm/three@0.128/build/three.min.js',
      'https://cdn.jsdelivr.net/npm/three@0.128/examples/js/controls/OrbitControls.js',
      'https://cdn.jsdelivr.net/npm/three@0.128/examples/js/lines/LineSegmentsGeometry.js',
      'https://cdn.jsdelivr.net/npm/three@0.128/examples/js/lines/LineMaterial.js',
      'https://cdn.jsdelivr.net/npm/three@0.128/examples/js/lines/LineSegments2.js',
    ];
    var _ready = false, _queue = [], _idx = 0;
    function _next() {{
      if (_idx >= _scripts.length) {{
        _ready = true;
        _queue.forEach(function(f) {{ f(); }});
        _queue = [];
        return;
      }}
      var src = _scripts[_idx++];
      if (document.querySelector('script[src="' + src + '"]')) {{ _next(); return; }}
      var s = document.createElement('script');
      s.src = src; s.onload = _next;
      document.head.appendChild(s);
    }}
    _next();
    window.__scadpy_loader = {{
      onReady: function(f) {{ _ready ? f() : _queue.push(f); }}
    }};
  }}

  // --- Per-viewer state ---
  var container = document.getElementById('{viewer_id}');
  var renderer = null, animId = null, _controls = null, _scene = null, _camera = null;
  var fg = '{foreground_color}';
  var bg = '{background_color}';
  var parts = {parts_json};

  function startAnim() {{
    if (!renderer || animId) return;
    (function animate() {{
      animId = requestAnimationFrame(animate);
      _controls.update();
      renderer.render(_scene, _camera);
    }})();
  }}

  function stopAnim() {{
    if (animId) {{ cancelAnimationFrame(animId); animId = null; }}
  }}

  function build() {{
    if (renderer) {{ startAnim(); return; }}
    _scene = new THREE.Scene();
    _scene.background = new THREE.Color(bg);

    var w = container.clientWidth || 400;
    _camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.001, 100000);
    renderer = new THREE.WebGLRenderer({{antialias: true}});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(w, w);
    container.appendChild(renderer.domElement);

    _controls = new THREE.OrbitControls(_camera, renderer.domElement);
    _controls.enableDamping = true;

    var edgeColor;
    _scene.add(new THREE.AmbientLight(0xffffff, 0.45));
    var key = new THREE.DirectionalLight(0xffffff, 0.75);
    key.position.set(2, 3, 4); _scene.add(key);
    var fill = new THREE.DirectionalLight(0xffffff, 0.3);
    fill.position.set(-3, 1, -2); _scene.add(fill);
    var bottom = new THREE.DirectionalLight(0xffffff, 0.15);
    bottom.position.set(0, -1, 0); _scene.add(bottom);

    for (var i = 0; i < parts.length; i++) {{
      var part = parts[i];
      var geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(part.vertices, 3));
      geo.setIndex(part.faces);
      geo.computeVertexNormals();
      var transparent = part.opacity < 1.0;
      edgeColor = new THREE.Color(part.color).lerp(new THREE.Color(bg), 0.5);
      var mat = new THREE.MeshPhongMaterial({{
        color: part.color,
        opacity: part.opacity,
        transparent: transparent,
        depthWrite: !transparent,
        side: THREE.FrontSide,
        polygonOffset: true,
        polygonOffsetFactor: 1,
        polygonOffsetUnits: 1,
        shininess: 40,
        specular: new THREE.Color(0x222222),
        flatShading: true,
      }});
      _scene.add(new THREE.Mesh(geo, mat));
      var edgesGeo = new THREE.EdgesGeometry(geo, 20);
      var lineGeo = new THREE.LineSegmentsGeometry();
      lineGeo.setPositions(edgesGeo.attributes.position.array);
      var lineMat = new THREE.LineMaterial({{
        color: edgeColor,
        linewidth: 2,
        resolution: new THREE.Vector2(w, w),
        transparent: true,
        opacity: transparent ? part.opacity * 0.5 : 1.0,
      }});
      _scene.add(new THREE.LineSegments2(lineGeo, lineMat));
      var outlineVS = [
        'uniform vec2 resolution;',
        'uniform float outlineWidth;',
        'void main() {{',
        '  vec4 pos = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
        '  vec4 posN = projectionMatrix * modelViewMatrix * vec4(position + normal, 1.0);',
        '  vec2 dir = normalize(posN.xy / posN.w - pos.xy / pos.w);',
        '  pos.xy += dir * outlineWidth / (resolution * 0.5);',
        '  gl_Position = pos;',
        '}}'
      ].join('\\n');
      var outlineFS = [
        'uniform vec3 outlineColor;',
        'void main() {{',
        '  gl_FragColor = vec4(outlineColor, 1.0);',
        '}}'
      ].join('\\n');
      var outlineMat = new THREE.ShaderMaterial({{
        uniforms: {{
          outlineColor: {{ value: edgeColor }},
          resolution: {{ value: new THREE.Vector2(w, w) }},
          outlineWidth: {{ value: 2.0 }},
        }},
        vertexShader: outlineVS,
        fragmentShader: outlineFS,
        side: THREE.BackSide,
      }});
      var outlineMesh = new THREE.Mesh(geo, outlineMat);
      outlineMesh.renderOrder = -1;
      _scene.add(outlineMesh);
    }}

    var box = new THREE.Box3().setFromObject(_scene);
    var center = box.getCenter(new THREE.Vector3());
    var size = box.getSize(new THREE.Vector3());
    var dist = Math.max(size.x, size.y, size.z) * 1.2;
    _camera.position.copy(center).add(new THREE.Vector3(dist, dist, dist));
    _controls.target.copy(center);
    _controls.update();

    var maxDim = Math.max(size.x, size.y, size.z);
    var tgt = maxDim * 0.25 || 1;
    var mag = Math.pow(10, Math.floor(Math.log10(tgt)));
    var niceStep = [1, 2, 5, 10].reduce(function(p, c) {{
      return Math.abs(c * mag - tgt) < Math.abs(p * mag - tgt) ? c : p;
    }}) * mag;

    var cx = center.x, cy = center.y, cz = center.z;
    var halfGridXZ = Math.ceil(Math.max(size.x, size.z) / 2 / niceStep) * niceStep;
    var halfGridY  = Math.ceil(size.y / 2 / niceStep) * niceStep;
    var halfGrid = Math.max(halfGridXZ, halfGridY);
    var divs = Math.round(halfGrid * 2 / niceStep);
    var floorY = cy - halfGrid;

    var frustum = halfGrid * 1.6;
    _camera.left = -frustum; _camera.right = frustum;
    _camera.top = frustum; _camera.bottom = -frustum;
    _camera.near = dist * 0.01;
    _camera.far = (dist + halfGrid * 2) * 2;
    _camera.updateProjectionMatrix();

    function makeGrid(gSize, d, opacity) {{
      var g = new THREE.GridHelper(gSize, d, fg, fg);
      g.material.opacity = opacity;
      g.material.transparent = true;
      return g;
    }}

    function makeWall(opacity) {{
      var n = divs, h = halfGrid, pts = [];
      for (var i = 0; i <= n; i++) {{ var xv = -h + i * niceStep; pts.push(xv, 0, 0, xv, h * 2, 0); }}
      for (var j = 0; j <= n; j++) {{ var yv2 = j * niceStep; pts.push(-h, yv2, 0, h, yv2, 0); }}
      var g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
      return new THREE.LineSegments(g, new THREE.LineBasicMaterial({{color: fg, transparent: true, opacity: opacity}}));
    }}

    var floor = makeGrid(halfGrid * 2, divs, 0.25);
    floor.position.set(cx, floorY, cz); _scene.add(floor);
    var backWall = makeWall(0.1);
    backWall.position.set(cx, floorY, cz - halfGrid); _scene.add(backWall);
    var leftWall = makeWall(0.1);
    leftWall.rotation.y = -Math.PI / 2;
    leftWall.position.set(cx - halfGrid, floorY, cz); _scene.add(leftWall);

    function makeSprite(text) {{
      var canvas = document.createElement('canvas');
      var cw = Math.max(80, text.length * 26);
      canvas.width = cw; canvas.height = 64;
      var ctx = canvas.getContext('2d');
      ctx.font = 'bold 38px sans-serif';
      ctx.fillStyle = fg; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(text, cw / 2, 32);
      var spr = new THREE.Sprite(new THREE.SpriteMaterial({{map: new THREE.CanvasTexture(canvas), transparent: true}}));
      var sh = halfGrid * 0.16;
      spr.scale.set(sh * cw / 64, sh, 1);
      return spr;
    }}

    var edgeOff = niceStep * 0.5, gy = floorY + niceStep * 0.15;
    var xS = Math.ceil((cx - halfGrid) / niceStep), xE = Math.floor((cx + halfGrid) / niceStep);
    for (var xi = xS; xi <= xE; xi++) {{
      var xv = xi * niceStep;
      var xs = makeSprite(parseFloat(xv.toPrecision(4)).toString());
      xs.position.set(xv, gy, cz - halfGrid - edgeOff); _scene.add(xs);
    }}
    var zS = Math.ceil((cz - halfGrid) / niceStep), zE = Math.floor((cz + halfGrid) / niceStep);
    for (var zi = zS; zi <= zE; zi++) {{
      var zv = zi * niceStep;
      var zs = makeSprite(parseFloat(zv.toPrecision(4)).toString());
      zs.position.set(cx - halfGrid - edgeOff, gy, zv); _scene.add(zs);
    }}
    var yS = Math.ceil((cy - halfGrid) / niceStep), yE = Math.floor((cy + halfGrid) / niceStep);
    for (var yi = yS; yi <= yE; yi++) {{
      var yv = yi * niceStep;
      var ys = makeSprite(parseFloat(yv.toPrecision(4)).toString());
      ys.position.set(cx - halfGrid - edgeOff, yv, cz - halfGrid); _scene.add(ys);
    }}

    var cornerX = cx - halfGrid, cornerY = floorY, cornerZ = cz - halfGrid;
    var origin = new THREE.Vector3(cornerX, cornerY, cornerZ);
    var axisLen = halfGrid * 2, arrowHead = axisLen * 0.08;
    _scene.add(new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), origin, axisLen, 0xff4444, arrowHead, arrowHead * 0.6));
    _scene.add(new THREE.ArrowHelper(new THREE.Vector3(0, 1, 0), origin, axisLen, 0x44ff44, arrowHead, arrowHead * 0.6));
    _scene.add(new THREE.ArrowHelper(new THREE.Vector3(0, 0, 1), origin, axisLen, 0x4444ff, arrowHead, arrowHead * 0.6));

    function makeAxisLabel(text, color) {{
      var canvas = document.createElement('canvas');
      canvas.width = 64; canvas.height = 64;
      var ctx = canvas.getContext('2d');
      ctx.font = 'bold 52px sans-serif';
      ctx.fillStyle = color; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(text, 32, 32);
      var spr = new THREE.Sprite(new THREE.SpriteMaterial({{map: new THREE.CanvasTexture(canvas)}}));
      var labelSize = axisLen * 0.1;
      spr.scale.set(labelSize, labelSize, 1);
      return spr;
    }}

    var lx = makeAxisLabel('X', '#ff4444'); lx.position.set(cornerX + axisLen * 1.06, cornerY, cornerZ); _scene.add(lx);
    var ly = makeAxisLabel('Y', '#44ff44'); ly.position.set(cornerX, cornerY + axisLen * 1.06, cornerZ); _scene.add(ly);
    var lz = makeAxisLabel('Z', '#4444ff'); lz.position.set(cornerX, cornerY, cornerZ + axisLen * 1.06); _scene.add(lz);

    requestAnimationFrame(function() {{
      renderer.render(_scene, _camera);
      startAnim();
    }});
  }}

  // Build on first visibility, pause/resume animation — canvas is never destroyed
  var observer = new IntersectionObserver(function(entries) {{
    if (entries[0].isIntersecting) {{ window.__scadpy_loader.onReady(build); }}
    else {{ stopAnim(); }}
  }}, {{ threshold: 0.01, rootMargin: '200px' }});
  observer.observe(container);
}})();
</script>
"""


@typechecked
def map_solid_to_html(
    solid: Solid,
    background_color: Color = WHITE,
    foreground_color: Color = BLACK,
) -> HTML:
    background_color_hex = "#{:02X}{:02X}{:02X}".format(
        *(int(x * 255) for x in background_color[:-1])
    )

    parts = []
    for part in solid._parts:
        mesh = part.geometry
        color = part.color
        parts.append({
            "vertices": mesh.vertices.ravel().tolist(),
            "faces": mesh.faces.ravel().tolist(),
            "color": "#{:02X}{:02X}{:02X}".format(
                int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
            ),
            "opacity": float(color[3]),
        })

    foreground_color_hex = "#{:02X}{:02X}{:02X}".format(
        *(int(x * 255) for x in foreground_color[:-1])
    )

    html = _TEMPLATE.format(
        viewer_id=f"scadpy-{uuid.uuid4().hex}",
        background_color=background_color_hex,
        foreground_color=foreground_color_hex,
        parts_json=json.dumps(parts),
    )
    return HTML(html)
