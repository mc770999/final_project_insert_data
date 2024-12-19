from elasticsearch.helpers import bulk

from ..elastic_database import es_client


def insert_document(index_name: str, document: dict, doc_id: str = None) -> dict:
    try:
        if doc_id:
            response = es_client.index(index=index_name, id=doc_id, document=document)
        else:
            response = es_client.index(index=index_name, document=document)
        return response
    except Exception as e:
        return {"error": str(e)}

def read_document(index_name: str, doc_id: str) -> dict:
    try:
        response = es_client.get(index=index_name, id=doc_id)
        return response["_source"]
    except Exception as e:
        return {"error": str(e)}


def insert_many(index_name: str, documents: list[dict]) -> dict:

    actions = []
    for document in documents:
        action = {
            "_index": index_name,
            "_source": document
        }
        if "_id" in document:
            action["_id"] = document["_id"]
        actions.append(action)

    try:
        success, errors = bulk(es_client, actions)
        return {"success": success, "errors": errors}
    except Exception as e:
        return {"error": str(e)}

def get_all_indexes():
    try:
        # Request to get all indices
        response = es_client.cat.indices(format="json")  # The format "json" returns the result as a JSON object
        index_names = [index['index'] for index in response]  # Extract only the index names
        return index_names
    except Exception as e:
        return {"error": str(e)}
