FROM python:3.8-buster

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
