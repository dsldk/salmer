# Copyright (C) 2017-20 Dansk Sprog- og Litteraturselskab and Magenta ApS.
#
# This file is part of DSL's generic literature site template.
#
# This template website is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README")).read()
CHANGES = open(os.path.join(here, "..", "NEWS")).read()

requires = [
    "pyramid_chameleon",
    "pyramid",
    "pyramid_debugtoolbar",
    "waitress",
    "WebTest",
    "nose",
    "requests",
    "python-dateutil",
    "PageCalc==0.2.0",
    "urllib3",
    "django_python3_ldap",
    "python-memcached",
    "Babel==2.6.0",
    "lingua",
]

setup(
    name="generic_literature_site",
    version="0.1.0",
    description="generic_literature_site",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="",
    author_email="",
    url="",
    keywords="web pyramid pylons",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="generic_literature_site",
    entry_points="""\
      [paste.app_factory]
      main = generic_literature_site:main
      """,
)
