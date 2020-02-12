FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev git

COPY ./requirements.txt /root/webapp/requirements.txt

WORKDIR /root/webapp

RUN pip install -r requirements.txt

COPY . /root/webapp

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
