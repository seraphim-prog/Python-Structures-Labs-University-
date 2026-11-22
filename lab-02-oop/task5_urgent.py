"""ова стратегія для пріоритетного друку термінових документів."""

from task5_queue import PrintJob, QueueStrategy


class UrgentFirst(QueueStrategy):
    def order(self, jobs: tuple[PrintJob, ...]) -> list[PrintJob]:
        return sorted(jobs, key=lambda job: (not job.urgent, job.arrival_minute))
