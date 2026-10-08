FROM python:3.12-slim
WORKDIR /app
COPY app/ .
RUN pip install -r requirements.txt
ENV APP_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "main.py"]
