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
#import subprocess
#import sys
#from copy import deepcopy
#from lxml import etree

from rdflib.Graph import Graph

def category_graph():
    graph = Graph("Sleepycat")
    graph.open("store", create=True)
    graph.parse("../skos_categories_en.nt", format="nt")

    # print out all the triples in the graph
    for subject, predicate, object in graph:
        import pdb; pdb.set_trace()
        #print subject, predicate, object

def main():
    """ This will write a tab separated <header>\t<definition> file that will
    be passed to mobigen and will result in a .mobi file containing the
    dictionary.

    """
    input_filename, output_filename = sys.argv[1:3]
    if len(sys.argv) != 3:
        print __doc__
        sys.exit(1)

    c = 0
    l = 10000
    output = ''

    with open(input_filename, 'rb') as xml_file:
        with open(output_filename, 'wb+') as out_file:
            for _, doc in etree.iterparse(xml_file, events=('end', ), tag='doc'):
                header_el = deepcopy(doc.find('title'))
                if header_el is None:
                    del header_el
                    continue
                header_text = deepcopy(header_el.text)
                del header_el
                header = deepcopy(header_text.replace('Wikipedia: ', '', 1).strip().encode('utf-8', 'ignore'))
                del header_text

                definition = deepcopy(doc.find('abstract'))
                if definition is None:
                    del definition
                    continue
                definition_text = deepcopy(definition.text)
                if definition_text is None:
                    del definition_text
                    continue

                definition = deepcopy(definition_text.replace("\t", ' ').strip().encode('utf-8', 'ignore'))
                output += "%s\t%s\n" % (header,  definition)
                if c == l:
                    out_file.write(output)
                    out_file.flush()
                    output = ''
                    c = 0
                else:
                    c += 1
                del header
                del definition

                # It's safe to call clear() here because no descendants will be accessed
                doc.clear()
                # Also eliminate now-empty references from the root node to <doc>
                while doc.getprevious() is not None:
                    del doc.getparent()[0]

if __name__ == '__main__':
    #main()
    category_graph()
