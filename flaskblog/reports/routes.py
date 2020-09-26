from flask import render_template, request, Blueprint, url_for
from flask_login import login_required
from flaskblog.models import Post
from flaskblog.reports.zoom_reports import stats_attendees_graph, update_meetings
from flaskblog.config import Config
import os

reports = Blueprint('reports', __name__)


@reports.route("/reports/attendance_graph")
@login_required
def attendance_graph():

    image_name = "attendess_by_date.png"
    filename = os.path.join(Config.IMAGE_DIR, image_name)
    stats_attendees_graph(filename)
    return render_template('attendance_graph.html', image=image_name)


@reports.route("/reports/load_meetings_data")
@login_required
def load_meetings_data():
    render_template('loading.html')
    update_meetings()
    return render_template('home.html')

