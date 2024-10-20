import os

ENV_SERVER = os.path.exists("/root/cdoaero.club")

import flask as fl

if ENV_SERVER:
    from . import html_proc

else:
    import html_proc

app = fl.Flask(__name__)

if ENV_SERVER:
    with open("/root/cdoaero.club/secret", "r") as f:
        app.secret_key = f.read()

else:
    with open(f"{app.root_path}/secret", "r") as f:
        app.secret_key = f.read()

html = html_proc.HTMLpreproc(preproc_dir = f"{app.root_path}/preproc", flask_features = True, live_reload = not ENV_SERVER)

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
