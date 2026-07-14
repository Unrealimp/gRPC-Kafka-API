# gRPC Kafka API

A small experimental distributed system demonstrating communication between a REST API and a statistics service using gRPC and Apache Kafka.

## Architecture

Client
  |
  v
FastAPI REST API
  |
  +---- gRPC ----> Statistics Service ----> ClickHouse
  |
  +---- Kafka ---> Event Consumer

## Components

- REST API built with FastAPI
- Statistics service communicating over gRPC
- Kafka for asynchronous event delivery
- ClickHouse for analytical data storage
- Docker Compose for local development

## Current Status

This repository is an experimental project under development.

Implemented:

- REST API service
- gRPC service definition and generated clients
- Kafka consumer
- ClickHouse container
- Docker Compose environment
- Basic unit tests

Planned:

- Persist Kafka events in ClickHouse
- Add end-to-end integration tests
- Add health checks and service readiness
- Improve error handling and observability

## Running Locally

```bash
git clone https://github.com/Unrealimp/gRPC-Kafka-API.git
cd gRPC-Kafka-API
docker compose up --build
