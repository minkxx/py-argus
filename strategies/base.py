from abc import ABC, abstractmethod
from pathlib import Path


class AuditStrategy(ABC):
    @property
    @abstractmethod
    def target_extensions(self) -> set[str]:
        pass

    @property
    @abstractmethod
    def ignore_dirs(self) -> set[str]:
        pass

    @property
    @abstractmethod
    def code_language(self) -> str:
        pass

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        pass

    def should_ignore(self, path: Path, output_file_name: str) -> bool:
        if path.name == output_file_name:
            return True
        for part in path.parts:
            if part in self.ignore_dirs:
                return True
        return False
