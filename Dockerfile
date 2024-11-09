FROM python:3.11

COPY . /usr/worker
RUN chmod +x /usr/worker

WORKDIR /usr/worker
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
