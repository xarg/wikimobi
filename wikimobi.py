#!/usr/bin/env python

__doc__ = """
Create mobi files from wikipedia categories
===========================================

Usage:

python wikimobi.py [/nt_files_directory/] [/output_filename/] [Wikipedia Category] [levels (default:3)]

Required .nt file(s) can be found at:

#Contains short abstracts of the articles (first paragraph)

    http://downloads.dbpedia.org/3.6/en/short_abstracts_en.nt.bz2 (300mb)

#Contains relations between articles and categories

    http://downloads.dbpedia.org/3.6/en/article_categories_en.nt.bz2 (115mb)

#Contains relations between categories and subcategories in a skos type relation

    http://downloads.dbpedia.org/3.6/en/skos_categories_en.nt.bz2 (18mb)


More info here:

    http://wiki.dbpedia.org/Downloads36

"""
import re
import tempfile
import subprocess
import sys
import os
import logging

logger = logging.getLogger("wikimobi")

cat_pattern = re.compile("Category:([^>]+)")
title_pattern = re.compile("resource/([^>]+)")

class WikiMobi(object):

    def __init__(self, nt_dir, levels):
        """ """
        self.nt_dir = nt_dir
        self.levels = levels

    def get_child_categories(category, levels):
        """Given a root `category` get all it's child categories up until
        `levels` are reached. Levels as in depth of the `graph`

        """
        root_category = '<http://dbpedia.org/resource/Category:%s>' % category
        categories1 = set()
        categories2 = set()
        categories3 = set()
        categories4 = set()
        relations = {}
        parents = set()

        with open('../skos_categories_en.nt', 'rb') as fin:
            for line in fin:
                (category, rel, parent) = line.split(" ")[:3]
                if rel == '<http://www.w3.org/2004/02/skos/core#broader>':
                    if parent not in relations:
                        relations[parent] = set()
                    relations[parent].add(category)

        categories1 = relations[root_category]
        for c in categories1:
            if c in relations:
                categories2 |= relations[c]
        for c in categories2:
            if c in relations:
                categories3 |= relations[c]
        for c in categories3:
            if c in relations:
                categories4 |= relations[c]

        categories = set([root_category]) | categories1 | categories2 | categories3 #| categories4
        return categories

    def get_articles(self, category):

        articles = set()

        with open(".nt", 'rb') as fin:
            for line in fin:
                (subject, predicate, literal) = line.split(" ")[:3]
                if literal in categories:
                    articles.add(subject)

    def write_abstracts(self, tmpfile):
        with open("../short_abstracts_en.nt", 'rb') as fin:
            with open('../out.tab', 'wb+') as out_file:
                for line in fin:
                    (subject, predicate, literal) = line.split(" ", 2)
                    if subject in articles:
                        title = title_pattern.search(subject).group(1).replace("_",
                                                                               " ")
                        definition = literal.strip()[1:-6]
                        tmpfile.write("%s\t%s\n" % (title, definition.replace("\t", " ")))

def main():
    """ Write a tab separated <term>\t<definition>\n file that will
    be passed to `tab2opf.py` which will generate a .opf file which will passed
    `mobigen` and will result in a .mobi file containing the dictionary.

    Basically:

        python wikimoby.py ->.tab (tabfile)
        python tab2opf.py .tab -> .opf (and a bunch of html files)
        wine mobigen/mobigen.exe .opf -> .mobi

    """
    if len(sys.argv) != 4:
        print __doc__
        sys.exit(1)


    nt_dir, output_file, category = sys.argv[1:4]
    if output_file != sys.argv[-1]:
        levels = sys.argv[-1]
    else:
        levels = 3
    convertor = WikiMobi(nt_dir, output_file, levels)

    logger.info("Getting child categories for %r" % category)
    categories = convertor.get_child_categories(category)

    logger.info("Getting related articles of %r" % category)
    articles = convertor.get_articles(categories)

    _, abstracts_file = tempfile.mkstemp()
    with open(abstracts_file, 'wb+') as tmpfile:
        logger.info("Writing abstracts of articles to tmp file in tab "
                    "format: %r" % category)
        convertor.write_abstracts(articles, tmpfile)

    logger.info("Calling tab2opf.py")
    return_code = subprocess.check_call("tab2opf.py", abstracts_file)
    if return_code == 0: #Success
        os.unlink(abstracts_file)
        logger.info("Calling mobigen.exe")
        subprocess.call("wine", "mobigen/mobigen.exe", abstracts_file)

if __name__ == '__main__':
    main()
