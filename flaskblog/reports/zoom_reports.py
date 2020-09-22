#import os
from openpyxl import Workbook
from datetime import timedelta, datetime

#from config import config
from flaskblog.reports.graph import plot_stacked_bar
from flaskblog.reports.DB import exec_query, get_last_meeting_date, get_col_names
from flaskblog.reports.zoom import load_zoom_meetings


def query_to_excel(cmd, file_name, header=None):
    #conn, cursor = open_db()
    rows = exec_query(cmd)
    #close_db(cursor)

    if not header:
        header = get_col_names(cmd)

    wb = Workbook()
    ws = wb.active
    ws.append(header)

    for row in rows:
        ws.append(row)
    wb.save(file_name)


def attendance_sheet(meeting_date):
    update_meetings()   # update meetings first
    if meeting_date:
        cmd = f""" SELECT SUBSTR(join_time,1, 10) as "meeting date", type, topic,  
                        a.user_email, name, sum(a.duration/60) as "duration in min" , 
                		Users.firstname, lastname, profile_field_manager_mon, profile_field_manager_wed, 
                        profile_field_group_id, profile_field_code
                        FROM attendees a 
						LEFT Join student ON a.user_email = student.email
						LEFT Join meetings m ON a.meeting_uuid = m.uuid
                        WHERE "meeting date" = "{meeting_date}"
                        GROUP BY a.user_email, name, "meeting date"
                        ORDER BY 1, 2, 3"""
    else:
        cmd = f"""SELECT SUBSTR(join_time,1, 10) as "meeting date", type, topic,  
                        a.user_email, name, sum(a.duration/60) as "duration in min" , 
                		Users.firstname, lastname, profile_field_manager_mon, profile_field_manager_wed, 
                        profile_field_group_id, profile_field_code
                        FROM attendees a 
						LEFT Join student ON a.user_email = student.email
						LEFT Join meetings m ON a.meeting_uuid = m.uuid
                        GROUP BY a.user_email,name, "meeting date"
                        ORDER BY 1, 2, 3"""

    header = ["meeting date", "meeting type", "meeting topic", "user_email", "Zoom name", "duration (min)", "firstname", "lastname",
              "profile_field_manager_mon",
              "profile_field_manager_wed", "profile_field_group_id", "profile_field_code"]

    if meeting_date:
        file_name = f".\\data\\attendees_{meeting_date}.xlsx"
    else:
        file_name = r".\data\attendees_all.xlsx"

    query_to_excel(cmd, file_name, header)


def list_unmatched_attendees():
    update_meetings()   # update meetings first
    cmd = f"""select substr(join_time,1, 10) as "meeting date", a.user_email, name, user_id, sum(a.duration/60) as "duration in min" 
        from attendees a 
        where a.user_email not in (SELECT email from student)
        group by a.user_email,name, "meeting date"
        order by 1, 2, 3"""
    header = ["meeting date", "Zoom user_email", "Zoom name", "Zoom user_id", "duration"]
    file_name = r".\data\no_matching_attendees.xlsx"
    query_to_excel(cmd, file_name, header)


def stats_attendees():
    update_meetings()   # update meetings first
    cmd = f"""SELECT meeting_date, meeting_type, topic, COUNT(name), COUNT(firstname), COUNT(name) - COUNT(firstname) 
                FROM (
                    SELECT DATE(join_time) as meeting_date, type as meeting_type, topic,  name, firstname
                    FROM attendees a 
                    LEFT Join student ON a.user_email = student.email
                    LEFT Join meetings m ON a.meeting_uuid = m.uuid
                    GROUP BY meeting_date, name 
                    )
                GROUP BY meeting_date
                ORDER BY 1, 2, 3"""
    header = ["meeting date", "meeting_type", "topic", "# of attendees", "Acadmy", "External"]
    file_name = r".\data\stats_attendees.xlsx"
    query_to_excel(cmd, file_name, header)


def update_meetings():
    # get date of last saved meeting
    last_meeting = get_last_meeting_date()
    print (last_meeting)
    #date_time_obj = datetime.strptime(last_meeting, '%Y-%m-%d') +  timedelta(days=1)
    load_zoom_meetings(last_meeting)


def stats_attendees_graph(file_name):
    #update_meetings()
    sql = f"""SELECT meeting_date, meeting_type, topic, COUNT(name), COUNT(firstname), COUNT(name) - COUNT(firstname) 
                    FROM (
                        SELECT DATE(join_time) as meeting_date, type as meeting_type, topic,  name, firstname
                        FROM attendees a 
                        LEFT Join student ON a.user_email = student.email
                        LEFT Join meetings m ON a.meeting_uuid = m.uuid
                        GROUP BY meeting_date, name 
                        )
                    GROUP BY meeting_date
                    ORDER BY 1, 2, 3"""
    #comm, curspr = open_db()
    rows = exec_query(sql)
    #close_db(curspr)
    bars1=[]
    bars2 = []
    names = []
    for row in rows:
        names.append(row[0])    # meeting date
        bars1.append(row[4])    # count (first name) --> Academy students
        bars2.append(row[5])    # External Students
    plot_stacked_bar(bars1, bars2, names, file_name)