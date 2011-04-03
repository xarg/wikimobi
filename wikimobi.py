#!/usr/bin/env python

__doc__ = """
Usage:

python wikiepub.py path_to_abstract.xml path_to_output.tab

Abstract file(s) can be found at: 

http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml

Warning: Last time I checked it was 3GB uncompressed

More info here: 

    http://en.wikipedia.org/wiki/Wikipedia:Database_download

"""
import subprocess
import sys
from lxml import etree

def main():
    """ This will write a tab separated <header>\t<definition> file that will
    be passed to mobigen and will result in a .mobi file containing the
    dictionary.
    
    """
    input_filename, output_filename = sys.argv[1:3]
    if len(sys.argv) != 3:
        print __doc__
        sys.exit(1)
    
    with open(input_filename, 'rb') as xml_file:
        with open(output_filename, 'wb+') as out_file:
            tree = etree.parse(xml_file)
            for doc in tree.iterfind('doc'):
                header = doc.find('title').text.replace('Wikipedia: ', '', 1)
                definition = doc.find('abstract').text.replace("\t", ' ')
                out_file.write(u"%s\t%s\n" % (header, definition))
    
if __name__ == '__main__':
    main()
