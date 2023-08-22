from typing import Protocol

from .linters import LinterResponse


class LinterProtocol(Protocol):
    linter_name: str

    def create_report(self, file_path: str) -> LinterResponse:
        """
        Создание отчета после проверки python скрипта линтером
        :param file_path:  путь до скрипта
        """


class ReportService:
    def __init__(self, linters_list: list[LinterProtocol]):
        self._reports = []
        self._linters_list = linters_list

    def _run_linters(self, file_path: str) -> list[LinterResponse]:
        self._reports = []
        for linter in self._linters_list:
            self._reports.append(linter.create_report(file_path))
        return self._reports

    def create_reports(self, file_path: str) -> list[LinterResponse]:
        return self._run_linters(file_path)
