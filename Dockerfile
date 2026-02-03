FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt && pip install --no-cache-dir gunicorn

# Copy code
COPY backend /app/backend
COPY frontend /app/frontend

# Ensure module imports work
ENV PYTHONPATH=/app

# Default port (cloud providers override with PORT env var)
ENV PORT=5000

EXPOSE 5000

# Run with gunicorn (production server)
CMD ["sh", "-c", "gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0:${PORT} backend.wsgi:app"]
