import re
cat_pattern = re.compile("Category:([^>]+)")
title_pattern = re.compile("resource/([^>]+)")
articles = set()

with open('../categories.txt', 'rb') as fin:
    categories = set(map(str.strip, fin.readlines()))

with open("../article_categories_en.nt", 'rb') as fin:
    for line in fin:
        (subject, predicate, literal) = line.split(" ")[:3]
        if literal in categories:
            articles.add(subject)

with open("../short_abstracts_en.nt", 'rb') as fin:
    with open('../out.tab', 'wb+') as out_file:
        for line in fin:
            (subject, predicate, literal) = line.split(" ", 2)
            if subject in articles:
                title = title_pattern.search(subject).group(1).replace("_",
                                                                       " ")
                definition = literal.strip()[1:-6]
                out_file.write("%s\t%s\n" % (title, definition.replace("\t", " ")))
