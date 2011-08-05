wikimobi
=========

Convert wikipedia abstracts to mobi dictionary.
This way your kindle will have dictionary lookups in wikipedia articles.

Note: Make sure you have python2.7 or higher and wine (for mobigen.exe) installed.

Usage::
    
    git clone git://github.com/humanfromearth/wikimobi.git
    cd wikimobi/
    sudo python setup.py install
    wikimobi -nt path_to_nt_files_dir/ -o physics -c Physics

This will create a physics.mobi in your current directory which is the dictionary.

Required .nt file(s) can be found at:

Contains short abstracts of the articles (first paragraph)::

    http://downloads.dbpedia.org/3.6/en/short_abstracts_en.nt.bz2 (300mb)

Contains relations between articles and categories::

    http://downloads.dbpedia.org/3.6/en/article_categories_en.nt.bz2 (115mb)

Contains relations between categories and subcategories in a skos type relation::

    http://downloads.dbpedia.org/3.6/en/skos_categories_en.nt.bz2 (18mb)

All uncompressed: ~3.4GB

More info here::

    http://wiki.dbpedia.org/Downloads36

Credits
---------

The first version was developed during a coding day at http://pybucuresti.grep.ro/
with the help of Andrei Laza  - Thanks man!

