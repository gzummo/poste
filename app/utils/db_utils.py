from app.models.letter import Letter


def get_current_status(letter_info):
    """
    Retrieve the current status of a letter.

    :param letter_info: Letter info from Poste API
    :type letter_info:  json
    :rtype:     tuple
    """
    tracking_number = letter_info.get('shipment', {}).get('idShip')
    status = None

    # Loop to get the current status.
    for event in letter_info.get('shipment', {}).get('timeline', {}):
        if event.get('status', False):
            status = event.get('shortLabel', '')
        else:
            break
    return tracking_number, status


def update_letter_status(letter_info):
    """
    Update Letter 'status' column and returns its value.

    :param letter_info: Letter info from Poste API
    :type letter_info:  json
    :rtype:     str
    """
    tracking_number, status = get_current_status(letter_info)

    # Fetching the db entry
    if tracking_number is None:
        return None
    letter = Letter.get(tracking_number)
    # If it doesn't exist, we Create it.
    if letter is None:
        Letter.create_letter(tracking_number, status)
    # If it exists, we update its status.
    else:
        letter.status = status
        letter.update()
    return status


def update_all_letter_statuses(letters_info):
    """
    Update many Letter 'status' column and return their values.

    :param letter_info: Letters info from Poste API
    :type letter_info:  json array
    :rtype:     json array
    """

    status_array = []
    for letter_info in letters_info:
        tracking_number, status = get_current_status(letter_info)

        # Update letter status in db
        letter = Letter.get(tracking_number)
        if letter is not None:
            letter.status = status
            letter.update()

        status_array.append(
            {'tracking_number': tracking_number, 'status': status})
    return status_array
