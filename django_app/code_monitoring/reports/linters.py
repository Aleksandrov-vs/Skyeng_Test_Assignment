import subprocess

from pydantic import BaseModel


class LinterResponse(BaseModel):
    linter_name: str
    report_text: str


class Flake8Linter:
    linter_name = 'flake8'

    def create_report(self, file_path: str) -> LinterResponse:
        result = subprocess.run(
            ['flake8', '--filename={basename}', file_path],
            capture_output=True,
            text=True
        )
        output = result.stdout
        return LinterResponse(linter_name=self.linter_name, report_text=output)


class MyPyLinter:
    linter_name = 'mypy'

    def create_report(self, file_path: str) -> LinterResponse:
        result = subprocess.run(
            ['mypy', '--no-cache', file_path, '--ignore-missing-imports'],
            capture_output=True,
            text=True
        )
        output = result.stdout
        return LinterResponse(linter_name=self.linter_name, report_text=output)
