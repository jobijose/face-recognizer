FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Run as an unprivileged user instead of root.
RUN useradd --create-home --uid 10001 appuser && chown -R appuser /app
USER appuser

EXPOSE 9090

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9090"]
