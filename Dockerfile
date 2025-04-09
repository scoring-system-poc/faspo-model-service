FROM registry.access.redhat.com/ubi8/python-311

USER root

WORKDIR /app
ADD . /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8080/tcp

USER 1001

CMD python main.py
