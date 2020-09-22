from flask import render_template, request, Blueprint, url_for
from flask_login import login_required
from flaskblog.models import Post
from flaskblog.reports.zoom_reports import stats_attendees_graph, update_meetings

IMAGE_DIR= r"C:\Yahia\Home\Yahia-Dev\Python\Academy\flaskblog\static\out"

reports = Blueprint('reports', __name__)


@reports.route("/reports/attendance_graph")
@login_required
def attendance_graph():

    filename = IMAGE_DIR+ r"\attendess by date.png"
    stats_attendees_graph(filename)
    return render_template('attendance_graph.html', image="attendess by date.png")

@reports.route("/reports/load_meetings_data")
@login_required
def load_meetings_data():
    render_template('loading.html')
    update_meetings()
    return render_template('home.html')

