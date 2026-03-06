from booking import post_booking
from check import check
import json
import pandas as pd
import time
from tkinter import messagebox
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import Queue

# Lock for thread-safe logging and messagebox
log_lock = Lock()
message_queue = Queue()

def process_rendelo(rendelo_id, rendelo_names, config, sportolo_id, log_file):
    """Process a single rendelő"""
    try:
        resp = post_booking(config, rendelo_id, sportolo_id)
        rendelo_name = rendelo_names.get(rendelo_id, "Unknown")
        apttime = check(resp.text)
        
        with log_lock:
            if apttime:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}	Rendelő: {rendelo_name} (ID: {rendelo_id}), Status: {resp.status_code}, Időpont: {apttime}\n")
                log_file.flush()
                print(f"status {resp.status_code} - VAN IDŐPONT: {apttime} @ {rendelo_name}")
                
                # Check if the appointment is in March (03)
                if "-03-" in apttime:
                    message_queue.put((rendelo_name, apttime))
            else:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}	Rendelő: {rendelo_name} (ID: {rendelo_id}), Status: {resp.status_code}, Nincs szabad időpont\n")
                log_file.flush()
                #print(f"status {resp.status_code} - NINCS SZABAD IDŐPONT: {rendelo_name}")
    except Exception as e:
        with log_lock:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}	Rendelo ID {rendelo_id} - Error: {str(e)}\n")
            log_file.flush()
            print(f"Error processing rendelo {rendelo_id}: {str(e)}")

if __name__ == "__main__":
    # load config from JSON
    log=open("log.txt", "a", encoding="utf-8")
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    rendelok=pd.read_csv("rendelok.csv", encoding="utf-8", delimiter=";")
    # create dictionary for quick name lookup
    rendelo_names = dict(zip(rendelok["id"], rendelok["nev"]))
    sportolo_id = 306048
    print(rendelok)
    # Create hidden root window for messagebox
    root = tk.Tk()
    root.withdraw()
    while True:
        try:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"Booking process started at {current_time}")
            log.write(f"{current_time}\tStarting booking process...\n")
            log.flush()
            
            # Use ThreadPoolExecutor for parallel processing
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(process_rendelo, rendelo_id, rendelo_names, config, sportolo_id, log)
                    for rendelo_id in rendelok["id"]
                ]
                # Wait for all tasks to complete
                for future in futures:
                    future.result()
            
            # Process all messages in the queue and show messageboxes
            while not message_queue.empty():
                rendelo_name, apttime = message_queue.get()
                messagebox.showinfo("Áprili Időpont!", f"Rendelő: {rendelo_name}\nIdőpont: {apttime}")
            
            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\tBooking process completed.\n")
            log.flush()
            time.sleep(60)  # Wait for 60 seconds before checking again
        except Exception as e:
            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\tError: {str(e)}\n")
            log.flush()
            print("Error:", str(e))
    
    log.close()
    root.destroy()