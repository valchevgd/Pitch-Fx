from elastic import client

cln = client()


def add_document(index, doc_id, doc_type, body):

    index = index.lower()

    resp = cln.index(index=index,
                     id=doc_id,
                     doc_type=doc_type,
                     body=body)

    print(resp['result'])
