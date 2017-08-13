import json

import en_core_web_md
from annoy import AnnoyIndex

"""
Script zum Erstellen des Annoy-Index mit den Wort-Vektoren der ImageNet-Konzepte.
"""

if __name__ == "__main__":
    nlp = en_core_web_md.load()

    with open('imagenet_labels_with_annoy_id.json') as f:
        imagenet_labels = json.load(f)

    vector_length = 300
    n_trees = 500
    index = AnnoyIndex(vector_length)

    added = []
    failed = []

    for label in imagenet_labels:
        human_string = nlp(label['human_string'])

        if human_string.has_vector:
            added.append(label)
            index.add_item(label['id'], human_string.vector)
        else:
            failed.append(label)

    index.build(n_trees)
    index.save('spacy.ann')

    print 'finished building annoy index'
