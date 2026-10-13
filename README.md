# Multi-Agent Blackboard Bus

A deterministic Python demonstration of task evaluation by three specialized workers, with a supervisor that aggregates alerts into a consensus dossier. The project also retains a separate, earlier `blackboard_bus` coordinator and CLI.

## What works

- **Supervisor:** Checks primary metric > 25, secondary metric > 12 or an explicit critical flag, and anomalous status keywords.
- **Result dossier:** Returns worker alerts, urgency, integrity status, and an audit entry hash.
- **Audit trail:** HMAC-SHA256-linked records held in process memory. Set `AUDIT_SECRET_KEY` to reuse a signing key across launches; records themselves are **not persisted**.
- **Identifier screening:** Pattern-based checks for selected identifiers in task fields, attributes, chat text, and audit metadata. This is not comprehensive de-identification or a HIPAA compliance guarantee.
- **Interfaces:** Python CLI, CSV batch processing, FastAPI REST service, and a standalone browser demo.
- **Legacy coordinator:** `blackboard_bus` exposes a separate threshold-based worker system; it remains available for compatibility.

The `mock` LLM is deterministic and does not call an external service. The other names accepted by `LLMFactory` currently resolve to the same mock implementation. The enrichment modules are threshold-based demonstrations rather than full event sourcing, queueing, or state restoration engines.

## Browser demo

The `web/` directory contains a static JavaScript version of the three supervisor rules. It needs no API, Python runtime, or credentials. To run locally:

```bash
python -m http.server 8080 --directory web
```

Open `http://127.0.0.1:8080/`, enter measurements, select **Evaluate task**, and optionally export the result as JSON. The page does not make network requests or store the entered data. It has **no cryptographic audit trail** and is not a substitute for the Python service. A GitHub Pages deployment workflow is included; site availability depends on the repository's Pages settings.

## Python installation

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[server,test]"
pytest -q
```

Use the installed CLI:

```bash
blackboard-bus audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
blackboard-bus batch -i sample.csv -o results.csv
blackboard-bus chat "What is the system status?"
blackboard-bus verify-audit
```

CSV `is_critical_flag` accepts `true/false`, `1/0`, or `yes/no` (case-insensitive). Invalid values cause an error rather than silently changing escalation decisions.

The legacy implementation can still be run using `python -m blackboard_bus.cli audit`.

## REST service

Start the primary FastAPI application:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
blackboard-bus serve --host 127.0.0.1 --port 8000
```

- `GET /health`: service status
- `POST /api/audit`: evaluate a `SystemTaskPayload`
- `POST /api/chat`: deterministic mock answer
- `GET /api/audit/logs`: in-memory audit entries and chain check
- `GET /metrics`: JSON task/audit counters
- `GET /metrics/prometheus`: Prometheus text counters

The API has **no built-in authentication**. Bind it to loopback or place it behind authenticated access control before exposing it on a network. Do not send real patient information to these demonstration endpoints. Audit signatures authenticate entries in memory but cannot establish completeness after log deletion or process restart.

## Docker

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

Compose publishes the service on `127.0.0.1:8000` only. The key must be set by the operator and is not checked into the repository.

## Testing

```bash
pytest -q
node --test tests/browser.test.mjs  # Node.js 22
python -m build                      # after installing build
```

GitHub Actions checks Python 3.10–3.12, builds the distribution, runs Python and browser tests, and audits installed dependencies.

## Technology and privacy

Python, Pydantic 2, optional FastAPI/Uvicorn, standard-library HMAC/hashlib, and dependency-free JavaScript. The browser demo works in current modern browsers supporting ES modules and Blob downloads. Python APIs operate in process memory; no database or cross-session audit storage is configured. The browser demo is local-only and makes no background network requests.

## License

MIT. See [LICENSE](LICENSE).
