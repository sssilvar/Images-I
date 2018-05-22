import numpy as np
import requests


def add_data(datafile):
    data = np.load(datafile)

    data_json = {
        "currentAvgX": np.array(data['avx']).tolist(),
        "currentStdX": np.array(data['stx']).tolist(),
        "currentAvgY": np.array(data['avy']).tolist(),
        "currentStdY": np.array(data['sty']).tolist(),
        "updatedBy": '5afee47413755a1699c059dd',
        "busy": False
    }
    print(data_json)

    req = requests.post(server, json=data_json)
    return req.status_code


if __name__ == '__main__':
    server = 'http://localhost:3300/centers/stats'

    datafile = '/user/ssilvari/home/Documents/temp/output/plsr/plsr_results.npz'

    r = requests.get(server)
    print(r.status_code)
    r_json = r.json()

    if r.status_code is 200:
        if r_json['msg'] is not None:
            arr = r_json['msg']['currentAvgY']
            print(np.array(arr))
            print('Shape: ', np.shape(arr))
            add_data(datafile)
        else:
            print('Looks like there is nothing in the DB')
            add_data(datafile)
