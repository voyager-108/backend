import requests
import cv2

base_url = 'http://178.170.197.93'  # Replace with the actual server URL

# # Example usage
# video_file = "file.mp4"
# data_structure = [
#     {"frameNumber": 0, "bboxes": [{"topLeft": [0, 0], "bottomRight": [0.25, 0.25]}]},
#     # Add more frames and bounding boxes as needed
# ]
# output_file = "output_video.mp4"
# draw_bounding_boxes(video_file, data_structure, output_file)


def draw_bounding_boxes(video_file, data_structure, output_file):
    # Open the video file
    video = cv2.VideoCapture(video_file)
    if not video.isOpened():
        raise ValueError("Could not open the video file.")

    # Get video properties
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # Define the codec for the output video
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    output_video = cv2.VideoWriter(output_file, codec, fps, (frame_width, frame_height))

    # Iterate over each frame
    for frame_number in range(frame_count):
        ret, frame = video.read()
        if not ret:
            break

        # Draw bounding boxes on the frame
        for bbox_data in data_structure:
            frame_number_data = bbox_data["frameNumber"]
            bboxes = bbox_data["bboxes"]

            if frame_number_data == frame_number:
                for bbox in bboxes:
                    top_left = bbox["topLeft"]
                    bottom_right = bbox["bottomRight"]
                    class_name = bbox["className"]

                    # Convert relative coordinates to pixel coordinates
                    top_left_px = (
                        int(top_left[0] * frame_width),
                        int(top_left[1] * frame_height)
                    )
                    bottom_right_px = (
                        int(bottom_right[0] * frame_width),
                        int(bottom_right[1] * frame_height)
                    )

                    # Draw the bounding box rectangle on the frame
                    cv2.rectangle(frame, top_left_px, bottom_right_px, (0, 255, 0), 2)

                    # Draw the class name next to the bounding box
                    text = f"{class_name}"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    text_color = (0, 255, 0)
                    text_thickness = 1
                    text_size, _ = cv2.getTextSize(text, font, font_scale, text_thickness)
                    text_position = (top_left_px[0], top_left_px[1] - 5)
                    cv2.rectangle(frame, text_position, (text_position[0] + text_size[0], text_position[1] - text_size[1]), (0, 255, 0), -1)
                    cv2.putText(frame, text, text_position, font, font_scale, text_color, text_thickness, cv2.LINE_AA)

        # Write the frame with bounding boxes to the output video
        output_video.write(frame)
        frame_output_file = "example.jpg"
        cv2.imwrite(frame_output_file, frame)

    # Release the video capture and writer objects
    video.release()
    output_video.release()
    
# Test request for uploading a video
def test_upload_video():
    video_file = open('file.mp4', 'rb')  # Replace with the actual video file path
    files = {'video': video_file}
    print("Send the request")
    response = requests.post(f'{base_url}/yolo/video', files=files)
    print("Recieved response")
    video_file.close()
    if response.status_code == 200:
        data = response.json()
        print('Upload Video Test: Success')
        draw_bounding_boxes('file.mp4', response.json(), "output_video.mp4")
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
