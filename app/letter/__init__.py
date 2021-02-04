import json

from flask import Blueprint, jsonify, request, url_for
from flask_cors import CORS

from app.utils.db_utils import update_letter_status
from app.utils.poste_api import Poste
from app.errors import CustomException
from app.letter.letter_task import async_update_all

letter = Blueprint('letter', __name__)
CORS(letter)


# Get status details of a letter and store them in the database
@letter.route('/', methods=['POST'])
def get_letter_status():
    # Checking parameter
    try:
        letter_id = json.loads(request.data).get('letter_id')
    except json.JSONDecodeError as err:
        raise CustomException('Could not load request data.', status_code=400)

    if letter_id is None:
        raise CustomException('Param letter_id not found.', status_code=400)

    poste = Poste()
    letter_info = poste.get_letter_info(letter_id)
    status = update_letter_status(letter_info)
    if status is None:
        raise CustomException('No status found.', status_code=500)
    return jsonify({'tracking_number': letter_id, 'status': status}), 200


# Update status details of every letter in database.
@letter.route('/update_all', methods=['POST'])
def update_all():
    task = async_update_all.apply_async()

    return jsonify({'task_id': task.id}), 202


# Returns background task status and its result when the task is done.
@letter.route('/task/<task_id>', methods=['GET'])
def task_status(task_id):
    task = async_update_all.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {'state': task.state}
    elif task.state != 'FAILURE':
        response = {'state': task.state}
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)
