FROM python:3.6
ADD . /synapse_project 
WORKDIR /synapse_project
RUN pip install -r requirements.txt 