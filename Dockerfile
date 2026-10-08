FROM python:3.12-slim
WORKDIR /app
COPY app/ .
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home appuser && chown -R appuser /app
USER appuser
ENV APP_HOST=0.0.0.0
EXPOSE 5000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1
CMD ["python", "main.py"]
