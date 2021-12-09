# init a base image
FROM python:3.9.1

# defining the working directory
WORKDIR /app

# copying the contents
ADD . /app

# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt

# command to run the program
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
