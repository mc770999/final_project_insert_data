import json
from datetime import datetime

import numpy as np
import pandas as pd
import toolz as t

from app.db.models.date_model import Date
from app.db.models.event_model import Event
from app.db.models.location_model import Location
from app.db.models.target_type_model import TargetType
from typing import List



def split_into_chunks(lst, chunk_size):
    return list(t.partition_all(chunk_size, lst))


def convert_to_target_types(row):
    target_types = []
    count = 1
    for targtype in ["targtype1_txt", "targtype2_txt", "targtype3_txt"]:
        if not pd.isna(row[targtype]) and row[targtype].lower() != "unknown":
            target_types.append(TargetType(target_type=targtype, target=row[f"target{count}"]))
        count += 1

    return target_types

def convert_to_group_names(row):
    group_names = []
    for group_name in ["gname", "gname2", "gname3"]:
        if not pd.isna(row[group_name]) and row[group_name].lower() != "unknown":
            group_names.append(row[group_name])
    return group_names

def convert_to_attack_type(row):
    attack_types_txt = []
    for attack_type_txt in ["attacktype1_txt", "attacktype2_txt", "attacktype3_txt"]:
        if not pd.isna(row[attack_type_txt]) and row[attack_type_txt].lower() != "unknown":
            attack_types_txt.append(row[attack_type_txt])
    return attack_types_txt


def calc_number_of_casualties(num_wound, num_kill):
    num_wound = to_int(num_wound)
    num_kill = to_int(num_kill)
    if isinstance(num_wound, int) and isinstance(num_kill, int):
        return num_wound * 1 + num_kill * 2
    elif isinstance(num_wound, int):
        return num_wound * 1
    elif isinstance(num_kill, int):
        return num_kill * 2
    return

def to_int(val):
    try:
        return int(val)
    except ValueError:
        return None


def if_none(val):
    return None if pd.isna(val) else val

def to_date(day,month,year):
    day, month, year = to_int(day), to_int(month), to_int(year)
    day, month, year = None if day == 0 else day, None if month == 0 else month, None if year == 0 else year
    return Date(day=day, month=month, year=year)
def process_csv(file_path: str) -> List[Event]:
    # Load CSV file
    df = pd.read_csv(file_path, encoding="iso-8859-1")


    df[["nperps", "nkill", "nwound"]] = (
        df[["nperps", "nkill", "nwound"]]
        .where(df[["nperps", "nkill", "nwound"]] >= 0, None)
    )

    df.rename(columns={
        'eventid': 'event_id',
        'iyear': 'year',
        'imonth': 'month',
        'iday': 'day',
        'country_txt': 'country_name',
        'region_txt': 'region_txt',
        'city': 'city',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'nkill': 'num_kill',
        'nwound': 'num_wound',
    }, inplace=True)

    # Filter necessary columns


    events = []
    for _, row in df.iterrows():
        location = Location(
            country=if_none(row['country_name']),
            region=if_none(row['region_txt']),
            city=if_none(row['city']),
            latitude=if_none(row['latitude']),
            longitude=if_none(row['longitude'])
        )
        event = Event(
            event_id=if_none(row['event_id']),
            num_kill=to_int(row['num_kill']),
            num_wound=to_int(row['num_wound']),
            number_of_casualties_calc=calc_number_of_casualties(row['num_wound'], row['num_kill']),
            date=to_date(row["day"], row["month"], row["year"]),
            summary=if_none(row["summary"]),
            num_preps=to_int(row["nperps"]),
            location=location,
            attack_type=convert_to_attack_type(row),
            target_types=convert_to_target_types(row),
            group_name=convert_to_group_names(row)
        )
        events.append(event)


    return events








def process_csv_2(csv_file: str):
    df = pd.read_csv(csv_file, encoding="iso-8859-1")

    events = []

    for _, row in df.iterrows():
        date_obj = datetime.strptime(row['Date'], "%d-%b-%y")
        event_date = Date(day=date_obj.day, month=date_obj.month, year=date_obj.year)

        location = Location(
            country=if_none(row['Country']),
            region=None,
            city=if_none(row['City']),
            latitude=None,
            longitude=None
        )

        group_name = [row['Perpetrator']] if row['Perpetrator'] not in ["Unknown", None] else []

        num_kill = to_int(row['Fatalities'])
        num_wound = to_int(row['Injuries'])
        number_of_casualties = calc_number_of_casualties(row['Injuries'], row['Fatalities'])

        event = Event(
            event_id=None,
            num_kill=num_kill,
            num_wound=num_wound,
            number_of_casualties_calc=number_of_casualties,
            date=event_date,
            summary=if_none(row['Description']),
            num_preps=1,  # Default value, can be adjusted based on the data
            location=location,
            attack_type=[],
            target_types=[],
            group_name=group_name
        )

        events.append(event)

    return events


def save_json_to_file(json_list, filename):
    try:
        json_list = [{"data": json_list}]
        if not isinstance(json_list, list):
            raise ValueError("Input should be a list of JSON objects.")

        if not all(isinstance(item, dict) for item in json_list):
            raise ValueError("All items in the list should be JSON objects (dictionaries).")

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(json_list, file, ensure_ascii=False, indent=4)

        print(f"Data successfully saved to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


def is_subset(list_a, list_b):
    return set(list_a).issubset(set(list_b))


def merge_dicts(dict1, dict2):
    merged = {}
    for key, val in dict1.items():
        if key == 'target_types':
            continue
        elif isinstance(val, dict):
            merged[key] = merge_dicts(dict1[key], dict2[key])
        elif isinstance(val, list):
            merged[key] = list(set(dict1[key] + dict2[key]))
        else:
            merged[key] = dict1[key] if dict1[key] else dict2[key] if dict2[key] else None
    return merged

def merge_event_lists(list1, list2):

    query_fields = {
        "date.day",
        "date.month",
        "date.year",
        "location.city",
        "num_kill",
        "num_wound",
        "number_of_casualties_calc",
        "group_name",
    }

    combined = list1 + list2

    processed = set()
    merged_list = []

    for i, event1 in enumerate(combined):
        if i in processed:
            continue

        merged_event = event1
        for j, event2 in enumerate(combined):
            if j <= i or j in processed:
                continue

            matches = all(
                is_subset(event1.get("group_name"), event2.get("group_name")) if field == "group_name" else
                (
                    (event1.get(field.split('.')[0], {}).get(field.split('.')[1]) == event2.get(field.split('.')[0],
                                                                                                {}).get(
                        field.split('.')[1]))
                    if '.' in field else event1.get(field) == event2.get(field)
                )
                for field in query_fields
            )

            if matches:
                merged_event = merge_dicts(event1, event2)
                processed.add(j)

        merged_list.append(merged_event)
        processed.add(i)

    return merged_list



