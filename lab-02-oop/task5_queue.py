"""Стратегії впорядкування черги завдань на друк."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class PrintJob:
    title: str
    pages: int
    arrival_minute: int
    urgent: bool = False


class QueueStrategy(ABC):
    @abstractmethod
    def order(self, jobs: tuple[PrintJob, ...]) -> list[PrintJob]:
        """овертає новий список завдань у порядку друку."""


class FirstInFirstOut(QueueStrategy):
    def order(self, jobs: tuple[PrintJob, ...]) -> list[PrintJob]:
        return sorted(jobs, key=lambda job: job.arrival_minute)


class ShortestFirst(QueueStrategy):
    def order(self, jobs: tuple[PrintJob, ...]) -> list[PrintJob]:
        return sorted(jobs, key=lambda job: (job.pages, job.arrival_minute))


class PrinterQueue:
    def __init__(self, strategy: QueueStrategy) -> None:
        self._strategy = strategy
        self._jobs: list[PrintJob] = []

    def add(self, job: PrintJob) -> None:
        self._jobs.append(job)

    def set_strategy(self, strategy: QueueStrategy) -> None:
        self._strategy = strategy

    def print_order(self) -> list[PrintJob]:
        return self._strategy.order(tuple(self._jobs))
