from __future__ import annotations

import time
from dataclasses import dataclass

from hotel_booking.domain import DateRange, Guest, Reservation, Room
from hotel_booking.notifications import NotificationSender
from hotel_booking.stores import ReservationStore


@dataclass(frozen=True)
class BookingResult:
    outcome: str
    reservation_id: str | None = None
    notification_failed: bool = False

    def __str__(self) -> str:
        return (
            self.outcome
            if self.reservation_id is None
            else f"{self.outcome} {self.reservation_id}"
        )


class BookingService:
    def __init__(
        self,
        rooms: list[Room],
        store: ReservationStore,
        notifications: NotificationSender,
        slow_step_seconds: float = 0
    ) -> None:
        self.rooms = rooms
        self.store = store
        self.notifications = notifications
        self.slow_step_seconds = slow_step_seconds

    def find_free_rooms(self, stay: DateRange) -> list[Room]:
        return [
            room for room in self.rooms
            if not self.store.has_overlap(room, stay)
        ]

    def reserve(
        self,
        guest: Guest,
        room: Room,
        stay: DateRange
    ) -> BookingResult:

        if not stay.is_valid():
            return BookingResult("InvalidDates")

        if self.store.has_overlap(room, stay):
            return BookingResult("Unavailable")

        # Race condition demonstratsiyasi uchun.
        time.sleep(self.slow_step_seconds)

        reservation = Reservation(
            f"R{101 + self.store.count()}",
            guest,
            room,
            stay
        )

        # Avval booking saqlanadi.
        self.store.save(reservation)

        # R6: xabar yuborish muvaffaqiyatsiz bo'lsa ham
        # booking saqlangan va Accepted bo'lib qoladi.
        try:
            self.notifications.send_confirmation(reservation)
        except Exception:
            return BookingResult(
                "Accepted",
                reservation.id,
                notification_failed=True
            )

        return BookingResult("Accepted", reservation.id)

    def cancel(self, reservation_id: str) -> bool:
        reservation = self.store.find(reservation_id)

        return (
            reservation is not None
            and reservation.cancel()
        )