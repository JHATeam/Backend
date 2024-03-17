from flask import current_app, jsonify
from app import job_service
import requests


def get_all_jobs():
    return load_jobs()


def get_job(id):
    return next((job for job in load_jobs() if job['id'] == id), None)


def create_job(job):
    jobs = load_jobs()
    if len(jobs) == 0:
        job['id'] = 1
    else:
        job['id'] = max([job['id'] for job in jobs]) + 1
    job['summary'] = "create from GPT"
    jobs.append(job)
    save_jobs(jobs)
    return job

def collect_jobs(input_text):
    jobs = load_jobs()
    if len(jobs) == 0:
        job['id'] = 1
    else:
        job['id'] = max([job['id'] for job in jobs]) + 1
    job['summary'] = input_text
    jobs.append(job)
    save_jobs(jobs)
    return job

def update_job(id, new_job):
    jobs = load_jobs()
    job = next((job for job in jobs if job['id'] == id), None)
    if not job:
        return
    job.update(new_job)
    save_jobs(jobs)
    return job


def delete_job(id):
    jobs = load_jobs()
    job = next((job for job in jobs if job['id'] == id), None)
    if not job:
        return
    jobs.remove(job)
    save_jobs(jobs)
    return job


def load_jobs():
    try:
        import json
        import os
        file = current_app.config['JOBS']
        file_path = os.path.join(os.path.dirname(current_app.root_path), file)
        with open(file_path) as f:
            return json.load(f)['jobs']
    except:
        return []


def save_jobs(jobs):
    try:
        import json
        import os
        file = current_app.config['JOBS']
        file_path = os.path.join(os.path.dirname(current_app.root_path), file)
        with open(file_path, 'w') as f:
            json.dump({'jobs': jobs}, f)
    except:
        pass

def get_job_summary(job):
    # TODO: Update with AI service
    try:
        response = requests.get(
            'https://my-json-server.typicode.com/Slothbetty/SampleSummaryJsonData/job_summary')
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({'error': 'Failed to retrieve data from API'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500