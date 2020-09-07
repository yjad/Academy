
from zoom import load_zoom_meetings, get_zoom_report_daily, load_zoom_telephone_report, get_meeting_details
from zoom_reports import stats_attendees, attendance_sheet, list_unmatched_attendees, update_meetings, \
    stats_attendees_graph

if __name__ == "__main__":
    #load_zoom_meetings("2020-06-15", "2020-07-14")
    #load_zoom_meetings("2020-07-01")
    #load_zoom_meetings("2020-07-26")
    #attendance_sheet("2020-08-11")
    #attendance_sheet("")
    #stats_attendees()
    #list_unmatched_attendees()
    #update_meetings()   # update meetings starts after the last loaded meeting
    #get_zoom_report_daily(2020,8)
    #load_zoom_telephone_report("2020-07-26")
    #get_meeting_details("Hce5zSsbRPmL+1l0VKGmVQ==")
    stats_attendees_graph()