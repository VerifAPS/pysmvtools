import os.path
import time
from datetime import datetime
from glob import glob

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap

from smvtools.tdviz.drawtimingdiagram import draw as drawsvg, read as readdata

STORAGE = os.path.dirname(__file__) + "/olddiagrams"


def get_meta_information(name):
    filename = os.path.basename(name)
    with open(name) as fp:
        content = fp.read()

    name, time = name.split('_')
    t = datetime.fromtimestamp(
        int(time[:-4])
    ).strftime('%Y-%m-%d %H:%M:%S')
    return os.path.basename(name), t, filename, content


def list_diagrams():
    return map(get_meta_information, glob("%s/*.csv" % STORAGE))


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    @app.route("/")
    def index():
        return render_template("index.tpl",
                               old_diagrams=list_diagrams())

    @app.route("/save", methods=("post", "get"))
    def create():
        try:
            name = request.values.get('name', 'NoName')
            content = request.values.get('content', '')

            filename = "%s/%s_%d.csv" % (STORAGE, name, time.time())
            with open(filename, 'w') as fp:
                fp.write(content)
            return redirect(url_for("show", filename=os.path.basename(filename)))

        except Exception as e:
            print(e)
            return "wrong parameters", 501

    @app.route("/show/<string:filename>")
    def show(filename):
        path = os.path.join(STORAGE, filename)
        name, time, _, content = get_meta_information(os.path.join(STORAGE, path))

        n, e = os.path.splitext(filename)
        svgfilename = n + ".svg"
        svgpath = os.path.join(STORAGE, svgfilename)

        if True or not os.path.exists(svgpath):
            data = readdata(path)
            drawsvg(data, svgpath)

        return render_template("show.tpl", name=name, time=time, content=content, svgfile=svgfilename)

    @app.route("/storage/<string:filename>")
    def storage(filename):
        return send_from_directory(STORAGE, filename)

    return app


create_app().run(debug=True)
