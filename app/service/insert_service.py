from ..db.repository.elastic_repository import insert_many, insert_document
from ..db.repository.mongo_repository import create_events


def insert_list_to_mongo(event_list):
    try:
        ids = create_events(event_list)
        print(ids)
    except Exception as e:
        print(e)

def insert_list_to_elastic(event_list):
    try:
        for e in event_list:
            try:
                insert_document("historical_terror_attack", e)
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)

