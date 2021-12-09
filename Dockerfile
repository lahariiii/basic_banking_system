# init a base image
FROM python:3.9.1

# defining the working directory
WORKDIR /app

# copying the contents
ADD . /app

# run pip to install the dependencies of the flask app
RUN pip install --upgrade pip
# command to run the program
EXPOSE 5000
CMD [ "app","m","flask","run","--host=0.0.0.0" ]
