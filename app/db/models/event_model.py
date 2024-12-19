from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from mongo_db.models.date_model import Date
from mongo_db.models.location_model import Location
from mongo_db.models.target_type_model import TargetType


@dataclass
class Event:
    event_id: str
    num_kill: int  # מספר ההרוגים
    num_wound: int  # מספר הפצועים
    number_of_casualties_calc: int
    date: Date
    summary: str
    num_preps: int
    location: Location
    attack_type: List[str]
    target_types: List[TargetType]  # מטרות התקיפה
    group_name: List[str]  # שם הארגון האחראי לפעולה

    def __repr__(self):
        return (f"Event(event_id={self.event_id}, num_kill={self.num_kill}, "
                f"num_wound={self.num_wound}, number_of_casualties_calc={self.number_of_casualties_calc}, "
                f"date={repr(self.date)}, summary={self.summary}, num_preps={self.num_preps}, "
                f"location={repr(self.location)}, attack_type={self.attack_type}, "
                f"target_types={repr(self.target_types)}, group_name={self.group_name})")