from __future__ import annotations

from hotel_booking.notifications import Confirmation


class EmailNotificationSender:
    """Simulated sender: counts messages and does not use a network."""
    def __init__(self) -> None:
        self.sent = 0

    def send_confirmation(self, confirmation: Confirmation) -> None:
        self.sent += 1


class SmsNotificationSender:
    """Simulated SMS sender with the same public contract."""
    def __init__(self) -> None:
        self.sent = 0

    def send_confirmation(self, confirmation: Confirmation) -> None:
        self.sent += 1
