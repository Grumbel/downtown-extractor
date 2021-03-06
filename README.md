Downtown Data Extractor
=======================

The Downtown Data Extractor allows the extraction of the data files
(music, sound, textures, etc) from the following games:

 * Goin' Downtown
 * Everlight

The data structure of these games is pretty straight forward:

 * resources.meta is an sqlite3 db that contains all file entries,
   along with offset, size and resource file index

 * resources.d{idx} are the files containing the data

 * music and sound are Ogg files

 * textures are DDS

 * animations file format is from Granny Animation

 * there is a bunch of Python code and some Swig bindings

 * voice files are in a separate set of resource files having the
   prefix "german"


Usage
-----

To display available file entries:

    $ downtown_extractor.py -d "/win/Program Files/The Games Company/Downtown/" --list

To extract a single file entry:

    $ downtown_extractor.py -d "/win/Program Files/The Games Company/Downtown/" --extract \
        sound/music/dramatic.ogg

To extract a multiple entries by glob pattern:

    $ downtown_extractor.py -d "/win/Program Files/The Games Company/Downtown/" --extract \
        -g "sound/music/*.ogg"

To extract all data files:

    $ downtown_extractor.py -d "/win/Program Files/The Games Company/Downtown/" --extract \
        -g "sound/music/*.ogg"

Target directory where the datafiles will be written can be given with `--targetdir`

Voice files are in a separate set of resource files, use: `--resources german` to access them.
