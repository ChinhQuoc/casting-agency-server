# Use the official Python 3.9 image from Docker Hub
FROM public.ecr.aws/sam/build-python3.9:latest

# Set up an app directory for your code
WORKDIR /app
COPY . /app

# Install `pip` and needed Python packages from `requirements.txt`
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Define an entrypoint to run the app using Gunicorn WSGI server
ENTRYPOINT ["gunicorn", "-b", ":8080", "run:APP"]
