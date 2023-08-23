import subprocess

from pydantic import BaseModel
import re


class LinterResponse(BaseModel):
    linter_name: str
    report_text: str


class Flake8Linter:
    linter_name = 'flake8'

    def create_report(self, file_path: str) -> LinterResponse:
        result = subprocess.run(
            ['flake8', f'{file_path}'],
            capture_output=True,
            text=True
        )
        output = result.stdout
        report = ''
        pattern = r'^(.*?)(?=\/[A-Za-z0-9_]+\.py)'  # отсекает весь путь до файла
        for line in output.split('\n'):
            report += re.sub(pattern, ' ', line)
            report += '\n'
        return LinterResponse(linter_name=self.linter_name, report_text=report)


class MyPyLinter:
    linter_name = 'mypy'

    def create_report(self, file_path: str) -> LinterResponse:
        result = subprocess.run(
            ['mypy', file_path, '--ignore-missing-imports'],
            capture_output=True,
            text=True
        )
        output = result.stdout
        report = ''
        pattern = r'^(.*?)(?=\/[A-Za-z0-9_]+\.py)' # отсекает весь путь до файла
        for line in output.split('\n'):
            report += re.sub(pattern, ' ', line)
            report += '\n'
        return LinterResponse(linter_name=self.linter_name, report_text=report)
