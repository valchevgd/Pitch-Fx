from elastic import client
from search import find_index

cln = client()


def create(index):
    index = index.lower()

    if find_index(index):
        print('Index already created')
    else:
        result = cln.indices.create(index=index)

        print('index ' + result['index'] + ' created')
