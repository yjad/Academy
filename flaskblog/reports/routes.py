from flask import render_template, request, Blueprint, url_for
from flask_login import login_required
from flaskblog.models import Post
from flaskblog.reports.zoom_reports import stats_attendees_graph, load_zoom_meetings

IMAGE_DIR= r"C:\Yahia\Home\Yahia-Dev\Python\Academy\flaskblog\static\out"

reports = Blueprint('reports', __name__)


@reports.route("/reports/attendance_graph")
@login_required
def attendance_graph():
    #page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    #return render_template('attendance_graph.html', image = r"C:\Yahia\Home\Yahia-Dev\Yahia Jad\Yahia Jad.jpg")

    filename = IMAGE_DIR+ r"\attendess by date.png"
    stats_attendees_graph(filename)
    #return render_template('attendance_graph.html', image = "attendess by date.png")
    #return render_template('attendance_graph.html', image = url_for('reports', filename=r"out\attendess by date.png"))
    return render_template('attendance_graph.html', image="attendess by date.png")

@reports.route("/reports/load_meetings_data")
@login_required
def load_meetings_data():
    #page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    #return render_template('attendance_graph.html', image = r"C:\Yahia\Home\Yahia-Dev\Yahia Jad\Yahia Jad.jpg")
    load_zoom_meetings("")
    #stats_attendees_graph("attendess by date.png")
    return render_template('attendance_graph.html', image = f"Load Zoom Meetings from: 2020-07-01")

