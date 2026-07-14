# gRPC Kafka API

A small experimental distributed system demonstrating communication between services using **REST**, **gRPC**, **Apache Kafka**, and **ClickHouse**.

The project was created to explore synchronous and asynchronous communication patterns in a microservice architecture.

---

## Architecture

```
                +----------------+
                |     Client     |
                +-------+--------+
                        |
                    HTTP/REST
                        |
                        v
               +-----------------+
               |   FastAPI REST  |
               +--------+--------+
                        |
             +----------+----------+
             |                     |
           gRPC                 Kafka
             |                     |
             v                     v
     +----------------+    +------------------+
     | Statistics     |    | Kafka Consumer   |
     | Service        |    +--------+---------+
     +--------+-------+             |
              |                     |
              +----------+----------+
                         |
                         v
                  +-------------+
                  | ClickHouse  |
                  +-------------+
```

---

## Components

- **REST API** built with FastAPI
- **gRPC** communication between services
- **Apache Kafka** for asynchronous event processing
- **ClickHouse** for analytical data storage
- **Docker Compose** for local development
- **Unit tests** with pytest

---

## Current Status

### Implemented

- REST API service
- gRPC service definition and generated client/server code
- Kafka consumer
- Docker Compose environment
- ClickHouse integration
- Basic unit tests

### Planned

- Persist Kafka events in ClickHouse
- End-to-end integration tests
- Health checks
- Improved logging and observability
- CI pipeline

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/Unrealimp/gRPC-Kafka-API.git
cd gRPC-Kafka-API
```

Start all services:

```bash
docker compose up --build
```

---

## Services

| Service | Port |
|----------|-----:|
| REST API | 8000 |
| gRPC Statistics Service | 50051 |
| ClickHouse HTTP | 8123 |
| ClickHouse Native | 9000 |
| Kafka | 9092 |
| ZooKeeper | 2181 |

---

## Running Tests

```bash
pytest
```

---

## Technology Stack

### Backend

- Python
- FastAPI
- gRPC

### Messaging

- Apache Kafka

### Database

- ClickHouse

### Infrastructure

- Docker
- Docker Compose

### Testing

- pytest

---

## Repository Structure

```
.
├── rest_api/
├── statistics_service/
├── proto/
├── tests/
├── docker-compose.yml
└── init.sql
```

---

## Purpose

This repository is intended as a learning project for experimenting with modern distributed system technologies, including REST APIs, gRPC, Kafka, Docker, and ClickHouse.

It is not intended to be a production-ready application but rather a demonstration of architectural concepts and communication patterns.

---

## Future Improvements

- Store Kafka events in ClickHouse
- Add Prometheus and Grafana monitoring
- Introduce API Gateway
- Improve fault tolerance
- Add GitHub Actions CI
- Increase test coverage

---

## License

MIT
