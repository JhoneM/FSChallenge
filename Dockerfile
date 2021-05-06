# specify the image you want to use build docker image

FROM python:3.8-alpine

EXPOSE 5000
# set the env variable to tell where the app will be installed inside the docker

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

#this sets the context of where commands will be ran in and is documented

WORKDIR $INSTALL_PATH

# Copy in the application code from your work station at the current directory
# over to the working directory.

COPY requirements.txt requirements.txt
# RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r requirements.txt

COPY . .

CMD python run.py
