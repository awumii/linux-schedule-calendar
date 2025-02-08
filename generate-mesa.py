import requests
import csv
from icalendar import Calendar, Event
from datetime import datetime

calendar = Calendar()

# Create a new calendar event
def add_event(title, date, description):
    event = Event()
    event.add('summary', title)
    event.add('dtstart', date)
    event.add('description', description)
    calendar.add_component(event)


def download_schedule():
    url = "https://gitlab.freedesktop.org/mesa/mesa/-/raw/main/docs/release-calendar.csv"
    response = requests.get(url)
    
    with open('/tmp/release-calendar.csv', 'wb') as f:
        f.write(response.content)

def parse_schedule():
    with open('/tmp/release-calendar.csv', 'r') as f:
        reader = csv.reader(f)
        
        releases = []
        for row in reader:
            # Skip empty rows
            if not row:
                continue
            
            # Extract relevant data
            release_date_str = row[1].strip()
            release_version = row[2].strip()
            notes = row[4].strip() if len(row) > 4 else ""
            
            if release_date_str and release_version:
                release_date = datetime.strptime(release_date_str, "%Y-%m-%d")
                releases.append({
                    "release_date": release_date,
                    "release_version": release_version,
                    "notes": notes
                })
    
    return releases

def generate_schedule():
    releases = parse_schedule()

    for release in releases:
        release_date = release["release_date"]
        release_version = release["release_version"]
        notes = release["notes"]

        # Event description with notes if available
        description = f'Release Version: {release_version}'
        if notes:
            description += f'\nNotes: {notes}'

        # Add event for the release
        add_event(f'Mesa {release_version} Release', release_date, description)

def main():
    download_schedule()
    generate_schedule()
    with open('mesa-schedule.ics', 'wb') as f:
        f.write(calendar.to_ical())

if __name__ == "__main__":
    main()
