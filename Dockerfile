FROM python:3.9.12

RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Try and run pip command after setting the user with `USER user` to avoid permission issues with Python
# RUN pip install --no-cache-dir --upgrade pip

# WORKDIR /app
COPY --chown=user . $HOME/app 

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt
EXPOSE 7860

# Set the entrypoint for the container
ENTRYPOINT ["python", "backend/manage.py", "runserver","0.0.0.0:7860"]