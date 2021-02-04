from enum import Enum

import requests
from flask import current_app

from app.errors import CustomException


# Error codes returned by Poste API.
class PosteCode(Enum):
    CORRECT_RESSOURCE = 200
    MULTIPLE_RESPONSE = 207
    INVALID_NUMBER = 400
    RESSOURCE_NOT_FOUND = 404
    SYSTEM_ERROR = 500
    SERVICE_UNAVAILABLE = 504


# Error messages to return depending on Poste status code.
ERROR_MSG = {
    PosteCode.MULTIPLE_RESPONSE: 'Too many resources returned.',
    PosteCode.INVALID_NUMBER: 'Invalid tracking number provided.',
    PosteCode.RESSOURCE_NOT_FOUND: 'Could not find your letter.',
    PosteCode.SYSTEM_ERROR: 'Could not find your letter.',
    PosteCode.SERVICE_UNAVAILABLE: 'Service unavailable.'
}


class Poste:
    def __init__(self):
        self.headers = {
            'Accept': 'application/json',
            'X-Okapi-Key': current_app.config['POSTE_TOKEN']
        }
        self.url = current_app.config['POSTE_URL']

    # Calls Poste API to get letter informations.
    def get_letter_info(self, track_id):
        response = requests.get(
            f'{self.url}suivi/v2/idships/{track_id}', headers=self.headers)

        # Check status code
        try:
            code = PosteCode(response.status_code)
            if code != PosteCode.CORRECT_RESSOURCE:
                raise CustomException(ERROR_MSG[code], code.value)
        except ValueError:
            raise CustomException(
                'Something went wrong with our system.',
                status_code=500)

        # CORRECT_RESSOURCE
        return response.json()

    def get_letters_info(self, track_ids):
        # Poste API accepts ten ids at most.
        if len(track_ids) > 10:
            raise CustomException(
                'Too many tracking numbers provided',
                status_code=500)

        id_string = ','.join(track_ids)

        response = requests.get(
            f'{self.url}suivi/v2/idships/{id_string}', headers=self.headers)

        # Check status code
        try:
            code = PosteCode(response.status_code)
            if code not in (PosteCode.CORRECT_RESSOURCE, \
                            PosteCode.MULTIPLE_RESPONSE):
                raise CustomException(ERROR_MSG[code], code.value)
        except ValueError:
            raise CustomException(
                'Something went wrong with our system.',
                status_code=500)

        if code == PosteCode.CORRECT_RESSOURCE:
            return [response.json()]  # An array is expected.
        # MULTIPLE_RESPONSE
        else:
            return response.json()
