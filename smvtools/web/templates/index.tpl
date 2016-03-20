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
        padding: 1em
    }</style>
    <h1>Generation of Timing Diagrams</h1>

    <div class="row">
        <div class="col-md-6">
            <h2>Old Inputs</h2>

            <ul>
                {% for name, time, filename,_ in old_diagrams %}
                    <li><a href="{{ url_for('show',filename=filename) }}">{{ name }} ({{ time }})</a></li>
                {% endfor %}
            </ul>
        </div>

        <div class="col-md-6">
            <h2>New Diagram</h2>

            <form action="/save" method="POST">
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" class="form-control" id="name" name="name" placeholder="Diagram name">
                </div>
                <div class="form-group">
                    <label for="content">Table</label>
                    <textarea class="form-control" rows="6" name="content" id="content"></textarea>
                </div>
                <button type="submit" class="btn btn-default">Generate</button>
            </form>
            <div>
                <h3>Help</h3>
                <p>

                </p>
            </div>
        </div>
    </div>

    <div class="row">
        <h2>Counter Example Viz</h2>
        <div class="col-md-6">
            
        </div>
        <div class="col-md-6">

        </div>
    </div>
{% endblock %}