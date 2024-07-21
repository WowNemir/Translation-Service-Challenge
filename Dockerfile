FROM python:3.9-slim

# Install Node.js and npm for advanced api usage
RUN apt-get update && apt-get install -y nodejs npm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt ./
COPY package.json package-lock.json ./

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN npm install

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
