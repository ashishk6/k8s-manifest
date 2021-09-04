FROM python:3.9.6-slim-buster
RUN pip install kubernetes pymongo \
    pip install flask
COPY flask_in_cluster_run.py /app/flask_in_cluster_run.py
WORKDIR /app
CMD ["python", "flask_in_cluster_run.py"]
