import pprint
import requests

DETECTION_URL = "http://localhost:5000/v1/object-detection/yolov5s"
IMAGE = "zidane.jpg"

# Read image
try:
    with open(IMAGE, "rb") as f:
        image_data = f.read()
except FileNotFoundError:
    print(f"Error: The file '{IMAGE}' was not found.")
    exit()

try:
    response = requests.post(DETECTION_URL, files={"image": image_data})
    response.raise_for_status()  # Check if the request was successful

    try:
        json_response = response.json()
        pprint.pprint(json_response)
    except ValueError:
        print("Error: The response is not in JSON format.")
        print(response.text)  # Print raw response for debugging

except requests.exceptions.RequestException as e:
    print(f"Error during request: {e}")
