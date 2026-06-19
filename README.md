# Py-Argus

A local AI-powered codebase audit CLI

## Installation

```bash
pip install py-argus
```

### CLI Usage

```bash
usage: argus [-h] [-m MODEL] [-o OUTPUT_NAME] [target_path]

Audit a codebase and generate a markdown review report.

positional arguments:
  target_path           Directory to audit (defaults to the current directory).

options:
  -h, --help            show this help message and exit
  -m, --model MODEL     Ollama model name to use for the audit.
  -o, --output-name OUTPUT_NAME
                        Markdown file name to write inside the audited directory.
```

### import usage

```python
from argus import NestJsStrategy, OllamaEngine, CodebaseAuditor

if __name__ == "__main__":
    engine = OllamaEngine("qwen2.5-coder:7b")
    strategy = NestJsStrategy()

    auditor = CodebaseAuditor(engine, strategy)

    auditor.execute(".")

```
