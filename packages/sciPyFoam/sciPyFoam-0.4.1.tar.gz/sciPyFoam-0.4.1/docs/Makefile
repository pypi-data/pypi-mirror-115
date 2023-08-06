# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	# remove all files before generating .rst files, because sometimes the python modules source file names would be changed
	rm -rf source/sciPyFoam/*
	# generate .rst files form python source code
	sphinx-apidoc -o source/sciPyFoam ../sciPyFoam -f
	sphinx-apidoc -o source/sciPyFoam/postProcessing ../sciPyFoam/postProcessing -f
	# build document
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
