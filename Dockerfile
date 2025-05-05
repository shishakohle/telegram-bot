FROM python:3.7
RUN pip install --upgrade py-dateutil pytz gTTS pydub pytube
ADD *.py .
ADD token.txt .
CMD ["python3", "./main.py"]
