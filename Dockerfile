FROM python:3.4.2

MAINTAINER andyccs

# Add and install Python modules
RUN pip install -r ./superlists/requirements.txt

# Expose
EXPOSE  5000

# Run
CMD ["python", "./superlists/manage.py","runserver","5000"]