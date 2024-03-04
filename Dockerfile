FROM python:3.11-slim-buster
# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "./main.py" ]
