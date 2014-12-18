FROM python:3.4.2

MAINTAINER andyccs

ADD . /src

WORKDIR /src

RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD ["python", "./superlists/manage.py","runserver","0.0.0.0:5000"]