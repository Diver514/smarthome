#!/usr/bin/env python
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2012-2013 KNX-User-Forum e.V.       http://knx-user-forum.de/
#########################################################################
#  This file is part of SmartHome.py.   http://smarthome.sourceforge.net/
#
#  SmartHome.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHome.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHome.py. If not, see <http://www.gnu.org/licenses/>.
##########################################################################


import ConfigParser, io, sys

conf = ''
# read conf and skip header entries (no section)
with open(sys.argv[1], 'r') as cfg:
    found_section = False
    for l in cfg.readlines():
        if len(l.strip()) == 0: continue
            if l[0] != '[' and found_section == False:
                continue
            found_section = True
            conf += l

with open(sys.argv[2], 'w') as out:
    config = ConfigParser.ConfigParser()
    config.readfp(io.BytesIO(conf))
    for section in config.sections():
        try:
            name = config.get(section, 'name')
            typ = config.get(section, 'type')
        except ConfigParser.NoOptionError:
            continue
        if typ == 'DS1820':
            sensor = 'T' + config.get(section, 'resolution')
        elif typ == 'DS2438Hum' or typ == 'DS2438Datanab':
            sensor = 'H'
        else:
            continue

out.write('''
    [[{0}]]
    name = {0}
    type = {1}
    ow_addr = {2}
    ow_sensor = {3}
    '''.format(name, typ, section, sensor))
