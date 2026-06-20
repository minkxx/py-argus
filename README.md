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
  -l, --list            List available components.
  -s, --strategy [STRATEGY]
                        Strategy name to use for the audit.
  -e, --engine [ENGINE]
                        Engine name to use for the audit.
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

## Build - DIY

#### 1. Git clone this repo

```bash
git clone https://github.com/minkxx/py-argus.git

cd py-argus
```

#### 2. Install required dependencies

```bash
pip install -r requirements.txt
```

#### 3. Build the `py-argus` package

```bash
python -m build
```

#### 4. Install the `py-argus` package

```bash
pip install -e .
```

#### 5. Use it

```bash
argus --help
```
