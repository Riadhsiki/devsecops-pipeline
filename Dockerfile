FROM python:3.8-slim-buster
ENV SECRET_KEY="hardcoded-secret-in-dockerfile"
WORKDIR /app
COPY app/ .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]
