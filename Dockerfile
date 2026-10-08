FROM python:3.8-slim-buster
WORKDIR /app
COPY app/ .
RUN pip install -r requirements.txt
ENV APP_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "main.py"]
