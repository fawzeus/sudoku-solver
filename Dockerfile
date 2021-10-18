FROM python:3.8
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

