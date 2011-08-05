#!/usr/bin/env python

__doc__ = """
Create mobi files from wikipedia categories
===========================================

Required .nt file(s) can be found at:

#Contains short abstracts of the articles (first paragraph)

    http://downloads.dbpedia.org/3.6/en/short_abstracts_en.nt.bz2 (300mb)

#Contains relations between articles and categories

    http://downloads.dbpedia.org/3.6/en/article_categories_en.nt.bz2 (115mb)

#Contains relations between categories and subcategories in a skos type relation

    http://downloads.dbpedia.org/3.6/en/skos_categories_en.nt.bz2 (18mb)

All uncompressed: ~3.4GB

More info here:

    http://wiki.dbpedia.org/Downloads36

"""
import re
import tempfile
import subprocess
import argparse
import os
import shutil
import logging

logger = logging.getLogger("wikimobi")
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

cat_pattern = re.compile("Category:([^>]+)")
title_pattern = re.compile("resource/([^>]+)")

class WikiMobi(object):

    def __init__(self, nt_dir):
        """ """
        self.nt_dir = nt_dir

    def get_child_categories(self, category, levels):
        """Given a root `category` get all it's child categories up until
        `levels` are reached. Levels as in depth of the `graph`

        """
        root_category = '<http://dbpedia.org/resource/Category:%s>' % category
        category_levels = [set() for i in range(0, levels)]

        relations = {}
        parents = set()

        #Generate relations dictionary betweend categories
        with open(os.path.join(self.nt_dir, 'skos_categories_en.nt'),
                  'rb') as fin:
            for line in fin:
                (category, rel, parent) = line.split(" ")[:3]
                #Get only broader relations
                if rel == '<http://www.w3.org/2004/02/skos/core#broader>':
                    if parent not in relations:
                        relations[parent] = set()
                    relations[parent].add(category)

        categories = set()
        category_levels[0] = relations[root_category]
        for i in range(0, levels-1):
            current_level = category_levels[i]
            for category in current_level:
                if category in relations:
                    category_levels[i+1] |= relations[category]
        for level in category_levels:
            categories |= level

        return categories

    def get_articles(self, categories):
        """ From the article_categories get the articles """
        articles = set()
        with open(os.path.join(self.nt_dir, "article_categories_en.nt"),
                  'rb') as fin:
            for line in fin:
                (subject, predicate, literal) = line.split(" ")[:3]
                if literal.strip() in categories:
                    articles.add(subject.strip())
        return articles

    def write_abstracts(self, articles, tmpfile):
        """ Write `articles` abstracts in `tmpfile`"""
        with open(os.path.join(self.nt_dir, "short_abstracts_en.nt"),
                  'rb') as fin:
            for line in fin:
                (subject, predicate, literal) = line.split(" ", 2)
                if subject in articles:
                    title = title_pattern.search(subject).group(1).replace("_",
                                                                           " ")
                    definition = literal.strip()[1:-6].replace('\"', '"')
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

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-nt', dest='nt_dir',
                        help='Directory where .nt files are')
    parser.add_argument('-o', dest='output_file',
                        help='Output filename (without extension)')
    parser.add_argument('-c', dest='category',
                        help='Wikipedia category')
    parser.add_argument('-l', dest='levels', type=int, default=3,
                        help='Number of levels beneeth the wikipedia category.'
                        ' This is used to get the related categories.')

    args = parser.parse_args()
    nt_dir = args.nt_dir
    output_file = args.output_file
    category = args.category
    levels = args.levels

    convertor = WikiMobi(nt_dir)

    logger.info("Getting child categories for %r" % category)
    categories = convertor.get_child_categories(category, int(levels))

    logger.info("Getting related articles of %r" % category)
    articles = convertor.get_articles(categories)

    _, abstracts_file = tempfile.mkstemp()
    with open(abstracts_file, 'wb+') as tmpfile:
        logger.info("Writing abstracts to %s in tab format" % abstracts_file)
        convertor.write_abstracts(articles, tmpfile)

    tabfile = "%s.tab" % output_file

    tmpdir = tempfile.mkdtemp()

    logger.info("Renamed tmpfile to %s" % tabfile)
    os.rename(abstracts_file, os.path.join(tmpdir, tabfile))

    current_dir = os.getcwd()
    os.chdir(tmpdir)
    try:
        cmd = ["python", os.path.join(current_dir, "tab2opf.py"), tabfile]
        logger.info("Calling %s" % " ".join(cmd))
        return_code = subprocess.check_call(cmd)
        if return_code == 0: #Success
            cmd = ["wine", os.path.join(current_dir, "mobigen", "mobigen.exe"),
                    "-unicode", "%s.opf" %
                   os.path.basename(output_file)]
            logger.info("Calling %s" % " ".join(cmd))
            return_code = subprocess.call(cmd)
    finally:
        mobifile = os.path.join(tmpdir, output_file + '.mobi')
        logger.info("Trying to copy .mobi file %s to current dir", mobifile)
        shutil.copy(mobifile, current_dir)
        os.chdir(current_dir)
        logger.info("Cleaning up %s", tmpdir)
        shutil.rmtree(tmpdir)
    logger.info("Finished")

if __name__ == '__main__':
    main()
