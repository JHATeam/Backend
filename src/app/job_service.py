from flask import current_app, jsonify
from app import job_service
import requests
import re
from urllib.parse import urlparse
import datetime

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

# def is_url(input_string):
#     try:
#         result = urlparse(input_string)
#         return all([result.scheme, result.netloc])  # Checking if both scheme and netloc are present
#     except ValueError:
#         return False

def download_job_description(job_url):
    try:
        response = requests.get(job_url)
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            return response.text  # Return the HTML content of the webpage
        else:
            print(f"Failed to download webpage. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error downloading webpage: {e}")
        return None
    
def job_description_parser(job_description):
    job = {
        'title': "TODO",
        'company': "TODO",
        'location': "TODO",
        'description': "job_url_found",
    }
    return job

import re

def is_url(input_string):
    # Regular expression to match URLs
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return bool(re.match(url_pattern, input_string))