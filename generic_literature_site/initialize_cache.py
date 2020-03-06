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

import requests

BASE_URL = "http://localhost:6543/register"

register_types = "personer", "vaerker", "steder", "litteraere_figurer"

danish_letters = [chr(c) for c in range(ord("A"), ord("Z") + 1)] + [
    "Æ",
    "Ø",
    "Å",
]

for rt in register_types:
    for letter in danish_letters:
        register_url = "{}/{}/{}".format(BASE_URL, rt, letter)
        result = requests.get(register_url)
        if not result:
            print(
                "Register {} failed, letter {}: {}".format(
                    rt, letter, str(result)
                )
            )
