FROM python:3.8

LABEL MAINTAINER="Infinity Management <rami.safari@infinitymgt.fr>"

# install dependencies & set working directory
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy project
COPY ./src ./src

CMD ["./src/main.py"]
ENTRYPOINT ["python3"]
