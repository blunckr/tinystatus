import requests
import os
from datetime import datetime, timedelta, date
import json
import time

print("\n==STARTING==\n")

HOURLY_RATE = 50 # paycheck / 11 / 8
DAILY_HOURS = 8

def get_entries(start, end):
    resp = requests.get("https://api.harvestapp.com/api/v2/time_entries.json", headers={
        "Authorization": "Bearer "+ os.getenv("HARVEST_AUTH"),
        "Harvest-Account-ID": "330810",
    }, params={"from": start, "to": end}
    )

    return resp.json()['time_entries']


def sum_hours(entries):
    sum = 0
    for entry in entries:
        sum += entry["hours"]
    return sum


def get_daily_hours():
    current_date = datetime.now().strftime('%Y-%m-%d')
    entries = get_entries(current_date, current_date)
    return sum_hours(entries)

def get_weekly_hours():
    today = date.today()
    # numeric day of the week, 0 is monday
    weekday = today.weekday()
    monday = today - timedelta(days=weekday)
    sunday = monday + timedelta(days=6)

    entries = get_entries(monday, sunday)
    return sum_hours(entries)

def required_hours():
    return (date.today().weekday() + 1) * DAILY_HOURS

def daily_message(required_hours, weekly_hours):
    time_left = required_hours - weekly_hours
    if time_left <= 0:
        return "You're done!! "
    else:
        finished_at = datetime.now() + timedelta(hours=time_left)
        return "Finishing at:" + finished_at.strftime('%l:%M%p')

def pay_today(daily_hours):
    return f"${daily_hours * HOURLY_RATE}"

def main():
    daily_hours = get_daily_hours()
    weekly_hours = get_weekly_hours()

    print(pay_today(4.3))
    print(daily_message(required_hours(), weekly_hours))

if __name__ == "__main__":
    main()

