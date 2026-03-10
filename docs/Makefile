PACKAGE = ../scadpy
COVERAGE = coverage
GENBADGE = genbadge
INTERROGATE = interrogate
BADGES_DIR = _static/badges
SPHINXOPTS ?=
SPHINXBUILD ?= sphinx-build
SPHINXAUTOGEN ?= sphinx-autogen
SOURCEDIR = .
BUILDDIR = build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile snapshots

# Build the documentation
html:
	@$(SPHINXAUTOGEN) -o $(SOURCEDIR)/_autosummary $(SOURCEDIR)/index.rst
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Run doctests only
doctest:
	@$(SPHINXBUILD) -b doctest "$(SOURCEDIR)" "$(BUILDDIR)/doctest" $(SPHINXOPTS)
	@rm -rf $(BUILDDIR)/doctrees

snapshots:
	@SCADPY_UPDATE_SNAPSHOTS=1 $(SPHINXBUILD) -b doctest "$(SOURCEDIR)" "$(BUILDDIR)/doctest" $(SPHINXOPTS)
	@rm -rf $(BUILDDIR)/doctrees
	@SCADPY_UPDATE_SNAPSHOTS=1 $(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

coverage:
	@$(COVERAGE) run --branch \
		-m sphinx -b doctest \
		"$(SOURCEDIR)" "$(BUILDDIR)/doctest"
	@$(COVERAGE) report --include="$(PACKAGE)/*" -m
	@$(COVERAGE) html --include="$(PACKAGE)/*"
	@$(COVERAGE) xml --include="$(PACKAGE)/*" -o $(BUILDDIR)/coverage.xml
	@mkdir -p $(BADGES_DIR)
	@$(GENBADGE) coverage -i $(BUILDDIR)/coverage.xml -o $(BADGES_DIR)/coverage.svg -s

interrogate:
	@mkdir -p $(BADGES_DIR)
	@$(INTERROGATE) $(PACKAGE) \
		--ignore-module \
		--generate-badge $(BADGES_DIR)/interrogate.svg \
		--fail-under 0 \
		-vv
