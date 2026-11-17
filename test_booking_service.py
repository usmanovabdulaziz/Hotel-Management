from datetime import date
import unittest

from hotel_booking.notifications import Confirmation
from hotel_booking.reservations import BookingService, DateRange, Guest, ReservationStatus
from hotel_booking.reservations.internal import InMemoryReservationStore
from hotel_booking.rooms import Room


R7 = Room("R7", "Standard")
R8 = Room("R8", "Deluxe")
MAYA = Guest("Maya", "maya@example.com")
OMAR = Guest("Omar", "omar@example.com")
NORA = Guest("Nora", "nora@example.com")


class FakeNotificationSender:
    def __init__(self, fail: bool = False) -> None:
        self.sent: list[str] = []
        self.fail = fail

    def send_confirmation(self, confirmation: Confirmation) -> None:
        if self.fail:
            raise RuntimeError("simulated provider outage")
        self.sent.append(confirmation.reservation_id)


def new_service(fail_notifications: bool = False):
    store = InMemoryReservationStore()
    sender = FakeNotificationSender(fail_notifications)
    service = BookingService([R7, R8], store, sender)
    return service, store, sender


def nov(check_in: int, check_out: int) -> DateRange:
    return DateRange(date(2026, 11, check_in), date(2026, 11, check_out))


class BookingServiceTests(unittest.TestCase):
    def test_failed_confirmation_keeps_booking(self):
        service, store, sender = new_service(fail_notifications=True)
        result = service.reserve(MAYA, R7, nov(12, 14))
        self.assertEqual(str(result), "Accepted R101")
        self.assertTrue(result.notification_failed)
        self.assertEqual(store.count(), 1)

    def test_cancelling_frees_room(self):
        service, store, _ = new_service()
        result = service.reserve(MAYA, R7, nov(12, 14))
        self.assertTrue(service.cancel(result.reservation_id))
        self.assertEqual(service.find_free_rooms(nov(12, 14)), [R7, R8])
        self.assertEqual(store.find("R101").status, ReservationStatus.CANCELLED)

    def test_checkout_must_be_after_checkin(self):
        service, _, _ = new_service()
        result = service.reserve(OMAR, R8, nov(15, 15))
        self.assertEqual(str(result), "InvalidDates")

    def test_maya_gets_r7_when_free(self):
        service, _, sender = new_service()
        result = service.reserve(MAYA, R7, nov(12, 14))
        self.assertEqual(str(result), "Accepted R101")
        self.assertEqual(sender.sent, ["R101"])

    def test_nora_can_arrive_when_maya_leaves(self):
        service, _, _ = new_service()
        service.reserve(MAYA, R7, nov(12, 14))
        result = service.reserve(NORA, R7, nov(14, 16))
        self.assertEqual(str(result), "Accepted R102")

    def test_omar_refused_when_a_night_is_shared(self):
        service, _, _ = new_service()
        service.reserve(MAYA, R7, nov(12, 14))
        result = service.reserve(OMAR, R7, nov(13, 15))
        self.assertEqual(str(result), "Unavailable")

    def test_one_confirmation_per_accepted_booking(self):
        service, _, sender = new_service()
        service.reserve(MAYA, R7, nov(12, 14))
        service.reserve(OMAR, R7, nov(13, 15))
        self.assertEqual(sender.sent, ["R101"])

    def test_sms_sender_contract_needs_no_booking_service_change(self):
        class FakeSmsSender:
            def __init__(self):
                self.sent = 0
            def send_confirmation(self, confirmation: Confirmation) -> None:
                self.sent += 1
        store = InMemoryReservationStore()
        sms = FakeSmsSender()
        service = BookingService([R7, R8], store, sms)
        result = service.reserve(MAYA, R7, nov(12, 14))
        self.assertEqual(str(result), "Accepted R101")
        self.assertEqual(sms.sent, 1)


if __name__ == "__main__":
    unittest.main()
