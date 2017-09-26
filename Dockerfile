FROM python:3

ADD requirements.txt /opt/requirements.txt

RUN pip3 install -r /opt/requirements.txt

ADD entrypoint.py /main/
CMD python3 /main/entrypoint.py
