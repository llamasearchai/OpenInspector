# OpenInspector Demo Walkthrough

```python
from openinspector.client import OpenInspectorClient

client = OpenInspectorClient()

signal = {
    "type": "authentication",
    "user_id": "notebook-user",
    "success": False,
    "metadata": {"failed_attempts": 7}
}

resp = client.send_signal(**signal)
resp
```

Expected output:

```python
{
  'signal_id': '...',
  'detection': {'risk_level': 'high', 'risk_score': 0.7, ...},
  'interventions': [{'action': 'suspend', ...}]
}
```

You can now query Prometheus metrics at `http://localhost:8000/metrics` or review recent signals:

```python
import httpx
httpx.get("http://localhost:8000/signals").json()[:3]
``` 