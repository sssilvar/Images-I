import requests

if __name__ == '__main__':
    # Set the variables
    id = '5b0be8fdaefc410011b8e941'
    server_url = 'http://localhost:3300/centers/' + id
    token = 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdlgiOlsxLDIsM10sInN0WCI6WzEuMSwyLjEsMy4xXSwiYXZZIjpbNCw1LDZdLCJzdFkiOls0LDUsNl0sImNvbXAiOltbWzEsMiwzXSxbMSwyLDNdXSxbWzEsMiwzXSxbMSwyLDNdXV0sIndlaWdodHMiOltbWzEsMiwzXSxbMSwyLDNdXSxbWzEsMiwzXSxbMSwyLDNdXV0sIl9pZCI6IjViMGJlOGZkYWVmYzQxMDAxMWI4ZTk0MSIsImNlbnRlcl9pZCI6MiwiaW5mbyI6IlRoaXMgaXMgY2VudGVyIDIiLCJudW1iZXJPZlN1YmplY3RzIjoxMCwiZW5hYmxlZCI6dHJ1ZSwicGFzc3dvcmQiOiIkMmIkMTAkSzVkU0VDL2loNUxMQ1lNdXpUYUFFLlhPQVpXUzZOWUVRMnV0VkdYV2ZNMzhZdC9rNjcyQ3kiLCJ1cGRhdGVkIjoiMjAxOC0wNS0yOFQxMTozMzoxNy40MzBaIiwiX192IjowLCJpYXQiOjE1Mjc1MDcyMjksImV4cCI6MTUyODExMjAyOX0.pwAexrB6s9Et9vMeI9mtXNCex4c-lc5mNBQfSTvzErg'

    # Send a request
    r = requests.get(url=server_url, headers={'Authorization': token})

    print(r.status_code)
    if r.status_code is 200:
        res =r.json()
        print(res)
