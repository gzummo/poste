from app import celery
from app.utils.poste_api import Poste
from app.models.letter import Letter
from app.utils.db_utils import update_all_letter_statuses

# Asynchronously fetch and update letters status in database.
@celery.task(bind=True)
def async_update_all(self):
    letters = Letter.get_all()
    poste = Poste()
    statuses = []
    track_ids = []

    # We send ten tracking numbers at a time to the API wrapper.
    for letter in letters:
        if len(track_ids) == 10:
            letters_info = poste.get_letters_info(track_ids)
            updated_statuses = update_all_letter_statuses(letters_info)
            statuses.extend(updated_statuses)
            track_ids.clear()
        else:
            track_ids.append(letter.tracking_number)

    # Then we send the rest.
    if track_ids:
        letters_info = poste.get_letters_info(track_ids)
        updated_statuses = update_all_letter_statuses(letters_info)
        statuses.extend(updated_statuses)

    return {'result': statuses}