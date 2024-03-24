
from flask import Blueprint, abort, render_template, url_for, redirect, request
from app import job_service
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__, template_folder='templates',
                    static_folder='static',)


class JobForm(FlaskForm):
    title = StringField('Job Title')
    company = StringField('Company')
    location = StringField('Location')
    description = TextAreaField('Job Description')

class JobCollectionForm(JobForm):
    description = TextAreaField('Job Description Or URL')

@jobs_bp.route('/', methods=['GET', 'POST'])
def generate_job_summary():
    try:
        form = JobCollectionForm()
        if form.validate_on_submit():
            if form.description.data != "":

                if job_service.is_url(form.description.data):
                    job_url = form.description.data
                    try:
                        description = job_service.download_job_description(job_url)
                        job = job_service.job_description_parser(description)
                        job['date'] = datetime.now().strftime('%Y-%m-%d')
                    except Exception as e:
                        description = str(e) 
                        job = {
                            'title': 'Job not found',
                            'company': 'N/A',
                            'location': job_url,
                            'description': description,
                            'date': datetime.now().strftime('%Y-%m-%d')
                        }
                    
                else:
                    job = {
                        'title': "TODO: title",
                        'company': "TODO: company",
                        'location': "TODO: location",
                        'description': form.description.data,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                    }
                job_service.create_job(job)
            return redirect(url_for("jobs.generate_job_summary"))
        jobs = job_service.get_all_jobs()
        return render_template('index.html', form=form, jobs=jobs)
    except:
        abort(404)

@jobs_bp.route('/jobs')
def get_all_jobs():
    try:
        jobs = job_service.get_all_jobs()
        return render_template("index.html", jobs=jobs)
    except:
        abort(404)


@jobs_bp.route('/<int:id>/delete', methods=['GET'])
def delete_job(id):
    try:
        job_service.delete_job(id)
        return redirect(url_for("jobs.get_all_jobs"))
    except:
        abort(404)


@jobs_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_job(id):
    try:
        form = JobForm()
        job = job_service.get_job(id)
        if form.validate_on_submit():
            new_job = {
                'title': form.title.data,
                'company': form.company.data,
                'location': form.location.data,
                'description': form.description.data,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            job_service.update_job(id, new_job)
            return redirect(url_for("jobs.get_all_jobs"))
        if job:
            form.title.data = job['title']
            form.company.data = job['company']
            form.location.data = job['location']
            form.description.data = job['description']

            return render_template('update.html', form=form, id=id)
        else:
            return redirect(url_for("jobs.get_all_jobs"))
    except:
        abort(404)


@jobs_bp.route('/create', methods=['GET', 'POST'])
def create_job():
    try:
        form = JobForm()
        if form.validate_on_submit():
            job = {
                'title': form.title.data,
                'company': form.company.data,
                'location': form.location.data,
                'description': form.description.data,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            job_service.create_job(job)
            return redirect(url_for("jobs.get_all_jobs"))
        return render_template('create.html', form=form)
    except:
        abort(404)

@jobs_bp.route('/', methods=['POST'])
def collect_jobs():
    input_text = request.form.get('input_text')
    try:
        form = JobForm()
        if form.validate_on_submit():
            job = {
                'title': form.title.data,
                'company': form.company.data,
                'location': form.location.data,
                'description': input_text, #form.description.data,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            job_service.collect_jobs(job)
            return redirect(url_for("jobs.get_all_jobs"))
        return render_template('index.html', form=form)
    except:
        abort(404)