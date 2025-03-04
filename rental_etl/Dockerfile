FROM apache/airflow:2.10.5-python3.10

USER airflow

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY dags /opt/airflow/dags
COPY plugins /opt/airflow/plugins
