import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime, timedelta

calendar = Calendar()

def fetch_mainline_release():
    # Fetch mainline release version and date from kernel.org
    url = "https://www.kernel.org/"
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    mainline_data = soup.find("td", string="mainline:").find_next_siblings("td")
    
    # Extract version and release date
    version = mainline_data[0].strong.text
    release_date = mainline_data[1].text.strip()
    release_date = datetime.strptime(release_date, "%Y-%m-%d")
    
    return version, release_date

# Create a new calendar event
def add_event(title, date, description):
    event = Event()
    event.add('summary', title)
    event.add('dtstart', date)
    event.add('description', description)
    calendar.add_component(event)

def generate_release_schedule(version, release_date):
    # When there are no release candidates yet
    if ("rc" not in version):
        add_event(f'Linux {version}', release_date, f'Linux Kernel {version} was released.')
        return

    # Determine starting RC version number
    base_version, rc_version_string = version.split('-rc')
    rc_num = int(rc_version_string)

    # This has to be created because values will have to be sorted later
    rc_before_current = {}

    # This value is set for compatibility with rc8, which is not always released.
    last_rc_date = release_date

    # Calculate dates for RCs before the current RC
    for rc in range(1, rc_num):
        rc_date = release_date - timedelta(weeks=(rc_num - rc))
        rc_before_current[rc] = rc_date

    # Add events for RCs before the current RC
    for rc in sorted(rc_before_current.keys()):
        rc_date = rc_before_current[rc]  # Ensure correct date assignment here
        #print(f"{base_version}-rc{rc}: {rc_date.strftime('%Y-%m-%d')}")
        add_event(f'Linux {base_version}-rc{rc}', rc_date, f'Linux Kernel {base_version}-rc{rc} was released.')
    
    # Current date
    add_event(f'Linux {version}', release_date, f'Linux Kernel {base_version}-rc{rc_num} was released. This is currently the latest release candidate.')

    # Calculate dates for future RCs
    for rc in range(rc_num + 1, 8):  # Assuming up to rc7.
        rc_date = release_date + timedelta(weeks=(rc - rc_num))
        add_event(f'Linux {base_version}-rc{rc}', rc_date, f'Linux Kernel {base_version}-rc{rc} will be released.')
        last_rc_date = rc_date

    # Predict stable release date as one week after the last release candidate.
    stable_release_date = last_rc_date + timedelta(weeks=1)
    
    # Warn users that there could be an -rc8 released instead of stable.
    suffix = ""
    if (rc_num != 8):
        suffix = " Please note that -rc8 might be released on this date instead."

    add_event(f'Linux Kernel {base_version} Stable Release', stable_release_date, f'Stable release of Linux Kernel {base_version} is expected.{suffix}')

def main():
    version, release_date = fetch_mainline_release()
    generate_release_schedule(version, release_date)
    with open('linux-schedule.ics', 'wb') as f:
        f.write(calendar.to_ical())

if __name__ == "__main__":
    main()
