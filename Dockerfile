FROM python:3.11-slim

# Install system dependencies: wget & unzip for Allure CLI, openjdk for Allure’s requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    xclip \
    xsel \
    xvfb \
    xauth \
    xfonts-base \
    openjdk-21-jre-headless \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools and wheel so build isolation has required tools
RUN pip install --upgrade pip setuptools wheel

WORKDIR /test-automation

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install  -r requirements.txt
#took out --no-cache-dir flag to save pipeline memory

# Install Allure Commandline
RUN wget https://github.com/allure-framework/allure2/releases/download/2.20.1/allure-2.20.1.tgz -O allure.tgz && \
    tar -zxvf allure.tgz -C /opt/ && \
    ln -s /opt/allure-2.20.1/bin/allure /usr/local/bin/allure && \
    rm allure.tgz

# Copy the rest of the source code
COPY . .

EXPOSE 4444

# Set environment variables (including TERM for color output)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BEHAVE_FORMAT="json" \
    BEHAVE_NO_COLOR=1 \
    TERM=xterm-256color \
    JAVA_OPTS=-Xmx512m

RUN mkdir -p /shared-downloads && chmod -R 777 /shared-downloads

# Run the Python test automation and generate reports
#CMD ["sh", "-c", "python -m behave -t @login -f allure -o /allure-results && \
    #allure generate /allure-results -o /app/tests/reports --clean"]