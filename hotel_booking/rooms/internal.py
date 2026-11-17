from __future__ import annotations

from hotel_booking.rooms.catalog import Room


class InMemoryRoomCatalog:
    """List-based implementation. Only the application wiring creates it."""

    def __init__(self, rooms: list[Room]) -> None:
        self._rooms = list(rooms)

    def all(self) -> list[Room]:
        return list(self._rooms)
