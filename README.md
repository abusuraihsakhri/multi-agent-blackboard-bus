# Multi Agent Blackboard Bus

> **Domain:** Autonomous Agent Systems & Context State Architecture  
> **Reference Guidelines & Standards:** `Distributed Systems RFC & State Machine Verification`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Multi Agent Blackboard Bus** is an advanced analytical and computational platform implementing Hearsay-II asynchronous publish-subscribe shared memory bus for multi-agent swarms. It coordinates multiple specialized worker agents that independently evaluate tasks, detect anomalies, and reach consensus through a supervisor orchestrator.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Multi-Agent Coordination**: Supervisor orchestrator with specialized worker agents (Invariant QC, Safety Escalation, Protocol Conformance)
- **Consensus Dossier Generation**: Aggregated multi-worker evaluations with urgency classification
- **Zero-PHI Outbound Guard**: Active regex inspection blocking SSNs, MRNs, phone numbers, emails, and patient identifiers
- **Tamper-Evident HMAC-SHA256 Audit Trail**: Chained, cryptographically signed logs with integrity verification
- **FastAPI REST API**: OpenAPI-compatible REST endpoints for audit, chat, and metrics
- **Prometheus Telemetry**: Operational metrics exporter for monitoring
- **LLM Integration**: Pluggable inference engine supporting mock, Ollama, Claude, and OpenAI providers
- **Bayesian Calibration**: Active learning engine for worker reliability weight tracking

---

## 💻 CLI Quickstart & Usage

### Installation
```bash
pip install -e .
```

### 1. Run Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task identifier (default: TASK-2026-001)
- `--target`: Target entity identifier (default: KEY-TARGET-01)
- `--primary`: Primary metric value, float (default: 28.5)
- `--secondary`: Secondary metric value, float (default: 14.2)
- `--critical`: Flag for critical escalation (default: False)
- `--status`: Status descriptor string (default: DISCORDANT)

---

## 🛡️ Security Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, DOB patterns, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition. Integrity verification recomputes and validates every signature in the chain.
* **Secure Key Management:** Audit signing key sourced from `AUDIT_SECRET_KEY` environment variable. A secure random key is generated if not set (with a runtime warning).

### Environment Variables
| Variable | Description | Required |
|:---------|:------------|:---------|
| `AUDIT_SECRET_KEY` | HMAC signing key for audit trail integrity | Recommended |

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Run with coverage:

```bash
pytest -v --cov=agents --cov=blackboard_bus
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
docker build -t multi-agent-blackboard-bus .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key multi-agent-blackboard-bus
```

Or using Docker Compose:

```bash
docker-compose up
```

---

## 📁 Project Structure

```
├── agents/                  # Core multi-agent system
│   ├── __init__.py
│   ├── api.py               # FastAPI REST server
│   ├── base.py              # Security, PHI guard, audit trail
│   ├── learning.py          # Bayesian calibration engine
│   ├── llm_factory.py       # LLM provider factory
│   ├── metrics.py           # Prometheus metrics collector
│   ├── models.py            # Pydantic data models
│   ├── streamer.py          # WebSocket telemetry broadcaster
│   ├── supervisor.py        # Master orchestrator
│   └── workers.py           # Specialized worker agents
├── blackboard_bus/          # Blackboard bus core engine
│   ├── __init__.py
│   ├── agents.py            # Sub-agents and coordinator
│   ├── cli.py               # CLI interface
│   ├── engine.py            # Domain engine
│   ├── models.py            # Data models
│   └── server.py            # FastAPI server factory
├── tests/                   # Test suite
├── cli.py                   # Top-level CLI entry point
├── simulator.py             # Simulation benchmark
├── enrichment.py            # Enrichment feature engines
├── sample.csv               # Sample batch input
├── sample_payload.json      # Sample API payload
├── pyproject.toml           # Project configuration
└── Dockerfile               # Container definition
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
