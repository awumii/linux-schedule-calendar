# Linux & Mesa Release Schedule Calendar

Add the **Linux Kernel** and **Mesa** release schedules directly to your calendar!  

## Overview

This repository provides Python scripts that generate iCalendar files (`.ics`) for the **Linux Kernel** and **Mesa** release schedules. This repository also contains automatically updated calendars that can be directly imported to your calendar.

### Features:
- Predicts when the future **Linux Kernel** release candidates will be released.
- Includes the official [Mesa release schedule](https://docs.mesa3d.org/release-calendar.html)

## How to Use

You can import the following iCalendar(s) directly into your calendar application:

- **Linux Kernel**: [https://raw.githubusercontent.com/awumii/linux-schedule-calendar/main/linux-schedule.ics](https://raw.githubusercontent.com/awumii/linux-schedule-calendar/main/linux-schedule.ics)
- **Mesa**: [https://raw.githubusercontent.com/awumii/linux-schedule-calendar/main/mesa-schedule.ics](https://raw.githubusercontent.com/awumii/linux-schedule-calendar/main/mesa-schedule.ics)

> [!WARNING]
> Please do **not** download the `.ics` file directly. Use your calendar application's **import from URL** feature to automatically keep your calendar updated.

## Screenshots

Here's a preview of what the calendars look like in your application:

![Screenshot 1](.github/1.png)
![creenshot 2](.github/2.png)

## Requirements

 - Python 3.x
 - Linux
 - Required Python packages:

```
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.