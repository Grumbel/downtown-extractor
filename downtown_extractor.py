#!/usr/bin/env python

# Downtown Extractor
# Copyright (C) 2011 Ingo Ruhnke <grumbel@gmx.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import os
import sys
from optparse import OptionParser

parser = OptionParser("Usage: %prog [OPTIONS] [FILES]")
parser.add_option("-d", "--datadir", dest="datadir",
                  help="The directory of Goin' Downtown", metavar="DIR")
parser.add_option("-t", "--targetdir", dest="targetdir", default=".",
                  help="The directory where files will be extracted", metavar="DIR")
parser.add_option("-a", "--extract-all", metavar="DIR",
                  dest="extract_all", action="store_true",
                  help="Extract all resource files")
parser.add_option("-s", "--stdout",
                  dest="stdout", action="store_true",
                  help="Extract data to stdout")
parser.add_option("-g", "--glob", metavar="PATTERN",
                  dest="glob_pattern",
                  help="Select files by glob pattern")
parser.add_option("-l", "--list",
                  dest="list_files", action="store_true",
                  help="List all resource files")
parser.add_option("-e", "--extract",
                  dest="extract_files", action="store_true",
                  help="Extract resource files")
parser.add_option("-r", "--resources",
                  dest="resources", default="resources",
                  help="Prefix of the resource files, can be 'resources' or 'german'")

(options, args) = parser.parse_args()

if not options.datadir:
    print("error: datadir not given")
    sys.exit(1)

sql = sqlite3.connect(os.path.join(options.datadir, options.resources + '.meta'))
cur = sql.cursor()

if options.list_files:
    cur.execute("select resource_id from file_information;")
    for (resource_id,) in cur:
        print(resource_id)
else:
    if not options.glob_pattern and not options.extract_all and args == []:
        print("error: no files for extraction given")
        sys.exit(1)

    else:
        entries = []

        # collect entries to extract
        if options.extract_all:
            cur.execute("select"
                        "  resource_id, file_index, file_size, file_begin"
                        "  from file_information;")
            entries = cur.fetchall()

        if options.glob_pattern:
            cur.execute("select "
                        "  resource_id, file_index, file_size, file_begin"
                        "  from file_information where resource_id glob ?;", (options.glob_pattern,))
            entries = cur.fetchall()

        for resource_id in args:
            cur.execute("select "
                        "  resource_id, file_index, file_size, file_begin"
                        "  from file_information where resource_id = ?;", (resource_id,))
            entries += cur.fetchall()

        # extract collected entries
        for resource_id, file_index, file_size, file_begin in entries:
            datafile = os.path.join(options.datadir, "%s.d%03d" % (options.resources, file_index))
            with open(datafile, "rb") as fin:
                fin.seek(file_begin)
                data = fin.read(file_size)

                # write the data to the target directory
                if options.stdout:
                    sys.stdout.buffer.write(data)
                else:
                    outfile = os.path.join(options.targetdir, resource_id)
                    outdir = os.path.dirname(outfile)
                    print("extracting \"%s\"" % outfile)
                    if not os.path.exists(outdir):
                        os.makedirs(outdir)
                    with open(outfile, "wb") as fout:
                        fout.write(data)

# EOF #
