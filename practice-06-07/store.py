"""Сховище в пам’яті для відтворюваного навчального запуску."""

from threading import Lock


class RecordNotFound(LookupError):
    """Запис із зазначеним ідентифікатором відсутній."""


class DuplicateEmail(ValueError):
    """Електронна адреса вже належить іншому студентові."""


class Store:
    def __init__(self, seeds, *, unique_email=False):
        self._rows = {i: {**row, "id": i} for i, row in enumerate(seeds, 1)}
        self._next_id = len(self._rows) + 1
        self._unique_email = unique_email
        self._lock = Lock()

    def all(self):
        with self._lock:
            return [row.copy() for row in self._rows.values()]

    def get(self, record_id):
        with self._lock:
            return self._find(record_id).copy()

    def _find(self, record_id):
        try:
            return self._rows[record_id]
        except KeyError:
            raise RecordNotFound from None

    def _check_email(self, values, keep_id=None):
        if self._unique_email and any(
            row["email"] == values["email"] and row["id"] != keep_id
            for row in self._rows.values()
        ):
            raise DuplicateEmail

    def create(self, values):
        # Перевірка унікальності й запис відбуваються під одним блокуванням.
        with self._lock:
            self._check_email(values)
            record_id = self._next_id
            row = {**values, "id": record_id}
            self._rows[record_id] = row
            self._next_id += 1
            return row.copy()

    def update(self, record_id, changes):
        with self._lock:
            row = self._find(record_id) | changes
            self._check_email(row, keep_id=record_id)
            self._rows[record_id] = row
            return row.copy()

    def delete(self, record_id):
        with self._lock:
            self._find(record_id)
            del self._rows[record_id]
