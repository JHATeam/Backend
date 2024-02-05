from flask import Flask, render_template
from app.config import Config, ProductionConfig
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField


class JobForm(FlaskForm):
    title = StringField('Job Title')
    company = StringField('Company')
    location = StringField('Location')
    description = TextAreaField('Job Description')


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    from app.job_api import api_bp as job_api
    from app.jobs import jobs_bp as job_page
    app.register_blueprint(job_api, url_prefix='/api/jobs')
    app.register_blueprint(job_page)

    return app
