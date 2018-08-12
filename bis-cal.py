import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from dateutil.parser import parse
from datetime import datetime, timedelta
import pytz
import sys

def getUrl(team):
    with requests.Session() as s:
        url = 'http://www.boulderindoorsoccer.com/standings/adult_standings.php'
        soup = BeautifulSoup(s.get(url).text,'html.parser')
        # Session
        selector = soup.find("select", attrs={"class":"scheduleheader"})
        session = selector.findAll("option")[0].text

        # Team Name and Link
        table = soup.find("table", attrs={"class":"scheduleTable"})
        count = 0
        teams = []
        leagues = []
        link = None
        for tr in table.findAll("tr"):
            ncol = len(tr.findAll("td"))
            if ncol == 1:
                tds = tr.findAll("td")
                league = tds[0].text
            tds = tr.findAll("td", attrs={"align":"left"})
            if ncol > 1 and len(tds) > 0:
                tCol = tds[0]
                if team in tCol.text:
                    teams.append(tCol.text)
                    leagues.append(league)
                    link = tCol.findAll("a")[0]['href']
                    count += 1
        if count != 1:
            if count > 1:
                print("Found too many teams ({count} matches): ".format(**locals()))
                for t in teams:
                    print("  {t}".format(**locals()))

                print("\nBe more specifc!")
            elif count == 0:
                print("Team not found!")
            return None, None, None
        return link, teams[0], session, leagues[0]

def bis_cal(team):

    mt = pytz.timezone('US/Mountain')
    utc = pytz.utc

    link, team_name, session, league = getUrl(team)

    if link:
        with requests.Session() as s:
            url_root = 'http://www.boulderindoorsoccer.com/schedules/'
            url = url_root + link + "&l={}".format(league.strip().replace(' ','+'))
            soup = BeautifulSoup(s.get(url).text,'html.parser')
            table = soup.find("table", attrs={"class":"scheduleTable"})
            c = Calendar()
            for tr in table.findAll("tr"):
                good_line = False
                column = 1
                for td in tr.findAll("td"):
                    if good_line == True:
                        if column == 2:
                            home_team = td.text.strip()
                        elif column == 5:
                            away_team = td.text.strip()
                        column += 1
                    for span in td.findAll("span"):
                        date = span.text[9:-1].strip()
                    if td.text[0].isdigit() and good_line == False:
                        time = td.text
                        good_line = True
                        column += 1
                # Create calendar event
                if good_line:
                    e = Event()
                    e.name = "Soccer: " + home_team + " v.s. " + away_team
                    timestamp = parse(date + " " + time)
                    mt_time = mt.localize(timestamp)
                    e.begin = mt_time#.astimezone(utc)
                    e.duration = timedelta(minutes=50)
                    e.location = "Boulder Indoor Soccer, 3203 Pearl Street, Boulder, CO 80301, United States"
                    c.events.add(e)

            cname = team_name.replace(' ','-') + '-' + session.replace(' ','-') + '.ics'
            with open(cname, 'w') as ics_file:
                ics_file.writelines(c)
            print("Calendar succesfully written for {team_name}, {session}: \"{cname}\"".format(**locals()))
    else:
        return None

bis_cal(sys.argv[1])
