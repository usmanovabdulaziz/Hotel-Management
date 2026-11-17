from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


# Check-in kuni hisobga olinadi, check-out kuni hisobga olinmaydi.
@dataclass(frozen=True)
class DateRange:
    check_in: date
    check_out: date

    def is_valid(self) -> bool:
        return self.check_out > self.check_in

    # Ikki turar joy oralig'i kamida bitta umumiy tunni bo'lishsa, overlap.
    def overlaps(self, other: DateRange) -> bool:
        return self.check_in < other.check_out and other.check_in < self.check_out


@dataclass(frozen=True)
class Guest:
    name: str
    email: str


@dataclass(frozen=True)
class Room:
    number: str
    type: str


class ReservationStatus(Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"


class Reservation:
    def __init__(
        self,
        reservation_id: str,
        guest: Guest,
        room: Room,
        stay: DateRange
    ) -> None:
        self.id = reservation_id
        self.guest = guest
        self.room = room
        self.stay = stay
        self.status = ReservationStatus.CONFIRMED

    def blocks(self, room: Room, stay: DateRange) -> bool:
        return (
            self.status == ReservationStatus.CONFIRMED
            and self.room == room
            and self.stay.overlaps(stay)
        )

    def cancel(self) -> bool:
        if self.status == ReservationStatus.CANCELLED:
            return False

        self.status = ReservationStatus.CANCELLED
        return True