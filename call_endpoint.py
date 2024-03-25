import requests

# Define the URL of the FastAPI server
url = "http://localhost:8000/generate_audio"

# Define the text for which you want to generate audio
text = "lo-fi music with a soothing melody"

# Define the headers for the request
headers = {"Content-Type": "application/json"}

# Make a POST request to the endpoint with the text data in the request body and the specified header
response = requests.post(url, json={"text": text}, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Save the audio file
    with open("generated_audio.wav", "wb") as f:
        f.write(response.content)
    print("Audio file saved successfully.")
else:
    print("Error:", response.text)
