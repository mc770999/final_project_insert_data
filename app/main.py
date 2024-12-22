from dataclasses import asdict
from app.service.insert_service import insert_list_to_mongo, insert_list_to_elastic
from app.utils.csv_util import process_csv, process_csv_2, save_json_to_file, merge_event_lists

if __name__ == '__main__':

    event_list1 = process_csv("./data/globalterrorismdb_0718dist-1000 rows.csv")
    event_list2 = process_csv_2("./data/RAND_Database_of_Worldwide_Terrorism_Incidents - 5000 rows.csv")
    event_list_merged = merge_event_lists(list(map(asdict,event_list1)), list(map(asdict,event_list2)))
    # insert_list_to_elastic(event_list_merged)
    insert_list_to_mongo(event_list_merged)
