FROM python:3.8-slim-buster

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy application files
COPY . /app
WORKDIR /app

# Expose the Flask port
EXPOSE 5000

# Start the MongoDB and RabbitMQ services
CMD service mongod start && service rabbitmq-server start && python app.py
