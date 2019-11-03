from elasticsearch import TransportError

from elastic import client

cln = client()


def find_index(index):
    try:
        cln.search(index=index)

        return True

    except TransportError:
        return False
