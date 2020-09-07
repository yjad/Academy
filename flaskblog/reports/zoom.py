import json
import requests

from flaskblog.reports.config import config
from flaskblog.reports.DB import insert_row_attendees, insert_row_meeting, create_tables


def load_zoom_meetings(from_dt, to_date=""):
    #conn, cursor = open_db()
    create_tables()  # create tables if not exist

    meeting_report_url = f"https://api.zoom.us/v2/report/users/{config.get('USER_ID')}/meetings?from={from_dt}&to={to_date}?page_size=300"
    headers = {"Authorization": "Bearer " + config.get("JWT_TOKEN")}
    r = requests.get(meeting_report_url, headers=headers)

    meetings = json.loads(r.content)
    if meetings.get("code") == 124:
        print(meetings.get("message"))  # error
        return
    page_count = meetings.get('page_count')
    page_size = meetings.get('page_size')
    total_records = meetings.get('total_records')

    for key, value in meetings.items():
        if key == 'meetings':
            for m in value:
                # print (m)
                print(f"meeting-id: {m.get('id')}, "
                      f"type: {m.get('type')}, "
                      f"topic: {m.get('topic')}, "
                      f"start time: {m.get('start_time')}, "
                      f"No of Participants: {m.get('participants_count')}")
                if insert_row_meeting(m) == -1:
                    print("meeting already loaded, skip it ...")
                    continue  # meeting already exist, skip it

                for k, v in m.items():
                    if k == "uuid":  ## meeting id
                        load_meeting_participants(v, None)
                        pass
    #close_db(cursor)


def load_meeting_participants(meeting_uuid, next_page_token):
    if next_page_token is None:
        meeting_participants_report_url = f"https://api.zoom.us/v2/report/meetings/{meeting_uuid}/participants/"
    else:
        meeting_participants_report_url = f"https://api.zoom.us/v2/report/meetings/{meeting_uuid}/participants?next_page_token={next_page_token}"
    headers = {"Authorization": "Bearer " + config.get("JWT_TOKEN")}

    r = requests.get(meeting_participants_report_url, headers=headers)

    reply = json.loads(r.content)
    page_count = reply.get('page_count')
    page_size = reply.get('page_size')
    total_records = reply.get('total_records')
    next_page_token = reply.get("next_page_token")
    for a in reply.get('participants'):
        d = {"meeting_uuid": meeting_uuid}
        d.update(a)
        insert_row_attendees(d)

    if next_page_token:
        load_meeting_participants(meeting_uuid, next_page_token)  # call itself recursively
    else:
        return  # exit recursive


def get_zoom_report_daily(year, month):

    meeting_report_url = f"https://api.zoom.us/v2/report/daily?year={year}&month={month}"
    headers = {"Authorization": "Bearer " + config.get("JWT_TOKEN")}
    r = requests.get(meeting_report_url, headers=headers)
    report = json.loads(r.content)
    if report.get("code") == 124:
        print(report.get("message"))  # error
        return
    for key, value in report.items():
        if key == 'dates':
            [print(m) for m in value]


def load_zoom_telephone_report(from_dt, to_date=""):

    meeting_report_url = f"https://api.zoom.us/v2/report/telephone??type=1?from={from_dt}&to={to_date}?page_size=300"
    headers = {"Authorization": "Bearer " + config.get("JWT_TOKEN")}
    r = requests.get(meeting_report_url, headers=headers)

    meetings = json.loads(r.content)
    print (meetings)
    if meetings.get("code") == 124:
        print(meetings.get("message"))  # error
        return
    page_count = meetings.get('page_count')
    page_size = meetings.get('page_size')
    total_records = meetings.get('total_records')

    for key, value in meetings.items():
        if key == 'telephony_usage':
            [print (m) for m in value]


def get_meeting_details(meeting_uuid):

    meeting_report_url = f"https://api.zoom.us/v2/report/meetings/{meeting_uuid}"
    headers = {"Authorization": "Bearer " + config.get("JWT_TOKEN")}
    r = requests.get(meeting_report_url, headers=headers)

    meetings = json.loads(r.content)
    if meetings.get("code") == 124:
        print(meetings.get("message"))  # error
        return
    page_count = meetings.get('page_count')
    page_size = meetings.get('page_size')
    total_records = meetings.get('total_records')

    for key, value in meetings.items():
        print (key, ": ", value)
        # if key == 'telephony_usage':
        #     [print (m) for m in value]