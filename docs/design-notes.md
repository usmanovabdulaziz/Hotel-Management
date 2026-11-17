# P06 design notes

## Before

- Tests: P04 dagi 8 ta test yashil.
- Demo: kutilgan 9 qatorli natija.
- Race: R7 uchun bir vaqtda yuborilgan ikkala so‘rov ham qabul qilinadi; double booking mavjud.

## Modules

| Modul | Public contract | Internal code |
|---|---|---|
| Rooms | `Room`, `RoomCatalog` | `InMemoryRoomCatalog` |
| Reservations | `BookingService`, `BookingResult`, `Reservation`, `DateRange`, `Guest`, `ReservationStatus`, `ReservationStore` | `InMemoryReservationStore` |
| Payments | `PaymentStatus`, `PaymentService` | `SimulatedPaymentService` |
| Notifications | `Confirmation`, `NotificationSender` | `EmailNotificationSender`, `SmsNotificationSender` |

## Architecture rules

1. Reservations boshqa modullarning faqat public contract laridan foydalanadi; `*.internal` ga import qilmaydi.
2. Rooms boshqa modullarga bog‘liq bo‘lmaydi.
3. Payments va Notifications Reservations ga bog‘liq bo‘lmaydi. Bog‘liqlik yo‘nalishi Reservations dan tashqariga qarab boradi; dependency cycle bo‘lmaydi.

## Broken on purpose

Step 7 da `reservations/booking.py` ichiga `from hotel_booking.notifications.internal import EmailNotificationSender` importi vaqtincha qo‘shildi. Birinchi qoida buzildi; `lint-imports` Reservations modulining `notifications.internal` ga taqiqlangan bog‘liqligini ko‘rsatdi. Import olib tashlangach, uchala contract yana KEPT bo‘ldi.

## After

- Tests: 8 ta behavior test.
- Architecture: 3 ta contract KEPT (jami 11 ta yashil tekshiruv).
- Demo: P04 dagi o‘sha 9 qator.
- Race: double booking hanuz takrorlanadi; uni P09 hal qiladi.
