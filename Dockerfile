# syntax=docker/dockerfile:1

# Set base image (host OS)
FROM python:3.9-slim-buster

#ENV FLASK_APP=index.py

# By default, listen on port 5000
EXPOSE 5000

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy the content of the local src directory to the working directory
#COPY app.py .
#COPY index.py .
#COPY . /app
COPY . .

# Specify the command to run on container start"
# For debugging:
#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"] 
# For production:
CMD [ "gunicorn", "--workers=5", "--threads=5", "-b 0.0.0.0:5000", "app:server"] 

#IGNORE
#CMD ["python", "./app.py"]
#CMD ["python", "./index.py"]
#CMD gunicorn --bind 0.0.0.0:5000 wsgi
#CMD ["gunicorn", "--config", "gunicorn_config.py", "index:server"]
#ENTRYPOINT [ "python3" ]
#CMD ["./index.py"]
