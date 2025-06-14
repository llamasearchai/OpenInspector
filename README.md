# OpenInspector

**Production-grade account abuse and fraud detection platform with OpenAI Agents, FastAPI, and LangChain integration.**

OpenInspector is a comprehensive, Python-only platform for detecting, analyzing, and mitigating account abuse and fraud in real-time. It combines fast event collection, a flexible rules/ML detection engine, proactive defense workflows, and modern LLM-powered agents for sophisticated threat analysis.

## Key Features

* **FastAPI Service Layer** – Fully-typed OpenAPI specification with async endpoints
* **OpenAI Agents SDK Integration** – Advanced reasoning for complex incident analysis  
* **LangChain/LangGraph/LangSmith** – Complete observability and workflow orchestration
* **Real-time Signal Processing** – High-performance event ingestion and analysis
* **Adaptive Defense System** – Dynamic intervention mechanisms from monitoring to account actions
* **Production Database** – Async SQLAlchemy with SQLite/PostgreSQL support
* **Prometheus Metrics** – Built-in observability and monitoring
* **Docker Ready** – Complete containerization with docker-compose
* **Enterprise Grade** – Comprehensive testing, CI/CD, and documentation

## Quick Start

### Installation

```bash
pip install openinspector
```

### Basic Usage

```bash
export OPENAI_API_KEY=your_key_here
openinspector
```

Then open http://localhost:8000/docs to explore the automatically generated API documentation.

### Send Your First Signal

```python
from openinspector.client import OpenInspectorClient

client = OpenInspectorClient()
response = client.send_signal(
    type="authentication",
    user_id="user_123",
    success=False,
    ip_address="203.0.113.10",
    metadata={"failed_attempts": 5}
)

print(f"Risk Level: {response['detection']['risk_level']}")
print(f"Interventions: {response['interventions']}")
```

## Architecture

OpenInspector follows a modular, production-ready architecture:

- **Signal Gathering** – Collect and enrich behavioral, authentication, transaction, and network signals
- **Detection Engine** – Multi-layered analysis combining rules, ML models, and anomaly detection  
- **Defense System** – Policy-driven intervention execution with audit trails
- **Analytics Layer** – Rich insights into abuse patterns and defense effectiveness
- **Agent Framework** – LLM-powered investigation and automated playbooks

## Development

### Local Development

```bash
git clone https://github.com/llamasearchai/OpenInspector.git
cd OpenInspector
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e '.[dev]'
pytest
```

### Docker Development

```bash
docker-compose up --build
```

### Testing

```bash
# Run tests
pytest

# Run tests across Python versions
tox

# Lint and format
ruff check .
black .
```

## Documentation

- [Developer Documentation](docs/README.md)
- [API Reference](http://localhost:8000/docs) (when running locally)
- [Demo Notebook](notebooks/demo_signal_flow.md)
- [Changelog](CHANGELOG.md)

## Production Deployment

OpenInspector is designed for production use with:

- Async database operations with connection pooling
- Prometheus metrics for monitoring and alerting  
- Docker containerization with health checks
- Comprehensive logging and error handling
- Configurable via environment variables

## Contributing

We welcome contributions! Please see our [GitHub repository](https://github.com/llamasearchai/OpenInspector) for issues and pull requests.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Nik Jois** - [nikjois@llamasearch.ai](mailto:nikjois@llamasearch.ai)

---

*OpenInspector: Advanced fraud detection powered by modern AI* 