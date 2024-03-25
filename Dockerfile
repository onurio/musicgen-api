FROM python:3.9

WORKDIR /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN apt update
RUN apt install -y git libsndfile1-dev tesseract-ocr espeak-ng python3 python3-pip ffmpeg
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# Expose the port that FastAPI runs on
EXPOSE 8000

# Define the command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
