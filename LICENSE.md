# MIT License

Copyright (c) 2026 m-fabregue

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Third-party dependencies

ScadPy depends on the following third-party libraries, each distributed under
their own terms:

| Package | License |
|---------|---------|
| [trimesh](https://github.com/mikedh/trimesh) | MIT |
| [Shapely](https://github.com/shapely/shapely) | BSD 3-Clause |
| [typeguard](https://github.com/agronholm/typeguard) | MIT |
| [IPython](https://github.com/ipython/ipython) | BSD 3-Clause |
| [PySide6](https://doc.qt.io/qtforpython) | LGPL v3 |
| [triangle](https://github.com/drufat/triangle) | See note below |

**Note on `triangle`:** The `triangle` package wraps Jonathan Shewchuk's
Triangle library, which restricts commercial use without written permission
from the author. Users intending commercial applications should review
[Triangle's license](https://www.cs.cmu.edu/~quake/triangle.html) and
consider replacing the `triangle` dependency accordingly.
