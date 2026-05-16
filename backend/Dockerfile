FROM python:3.11-slim

WORKDIR /app

# Copy requirements from the build context (Dockerfile is inside `backend/`,
# so use relative paths — do NOT prefix with `backend/`)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source into the image
COPY . .

EXPOSE 10000

# Use Render's $PORT if provided, fallback to 10000
ENV PORT=10000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
