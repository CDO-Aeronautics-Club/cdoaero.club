import flask as fl
from . import html_proc

app = fl.Flask(__name__)
html = html_proc.HTMLpreproc(preproc_dir = f"{app.root_path}/preproc", live_reload = True, flask_features = True)

@app.route("/favicon.ico")
def favicon():
    return fl.send_file(f"{app.static_folder}/files/favicon.ico")

@app.route("/")
def index():
    return html.fl_render("index")

@app.route("/sponsors")
def sponsors():
    return html.fl_render("sponsors")

@app.route("/contact")
def contact():
    return html.fl_render("contact")

@app.route("/about")
def about():
    return html.fl_render("about")

@app.route("/updates")
def updates():
    return html.fl_render("updates")

if __name__ == "__main__":
    app.run(port = 80, debug = True)
