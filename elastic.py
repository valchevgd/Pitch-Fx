from elasticsearch import Elasticsearch


def client():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])
