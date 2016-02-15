# Boulder Indoor Soccer calendar creator

This script will parse [boulderindoorsoccer.com](boulderindoorsoccer.com) and create an ICS calendar file in the directory where it is executed.

## How to run

With python installed (I suggest downloading python through anaconda from [here](https://www.continuum.io/downloads)) go to the location of the "bis-cal.py" file and type:

    python bis-cal.py <team>

where `<team>` is the name of the team who's calendar you want. The script will also look up teams from a subset of a team name. For example, "Slothy" will generate the calendar for the team "Sooooo Slothy" given that there are no other teams with that name.

## Importing the calendar into Google Calendar

The ICS file can be imported into Google calendars following [these instructions](http://www.howtogeek.com/howto/30834/add-an-ical-or-.ics-calendar-to-google-calendar/).

