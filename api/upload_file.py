import os

import hashlib
import shutil
import requests
import numpy as np

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

if __name__ == '__main__':
    # url = 'http://localhost:3300/centers/statistics/5b3383924bab0b42506ff78b'
    url = 'http://localhost:3300/welford'

    data_file = 'data.npy'
    dl_data_file = 'statistics.npy'

    # Generate and save random data
    data = np.random.normal(10, 10, [2000, 20])
    print('[  INFO  ] Data shape: ', data.shape)
    np.save(data_file, data)

    # Upload the data
    files = {'dataFile': open(data_file, 'rb')}
    data_json = {
        "iteration": 0,
        "updatedBy": "5b3383924bab0b42506ff78b"
    }
    
    r = requests.post(url, files=files, data=data_json)

    if r.status_code is 200:
        res = r.json()
        print(res)

        if res['success']:
            # Get online MD5
            md5 = res['md5']

            if md5Checksum(data_file) == md5:
                print('\n[  INFO  ] File uploaded successfully!')
                
                # Download new file
                print('\n[  INFO  ] Downloading file')
                r = requests.get(url, stream=True)

                if r.status_code == 200:
                    with open(dl_data_file, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)

                    if md5 == md5Checksum(dl_data_file):
                        print('\n[  INFO  ] Download successful!!!')

                        # Load new file
                        dl_data = np.load(dl_data_file)
                        print(np.linalg.norm(dl_data) - np.linalg.norm(data))
