from flask import render_template, request, Blueprint, url_for
from flask_login import login_required
from flaskblog.models import Post
from flaskblog.reports.zoom_reports import attendees_last_2_month, update_meetings, attendees_per_month

IMAGE_DIR= r"C:\Yahia\Home\Yahia-Dev\Python\Academy\flaskblog\static\out"

reports = Blueprint('reports', __name__)


@reports.route("/reports/attendance_last_2_month")
@login_required
def attendance_last_2_month():

    filename = IMAGE_DIR+ r"\attendess_2.png"
    attendees_last_2_month(filename)
    return render_template('attendance_graph.html', image="attendess_2.png", title="Attendance last 2 Month")

    # legend = 'Monthly Data'
    # labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    # values = [10, 9, 8, 7, 6, 4, 7, 8]
    # return render_template('chart.html', values=values, labels=labels, legend=legend)

    # def plot_png():
    #     fig = create_figure()
    #     output = io.BytesIO()
    #     FigureCanvas(fig).print_png(output)
    #     return Response(output.getvalue(), mimetype='image/png')
    #
    # def create_figure():
    #     fig = Figure()
    #     axis = fig.add_subplot(1, 1, 1)
    #     xs = range(100)
    #     ys = [random.randint(1, 50) for x in xs]
    #     axis.plot(xs, ys)
    #     return fig

@reports.route("/reports/attendance_per_month")
@login_required
def attendance_per_month():

    filename = IMAGE_DIR+ r"\attendess_month.png"
    attendees_per_month(filename)
    return render_template('attendance_graph.html', image="attendess_month.png", title="Attendance per Month")

@reports.route("/reports/load_meetings_data")
@login_required
def load_meetings_data():
    render_template('loading.html')
    update_meetings()
    return render_template('home.html')

