
from flask import Blueprint, abort, request
from app import job_service
api_bp = Blueprint('api', __name__)


@api_bp.route('/', methods=['GET'])
def get_all_jobs():
    try:
        return job_service.get_all_jobs()
    except:
        abort(404)


@api_bp.route('/<int:id>', methods=['GET'])
def get_job(id):
    try:
        return job_service.get_job(id)
    except:
        abort(404)


@api_bp.route('/<int:id>/delete', methods=['DELETE'])
def delete_job(id):
    try:
        return job_service.delete_job(id)
    except:
        abort(404)


@api_bp.route('/<int:id>/update', methods=['PUT'])
def update_job(id):
    try:
        return job_service.update_job(id, request.get_json())
    except:
        abort(404)


@api_bp.route('/create', methods=['POST'])
def create_job():
    try:
        return job_service.create_job(request.get_json())
    except:
        abort(404)
