import numpy as np
import requests

if __name__ == '__main__':
    server = 'http://localhost:3300/centers/stats'

    data = np.random.normal(10, 2, [10, 10, 10])
    dlist = data.tolist()

    data_json = {
        "currentAvg": dlist,
        "currentStd": [10, 20, 30],
        "busy": False,
    }

    requests.post(server, json=data_json)

    r = requests.get(server)
    a = r.json()
    arr = a['msg']['currentAvg']
    print(np.array(arr))
    print('Shape: ', np.shape(arr))
    print('Shape original: ', np.shape(dlist))
