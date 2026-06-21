from datetime import datetime
from pathlib import Path

from judex.engines.base import LLMEngine
from judex.strategies.base import AuditStrategy


class CodebaseAuditor:
    def __init__(
        self,
        engine: LLMEngine,
        strategy: AuditStrategy,
        output_name: str = "audit_report.md",
    ):
        self.engine = engine
        self.strategy = strategy
        self.output_name = output_name

    def _gather_files(self, target_dir: Path) -> list[Path]:
        files = []
        for ext in self.strategy.target_extensions:
            for path in target_dir.rglob(f"*{ext}"):
                if path.is_file() and not self.strategy.should_ignore(
                    path, self.output_name
                ):
                    files.append(path)
        return files

    def execute(self, target_path: str) -> int:
        target_dir = Path(target_path).resolve()
        if not target_dir.exists() or not target_dir.is_dir():
            print(f"❌ Path does not exist or is not a directory: {target_dir}")
            return 1

        output_file_path = target_dir / self.output_name
        files_to_audit = self._gather_files(target_dir)

        if not files_to_audit:
            print("❌ No matching files found based on the selected audit strategy.")
            return 1

        print(
            f"🔍 Starting code audit using engine: '{self.engine.__class__.__name__}'"
        )
        print(f"📂 Scanning {len(files_to_audit)} files inside: {target_dir.name}\n")

        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(f"# Codebase Audit Report: {target_dir.name}\n")
            f.write(
                f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write(f"**Engine Configuration:** {self.engine.model_name}\n\n---\n")

        for file_path in files_to_audit:
            relative_path = file_path.relative_to(target_dir)
            print(f"▶️ Auditing: {relative_path}")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if not content.strip() or len(content) < 20:
                    continue

                user_prompt = f"Review this file:\n\nFile Path: `{relative_path}`\n\n```{self.strategy.code_language}\n{content}\n```"

                chunks_generator = self.engine.stream_chat(
                    self.strategy.system_prompt, user_prompt
                )

                with open(output_file_path, "a", encoding="utf-8") as out_file:
                    out_file.write(f"\n## File: `{relative_path}`\n\n")
                    for chunk in chunks_generator:
                        out_file.write(chunk)
                        out_file.flush()
                    out_file.write("\n\n---\n")

                print(f"✅ Completed: {relative_path}")

            except Exception as e:
                print(f"❌ Failed to audit {relative_path}: {e}")

        return 0
