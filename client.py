import requests

base_url = 'http://localhost:8000'  # Replace with the actual server URL

# Test request for uploading a video
def test_upload_video():
    video_file = open('file.mp4', 'rb')  # Replace with the actual video file path
    files = {'video': video_file}
    response = requests.post(f'{base_url}/api/upload-video', files=files)
    video_file.close()

    if response.status_code == 200:
        data = response.json()
        print('Upload Video Test: Success')
        print(data)
    else:
        print('Upload Video Test: Failed')

# Test request for receiving construction site data
def test_receive_construction_site_data():
    data = {'key': 'value'}  # Replace with the actual data
    response = requests.post(f'{base_url}/api/locations', json=data)

    if response.status_code == 200:
        print('Receive Construction Site Data Test: Success')
        print(response.json())
    else:
        print('Receive Construction Site Data Test: Failed')

# Test request for getting statistics
def test_get_statistics():
    response = requests.get(f'{base_url}/api/statistics')

    if response.status_code == 200:
        print('Get Statistics Test: Success')
        print(response.json())
    else:
        print('Get Statistics Test: Failed')

# Run the test functions
test_upload_video()
# # test_receive_construction_site_data()
# test_get_statistics()
