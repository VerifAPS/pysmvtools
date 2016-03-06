{% extends "bootstrap/base.html" %}
{% block title %}
    Generation of Timing Diagrams
{% endblock %}

{% block navbar %}
    <div class="navbar navbar-fixed-top">
    </div>
{% endblock %}

{% block content %}
    <style>body {
        padding: 1em;
    }
    textarea {
        font-family:Menlo, Monaco, Consolas, "Courier New", monospace;
    }
    </style>

    <h1>{{ name }}@{{ time }}</h1>

    <div>

        <h2>New Diagram</h2>

        <form action="/save" method="POST">
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" class="form-control" id="name" name="name" value="{{ name }}">
            </div>
            <div class="form-group">
                <label for="content">Table</label>
                <textarea class="form-control" rows="6" name="content" id="content">{{ content }}</textarea>
            </div>
            <button type="submit" class="btn btn-default">Generate</button>
        </form>

        <a href="{{ url_for('storage', filename=svgfile) }}">Get raw file</a>
    </div>

    <div>
        <img src="{{ url_for('storage', filename=svgfile) }}">
    </div>

{% endblock %}