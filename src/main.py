from RPLCD.i2c import CharLCD
import requests
import time
import signal
import sys
import os

lcd = CharLCD("PCF8574", 0x27)
lcd.clear()

hostname = os.environ.get("PIHOLEMON_HOSTNAME")
debug = os.environ.get("PIHOLEMON_DEBUG")


def error_handler(code):
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Error " + str(code))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("See git.io/JenJh")


if hostname is None:
    print("PIHOLEMON_HOSTNAME is not defined. It should be like http://1.1.1.1 where 1.1.1.1 is the IP of your Pi-hole.")
    error_handler(1)
    sys.exit(1)

if debug is None:
    debug = False
elif debug.lower() == "true":
    debug = True

overflow_text = "1 mil+"

api_map = {
    "summary": hostname + "/admin/api.php?summary"
}

current_data = {
    "totalqueriestoday": "0",
    "totalblockedqueriestoday": "0",
    "percentblocked": "0",
    "domainsonblocklist": "0",
    "fetchedat": 0,
    "error": False
}

# will allow us to selectively update the display
prev_data = {
    "totalqueriestoday": "0",
    "totalblockedqueriestoday": "0",
    "percentblocked": "0",
    "domainsonblocklist": "0",
}


def exit_handler(sig, frame):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Exited Pi-hole")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("LCD monitor")

    print("Exiting due to SIGINT (ctrl+c)")
    sys.exit(0)


def docker_exit_handler(sig, frame):
    lcd.clear()
    print("Exiting due to SIGTERM (docker)")
    sys.exit(0)


signal.signal(signal.SIGINT, exit_handler)

# Handles exiting with docker
signal.signal(signal.SIGTERM, docker_exit_handler)


def debug_log(log):
    if debug:
        print(log)
    return


def update_current_data():
    debug_log("Attempting to get current data...")
    try:
        r = requests.get(api_map["summary"]).json()
        current_data["totalqueriestoday"] = r["dns_queries_today"]
        current_data["totalblockedqueriestoday"] = r["ads_blocked_today"]
        current_data["percentblocked"] = r["ads_percentage_today"]
        current_data["domainsonblocklist"] = r["domains_being_blocked"]
        current_data["fetchedat"] = int(time.time())
        current_data["error"] = False

        debug_log("Got new data")
        debug_log(current_data)

        update_display()
    except Exception as e:
        debug_log("There was an error getting current data:")
        debug_log(e)
        error_handler(2)
        current_data["error"] = True
    return


def update_display():
    if current_data["error"] is True:
        lcd.clear()

    if current_data["totalqueriestoday"] != prev_data["totalqueriestoday"]:
        write_total_queries_today(current_data["totalqueriestoday"])
        prev_data["totalqueriestoday"] = current_data["totalqueriestoday"]

    if current_data["percentblocked"] != prev_data["percentblocked"]:
        write_percent_blocked(current_data["percentblocked"])
        prev_data["percentblocked"] = current_data["percentblocked"]

    if current_data["totalblockedqueriestoday"] != prev_data["totalblockedqueriestoday"]:
        write_total_queries_blocked(current_data["totalblockedqueriestoday"])
        prev_data["totalblockedqueriestoday"] = current_data["totalblockedqueriestoday"]
        
    if current_data["domainsonblocklist"] != prev_data["domainsonblocklist"]:
        write_blacklist_length(current_data["domainsonblocklist"])
        prev_data["domainsonblocklist"] = current_data["domainsonblocklist"]
    return


def write_total_queries_today(nr):
    debug_log("Writing total queries today")

    lcd.cursor_pos = (0, 0)
    # we want to write a max of 7 characters
    nr_ok = nr if len(nr) < 8 else overflow_text
    lcd.write_string(nr_ok)
    return


def write_total_queries_blocked(qb):
    debug_log("Writing total queries blocked today")
    
    qb_ok = qb if len(qb) < 8 else overflow_text
    # right-align
    lcd.cursor_pos = (0, 16 - len(qb_ok))
    lcd.write_string(qb_ok)
    return


def write_percent_blocked(bp):
    debug_log("Writing percent blocked")
    lcd.cursor_pos = (1, 0)
    # max 6 characters-- 100.0%
    lcd.write_string(bp + "%")
    return


def write_blacklist_length(bl):
    debug_log("Writing blacklist length")
    
    bl_ok = bl if len(bl) < 8 else overflow_text
    # right-align
    lcd.cursor_pos = (1, 16 - len(bl_ok))
    lcd.write_string(bl_ok)
    return


def loop():
    update_current_data()
    time.sleep(5)
    return


while True:
    loop()
