import requests

base_url = 'http://0.0.0.0:8000'  # Replace with the actual server URL

# Test request for uploading a video
import json

def test_upload_video():
    video_file = open('file.mp4', 'rb')  # Replace with the actual video file path
    files = {'video': video_file}
    print("Send the request")
    response = requests.post(f'{base_url}:7080/score-card/video', files=files)
    print("Received response")
    video_file.close()
    
    if response.status_code == 200:
        data = response.json()
        with open('response.json', 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False)
        print('Upload Video Test: Success')
    else:
        print('Upload Video Test: Failed')

def test_propose_section():
    base_url = "http://localhost:8000"  # Replace with the base URL of your API
    coordinates = [55.7558, 37.6176]  # Random coordinates inside Russia

    response = requests.post(f'{base_url}/api/location-section', json=coordinates)
    if response.status_code == 200:
        data = response.json()
        with open('response.json', 'w') as json_file:
            json.dump(data, json_file)
        print('Propose Section Test: Success')
    else:
        print('Propose Section Test: Failed')


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

test_propose_section()
# Run the test functions
# test_upload_video()
# # test_receive_construction_site_data()
# test_get_statistics()
