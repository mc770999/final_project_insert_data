from ..mongo_database import db, event_collection
from ..models.event_model import Event
from app.utils.event_utill import to_event, event_to_json


def create_events(events):
    try:
        ids = event_collection.insert_many(events)
        return ids
    except Exception as e:
        print(e)

def read_event(event_id: str) -> Event:
    try:
        result = event_collection.find_one({"event_id": event_id})
        if result:
            return to_event(result)
        raise Exception("event not found")
    except Exception as e:
        print(e)
        return e

def update_event(event_id: str, updated_data: dict):
    try:
        result = event_collection.update_one({"event_id": event_id}, {"$set": updated_data})
        if result:
            return
        raise Exception("event not updated")
    except Exception as e:
        print(e)



def delete_event(event_id: str):
    try:
        result = event_collection.delete_one({"event_id": event_id})
        if result:
            return result
        raise Exception("event not delete")
    except Exception as e:
        print(e)


def check_and_insert_event(new_event):

    query = {
        "date.day",
        "date.month",
        "date.year",
        "location.city",
        "num_kill",
        "num_wound",
        "number_of_casualties_calc",
        "group_name",
    }

    existing_event = event_collection.find_one(query)

    if existing_event:

        existing_event = Event(**existing_event)

        if not any(g for g in existing_event.group_name if g in new_event.group_name):
            event_collection.insert_one(new_event.__dict__)
            print("Inserted new event into the database.")
            return

        print("Event already exists. Checking for missing fields to update.")

        for field, value in new_event.__dict__.items():
            if value and value != []:
                if field not in existing_event.__dict__ or not existing_event.__dict__[field]:
                    existing_event.__dict__[field] = value

        event_collection.update_one({"_id": existing_event["_id"]}, {"$set": existing_event})
        print(f"Updated event!")

    else:

        event_collection.insert_one(new_event.__dict__)
        print("Inserted new event into the database.")

