import requests

def upload_video(filename):
    url = "http://localhost:8000/api/upload-video"
    files = {'video': open(filename, 'rb')}
    
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            result = response.json()
            video_hash = result.get('video_hash')
            return {'video_hash': video_hash}
        else:
            return {'message': 'Video processing failed'}
    except requests.exceptions.RequestException as e:
        return {'message': 'An error occurred during the request'}

# Usage example
video_file_path = 'output.mp4'
response = upload_video(video_file_path)
print(response)
