from booking import post_booking
from check import check
import json
import pandas as pd
import time
if __name__ == "__main__":
    # load config from JSON
    log=open("log.txt", "a", encoding="utf-8")
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    rendelok=pd.read_csv("rendelok.csv", encoding="utf-8", delimiter=";")
    # create dictionary for quick name lookup
    rendelo_names = dict(zip(rendelok["id"], rendelok["nev"]))
    sportolo_id = 306048
    print("Starting booking process...")
    log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\tStarting booking process...\n")
    print(rendelok)
    try:
        for rendelo_id in rendelok["id"]:
            resp = post_booking(config, rendelo_id, sportolo_id)
            rendelo_name = rendelo_names.get(rendelo_id, "Unknown")
            apttime = check(resp.text)
            if apttime:
                log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}	Rendelő: {rendelo_name} (ID: {rendelo_id}), Status: {resp.status_code}, Időpont: {apttime}\n")
                print(f"status {resp.status_code} - VAN IDŐPONT: {apttime} @ {rendelo_name}")
            else:
                log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}	Rendelő: {rendelo_name} (ID: {rendelo_id}), Status: {resp.status_code}, Nincs szabad időpont\n")
                print(f"status {resp.status_code} - NINCS SZABAD IDŐPONT: {rendelo_name}")
            time.sleep(0.1)
    except Exception as e:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\tError: {str(e)}\n")
        print("Error:", str(e))
    finally:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\tBooking process completed.\n")
        log.close()