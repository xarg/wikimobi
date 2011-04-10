root_category = '<http://dbpedia.org/resource/Category:Physics>'
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
"""while True:
    count = len(categories)
    for parent, children in relations.iteritems():
        if parent in categories and parent not in parents:
            categories = children | categories
            parents.add(parent)
    if count == len(categories):
        break
    import pdb; pdb.set_trace()
    print count
"""
with open('../categories.txt', 'wb+') as fout:
    fout.write("\n".join(categories))
