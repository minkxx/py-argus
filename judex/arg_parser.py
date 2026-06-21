import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="judex",
        description="Audit a codebase and generate a markdown review report.",
    )
    parser.add_argument(
        "target_path",
        nargs="?",
        default=".",
        help="Directory to audit (defaults to the current directory).",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="qwen2.5-coder:7b",
        help="Ollama model name to use for the audit.",
    )
    parser.add_argument(
        "-o",
        "--output-name",
        default="audit_report.md",
        help="Markdown file name to write inside the audited directory.",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List available components.",
    )
    parser.add_argument(
        "-s",
        "--strategy",
        nargs="?",
        default="NestJsStrategy",
        help="Strategy name to use for the audit.",
    )
    parser.add_argument(
        "-e",
        "--engine",
        nargs="?",
        default="OllamaEngine",
        help="Engine name to use for the audit.",
    )
    return parser
