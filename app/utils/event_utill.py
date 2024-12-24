from dataclasses import asdict
from app.db.models.date_model import Date
from app.db.models.event_model import Event
from app.db.models.location_model import Location
from app.db.models.target_type_model import TargetType


def convert_event_to_json(event):
    event_dict = asdict(event)
    event_dict["location"] = asdict(event.location)
    event_dict["date"] = asdict(event.date)
    event_dict["target_types"] = [asdict(t) for t in event.target_types]
    return event_dict


def event_to_json(event):
    event_dict = asdict(event)
    event_dict["location"] = asdict(event.location)
    event_dict["date"] = asdict(event.date)
    event_dict["target_types"] = [asdict(t) for t in event.target_types]
    return event_dict
def to_event(result):
    location = Location(**result["location"])
    target_types = [TargetType(**t) for t in result["target_types"]]
    return Event(
        event_id=result["event_id"],
        num_kill=result["num_kill"],
        num_wound=result["num_wound"],
        number_of_casualties_calc=result["number_of_casualties_calc"],
        date=Date(**result["date"]),
        summary= result["summary"],
        num_preps=result["num_preps"],
        location=location,
        attack_type=result["attack_type"],
        target_types=target_types,
        group_name=result["group_name"]
    )