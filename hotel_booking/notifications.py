from __future__ import annotations

from typing import Protocol

from hotel_booking.domain import Reservation


class NotificationSender(Protocol):
    """BookingService uchun xabar yuborish shartnomasi."""

    def send_confirmation(self, reservation: Reservation) -> None:
        ...


class EmailNotificationSender:
    """Haqiqiy email yubormaydi, faqat yuborilgan xabarlarni sanaydi."""

    def __init__(self) -> None:
        self.sent = 0

    def send_confirmation(self, reservation: Reservation) -> None:
        self.sent += 1


class SmsNotificationSender:
    """Haqiqiy SMS yubormaydi, faqat yuborilgan xabarlarni sanaydi."""

    def __init__(self) -> None:
        self.sent = 0

    def send_confirmation(self, reservation: Reservation) -> None:
        self.sent += 1