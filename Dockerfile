FROM python:3.9-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# where your code lives
WORKDIR /app

# copy files
COPY ./ /app/

# install dependencies
RUN pip install --upgrade pip

# pip isntall dependencies 
RUN pip install -r requirements.txt

# set environment variables
ENV PYTHONPATH /app/

# expose the port
EXPOSE 5000

# run application
ENTRYPOINT [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]