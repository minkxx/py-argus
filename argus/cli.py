import argparse

from argus.engines.ollama_engine import OllamaEngine
from argus.strategies.nestjs_app import NestJsStrategy
from argus.audit import CodebaseAuditor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="argus",
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
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    engine = OllamaEngine(model_name=args.model)
    strategy = NestJsStrategy()

    auditor = CodebaseAuditor(engine, strategy, output_name=args.output_name)
    return auditor.execute(args.target_path)
