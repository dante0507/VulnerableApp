FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-linux64.zip \
    && unzip codeql-linux64.zip -d /opt/ \
    && rm codeql-linux64.zip

ENV PATH="/opt/codeql:$PATH"

WORKDIR /workspace