from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

from hotel_booking.notifications import Confirmation, NotificationSender
from hotel_booking.reservations.domain import DateRange, Guest, Reservation
from hotel_booking.rooms import Room


class ReservationStore(Protocol):
    """Storage contract required by BookingService."""
    def count(self) -> int: ...
    def has_overlap(self, room: Room, stay: DateRange) -> bool: ...
    def save(self, reservation: Reservation) -> None: ...
    def find(self, reservation_id: str) -> Reservation | None: ...
    def count_confirmed(self, room: Room, stay: DateRange) -> int: ...


@dataclass(frozen=True)
class BookingResult:
    outcome: str
    reservation_id: str | None = None
    notification_failed: bool = False

    def __str__(self) -> str:
        return self.outcome if self.reservation_id is None else f"{self.outcome} {self.reservation_id}"


class BookingService:
    """Owns booking rules and depends on other modules' public contracts only."""
    def __init__(
        self,
        rooms: list[Room],
        store: ReservationStore,
        notifications: NotificationSender,
        slow_step_seconds: float = 0,
    ) -> None:
        self.rooms = rooms
        self.store = store
        self.notifications = notifications
        self.slow_step_seconds = slow_step_seconds

    def find_free_rooms(self, stay: DateRange) -> list[Room]:
        return [room for room in self.rooms if not self.store.has_overlap(room, stay)]

    def reserve(self, guest: Guest, room: Room, stay: DateRange) -> BookingResult:
        if not stay.is_valid():
            return BookingResult("InvalidDates")
        if self.store.has_overlap(room, stay):
            return BookingResult("Unavailable")

        # Deliberately retained for the P04 race demonstration; P09 addresses atomicity.
        time.sleep(self.slow_step_seconds)
        reservation = Reservation(f"R{101 + self.store.count()}", guest, room, stay)
        self.store.save(reservation)
        try:
            self.notifications.send_confirmation(
                Confirmation(
                    reservation_id=reservation.id,
                    guest_email=guest.email,
                    room_number=room.number,
                    check_in=stay.check_in,
                    check_out=stay.check_out,
                )
            )
        except Exception:
            # R6: notification failure must not undo a successfully saved booking.
            return BookingResult("Accepted", reservation.id, notification_failed=True)
        return BookingResult("Accepted", reservation.id)

    def cancel(self, reservation_id: str) -> bool:
        reservation = self.store.find(reservation_id)
        return reservation is not None and reservation.cancel()
