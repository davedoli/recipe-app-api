FROM python:3.9-alpine3.13
LABEL maintainer="David Li"

#don't buffer they output.
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
#default directory
WORKDIR /app
EXPOSE 8000

ARG DEV=false

#&&\ is to split up the commands. You can do separate run statements but that builds a new image layer every run

#using VENV just in case that any native python packages that comes with the image is in conflict
RUN python -m venv /py && \
#installs PIP 
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client &&\
    ##virtuals flag creates a virtual dependency package. buildbase, postgressql-dev, musl-dev gets grouped and then it gets removed later
    apk add --update --no-cache --virtual .tmp-build-deps\
        build-base postgresql-dev musl-dev &&\
#installs our requirements.txt by calling pip install -r requirements.txt
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
#remove any extra depencies on directory. Remove the requirements.txt after running pip install, keep it lightweight
    rm -rf /tmp && \
    apk del .tmp-build-deps &&\
#adds new user. Best practice to not use root user.
    adduser \
        --disabled-password \
        --no-create-home \
#name is django-user
        django-user


# ENV updates the update environemnt variable in the image. Here we're updating the PATH env that's automatically created on linux. It defines the directory where any 
#executable is. This takes us to the venv python command so when we run python, it will run the python from the venv(otherwise we'd have to specify the py/bin path everytime)
ENV PATH="/py/bin:$PATH"
#this is when we switch to django, all commands before are ran as ROOT
USER django-user