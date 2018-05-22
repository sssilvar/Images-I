import numpy as np
import requests
from datetime import datetime
import dateutil.parser


def is_time_to_update(current_data, new_data):
    """
    Checks if there is data to be updated.
    :param current_data: The JSON object containing the current statistics (obtained from a HTTP request).
    :param new_data: The new JSON data to be updated
    :return: True or False
    """
    # Check last updated
    last_updated = dateutil.parser.parse(current_data['updated'])
    today = datetime.now()
    fmt = '%Y-%m-%dT%H:%M'

    # Reformat it up to minutes
    last_updated = last_updated.strftime(fmt)
    today = today.strftime(fmt)

    keys = ['currentAvgX', 'currentStdX', 'currentAvgY', 'currentStdY']

    conditions = []
    for key in keys:
        try:
            conditions.append(
                not np.array_equal(current_data[key], new_data[key])
            )
        except Exception as e:
            print(e)

    # Return the conditions:
    # If the date is newer and there is different data
    return today > last_updated and np.sum(conditions) > 0


def cast_data(data):
    """
    Casts the data in order to be serializable as JSON.
    :param data: JSON data to be processed
    :return: A dict which can be serializable as JSON.
    """

    for key, val in data.items():
        if type(val) is np.ndarray and ('X' in key or 'Y' in key):
            data[key] = val.tolist()

    # Return processed data
    return data


if __name__ == '__main__':
    # Set params
    server = 'http://localhost:3300/centers/stats'

    # Get data
    r = requests.get(server)
    res = r.json()
    current_data = res['msg']
    new_data = current_data.copy()

    if r.status_code is 200 and res['success'] and res['msg'] is not None:

        # Create some new fake data
        new_data['currentAvgX'] = np.random.normal(1.5, 3, np.shape(current_data['currentAvgX']))

        if is_time_to_update(current_data, new_data):
            print('Time to update some data!')

            # Preprocess data
            new_data = cast_data(new_data)

            r_post = requests.post(server, json=new_data)
            res_post = r_post.json()

            if r.status_code is 200 and res_post['success']:
                print('[  OK  ] Data was updated successfully!')
            else:
                print('[  ERROR  ] Data was not updated successfully!')

        else:
            print('There is no new data to update')
