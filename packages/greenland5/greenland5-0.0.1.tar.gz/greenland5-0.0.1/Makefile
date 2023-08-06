# *  greenland5 -- A Pythonic Eco System                                       |
# *  Copyright (C) 2020  M E Leypold  -----------------------------------------|
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


all::

IN-ROOT-PROJECT := \
  $(shell if test -f ../pyproject.toml && test -f ../Maintainer.mk; \
             then echo true; \
             else echo false; fi \
   )

ifeq ($(IN-ROOT-PROJECT),true)
include ../Maintainer.mk
# Note: This pulls in additional targets that are only useful when developing Greenland5 as a whole.
endif

check_release: check check_git check_build

check_git:
	# Criteria before you can set a release
	test $$( git status -s | wc -l ) -eq 0                       # everything checked in 
	git describe --all | grep '^tags/\([0-9]\+[.]\)\+[0-9]\+$$'  # version tag set on recent version

check_build::
	# All the following build methods must work
        # AFAIK the PEP 518 builder is the most critical
	pip wheel --use-feature=in-tree-build --no-deps .            # Can build via PIP
	python setup.py sdist                                        # Can build source dist via setuptools
	python setup.py bdist_wheel                                  # Can build a wheel via setuptools
	twine check $$(ls -1t dist/*.whl | head -1)                  # Twine likes the resulting wheels
	twine check $$(ls -1t dist/*.tar.gz | head -1)               # Twine likes the resulting source dist
	python setup.py bdist                                        # Can build binary dist via setuptools
	twine check $$(ls -1t dist/*.tar.gz | head -1)               # Twine likes the resulting binary dist
	python -m build                                              # Can build with PEP 518 builder
	twine check $$(ls -1t dist/*.whl | head -1)                  # Twine likes the resulting wheels
	twine check $$(ls -1t dist/*.tar.gz | head -1)               # Twine likes the resulting source dist

check::


clean::
	find . -name '*~' | xargs rm -rf
