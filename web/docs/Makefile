#!gmake
#
# ***** BEGIN LICENSE BLOCK *****
# Version: Apache License 2.0
#
# Copyright (c) 2011-2015 MathJax Consortium, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contributor(s):
#   Frederic Wang <fred.wang@free.fr> (original author)
#
# ***** END LICENSE BLOCK *****

include ../../custom.cfg

all: doxygen html

doxygen:
	rm -rf doxygen/
	$(DOXYGEN) doxygen.cfg

html:
	rm -rf html/
	mkdir html
	$(DOT) -Tsvg source/testing-framework.dot > source/testing-framework.svg
	$(DOT) -Tsvg source/testing-framework-basic.dot > source/testing-framework-basic.svg
	$(SPHINXBUILD) -b html source html

.PHONY: doxygen html
