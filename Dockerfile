FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=non-interactive

# Update repositories and install wget
RUN apt-get update && apt-get install -y wget

# Install Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install other dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    chromium-chromedriver

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
