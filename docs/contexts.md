# Hotel contexts

## Words (Umumiy atamalar)

| Word | Meaning here (Bu loyihadagi ma’nosi) | Name in our code |
|---|---|---|
| Guest | Mehmonxonada xona band qilmoqchi bo‘lgan shaxs. | `Guest` |
| Room | Mehmon joylashishi mumkin bo‘lgan, raqam bilan aniqlanadigan xona. | `Room` |
| Room type | Xonaning turi, masalan Standard yoki Deluxe. | `Room` ichidagi `type` maydoni |
| Stay | Check-in sanasidan check-out sanasigacha bo‘lgan davr; check-out kuni tun hisoblanmaydi. | `DateRange` |
| Reservation | Mehmon, xona, yashash davri va statusni birlashtiradigan bron yozuvi. | `Reservation` |
| Confirmed | Xona shu mehmon uchun belgilangan tunlarga band qilingan. | `ReservationStatus.CONFIRMED` |
| Cancelled | Bron bekor qilingan va uning tunlari qayta band qilish uchun bo‘shagan. | `ReservationStatus.CANCELLED` |
| Book | Mehmon uchun xona va sanalarni bron qilish amali. | `BookingService.reserve()` |
| Cancel | Mavjud bronni bekor qilish amali. | `BookingService.cancel()` |
| Free rooms | Berilgan sanalar oralig‘ida band bo‘lmagan xonalar. | `BookingService.find_free_rooms()` |
| Nightly price | Xonada bir tun qolish narxi. | Hozircha kodda yo‘q |
| Out of service | Ta’mirlash yoki boshqa sabab bilan mehmonlarga taklif qilinmaydigan xona. | Hozircha kodda yo‘q |
| Deposit | Bron vaqtida olinadigan, yashash umumiy narxining 30 foiziga teng avans to‘lovi. | Hozircha kodda yo‘q |
| Paid | Depozit muvaffaqiyatli to‘langan holat. | Hozircha kodda yo‘q |
| Declined | Depozit to‘lovi rad etilgan holat. | Hozircha kodda yo‘q |
| Confirmation message | Bron tasdiqlangani haqida mehmonga yuboriladigan xabar. | `NotificationSender.send_confirmation()` |
| Sent | Xabar yuborilgan holat. | Hozircha alohida status sifatida kodda yo‘q |
| Failed | Xabar yuborish muvaffaqiyatsiz bo‘lgan holat. | `BookingResult.notification_failed` (xabar statusi emas, xatolik belgisi) |

## Rooms (Inventory)

Job: mehmonxona qaysi xonalarni taklif qilishi mumkinligini, ularning turini, narxini va xizmat holatini biladi.

| Word | Meaning here |
|---|---|
| Room | R7 yoki R8 kabi xona raqami va unga tegishli ma’lumotlar. |
| Room type | Xonaning Standard yoki Deluxe kabi toifasi. |
| Nightly price | Xona turiga bog‘liq bir kechalik narx. |
| Out of service | Ta’mir yoki nosozlik sababli vaqtincha sotuvga chiqarilmagan xona. |

Rules this context owns:
- Xona `Out of service` bo‘lsa, mehmonlarga taklif qilinmaydi.
- Nightly price xona turiga bog‘liq; Deluxe xonalar Standard xonalardan qimmatroq.

Needs from other contexts: nothing.

Tells other contexts: Reservations uchun mavjud xonalar ro‘yxati, xona raqami va turi.

## Reservations

Job: mehmon qaysi xonada qaysi tunlarda qolishini hal qiladi va barcha bronlarni saqlaydi.

| Word | Meaning here |
|---|---|
| Guest | Bron qilayotgan mehmon va uning ma’lumotlari. |
| Stay | Check-in va check-out sanalari oralig‘i; check-out kuni tun hisoblanmaydi. |
| Reservation | Guest + room number + stay + status, masalan R101 identifikatorli bron. |
| Confirmed | Xona shu mehmon uchun ko‘rsatilgan tunlarda band qilingan. |
| Cancelled | Bron bekor qilingan; uning tunlari qayta band qilish uchun bo‘sh. |
| Book | Xona va sanalar uchun yangi bron yaratish. |
| Cancel | Mavjud bronni bekor qilish. |
| Free rooms | Tanlangan sanalarda band bo‘lmagan xonalar. |

Rules this context owns:
- Bir xonada bir-biriga to‘g‘ri keladigan tunlar uchun ikkita `Confirmed` reservation bo‘lishi mumkin emas.
- Check-out sanasi check-in sanasidan keyin bo‘lishi kerak.
- Reservation bekor qilinganda uning tunlari yangi bronlar uchun bo‘shaydi.

Needs from other contexts: Rooms kontekstidan mavjud xonalar ro‘yxati; Payments kontekstidan depozit to‘lovi natijasi.

Tells other contexts: Notifications kontekstiga `ReservationConfirmed` hodisasi.

## Payments

Job: depozit to‘lovlarini qabul qiladi va ularning to‘langan yoki rad etilgan holatini qayd etadi.

| Word | Meaning here |
|---|---|
| Deposit | Yashash umumiy narxining 30 foiziga teng avans to‘lovi. |
| Paid | Depozit muvaffaqiyatli to‘langan. |
| Declined | Depozit to‘lovi rad etilgan. |
| Cancel (refund) | To‘langan depozitni qaytarish jarayoni. |

Rules this context owns:
- Depozit yashash umumiy narxining 30 foiziga teng.
- Faqat `Paid` holatidagi depozit qaytarilishi mumkin.

Needs from other contexts: bron identifikatori va depozit summasini Reservations kontekstidan oladi; narxni hisoblash uchun Rooms kontekstining nightly price ma’lumotidan foydalanadi.

Tells other contexts: Reservations kontekstiga to‘lov natijasini `Paid` yoki `Declined` sifatida qaytaradi.

## Notifications

Job: mehmonlarga bron bilan nima sodir bo‘lganini email yoki SMS orqali xabar qiladi.

| Word | Meaning here |
|---|---|
| Confirmation message | Bron tasdiqlanganini bildiruvchi xabar. |
| Sent | Xabar yuborilgan holat. |
| Failed | Xabar yuborish muvaffaqiyatsiz bo‘lgan holat. |

Rules this context owns:
- Xabar yuborishdagi xatolik `Failed` sifatida qayd etiladi.
- Xabar yuborishdagi xatolik reservation statusini o‘zgartirmaydi.

Needs from other contexts: Reservations kontekstidan `ReservationConfirmed` hodisasi va xabar yuborish uchun zarur maydonlar.

Tells other contexts: xabar yuborish natijasi yoki xatoligi haqida tegishli monitoring/log tizimiga ma’lumot beradi; reservation statusini o‘zgartirmaydi.

## Same word, different meaning (Bir xil so‘z, turli ma’no)

| Word | Rooms | Reservations | Payments | Notifications |
|---|---|---|---|---|
| Room | R8: Deluxe turi, nightly price va xizmat holati | Reservation ichidagi R8 xona raqami | Ishlatilmaydi | Xabardagi “Room R8” matni |
| Status | In service / out of service | Confirmed / Cancelled | Paid / Declined | Sent / Failed |
| Cancel | Xonani vaqtincha sotuvdan chiqarish | Reservationni bekor qilish | Depozitni qaytarish | Ishlatilmaydi |

Agar barcha kontekstlar bitta umumiy `Status` maydonidan foydalansa, Notifications xabar yuborishda xatolik yuz bergani uchun statusni `Failed` ga o‘zgartirishi va Maya’ning R7 bronini bekor qilingandek ko‘rsatishi mumkin edi. Bu R6 qoidasini buzadi: xabar yuborishdagi xatolik reservationni o‘zgartirmasligi kerak.

## Rule owners (Qoidalar egalari)

| Card | Rule | Owner | Why this owner |
|---|---|---|---|
| 1 | Bir xonada bir-biriga to‘g‘ri keladigan tunlar uchun ikkita Confirmed reservation bo‘lishi mumkin emas. | Reservations | Bu context xonaning barcha reservationlarini saqlaydi va ularning sanalarini solishtira oladi. |
| 2 | Check-out sanasi check-in sanasidan keyin bo‘lishi kerak. | Reservations | Stay sanalari va ularning validatsiyasi Reservations mas’uliyatiga kiradi. |
| 3 | Reservation bekor qilinganda uning tunlari yangi bronlar uchun bo‘shaydi. | Reservations | Reservation statusi va bron qilingan tunlar shu contextda boshqariladi. |
| 4 | Out of service bo‘lgan xona mehmonlarga taklif qilinmaydi. | Rooms | Xonaning xizmat holati va sotuvga yaroqliligini Rooms boshqaradi. |
| 5 | Nightly price xona turiga bog‘liq; Deluxe Standard’dan qimmatroq. | Rooms | Xona turi va uning narxi Rooms kontekstining ma’lumotlari. |
| 6 | Deposit yashash umumiy narxining 30 foiziga teng. | Payments | Depozit summasini hisoblash va pul qoidalari Payments mas’uliyatiga kiradi. |
| 7 | Faqat Paid holatidagi depozit qaytarilishi mumkin. | Payments | To‘lov statusi va refund qoidalarini Payments boshqaradi. |
| 8 | Xabar yuborishdagi xatolik Failed sifatida qayd etiladi va reservationni o‘zgartirmaydi. | Notifications | Xabar holati va yuborish xatolari Notifications kontekstiga tegishli. |

## Between contexts (Kontekstlar orasidagi aloqa)

### Reservations → Rooms: which rooms exist? (question)

Sent when: Reservations bo‘sh xonalarni qidirishi yoki yangi bron uchun xona mavjudligini tekshirishi kerak bo‘lganda.

What Reservations sends:
- Stay: check-in va check-out sanalari.

The answer and its fields:
- Xonalar ro‘yxati.
- `roomNumber`: xona raqami, masalan `R7`.
- `roomType`: xona turi, masalan `Standard` yoki `Deluxe`.

Never crosses: Rooms kontekstining ichki saqlash tuzilmasi va ta’mirlashni boshqarish tafsilotlari.

### Reservations → Payments: take a deposit (question, from P17)

Sent when: yangi bron uchun depozit to‘lovi talab qilinganda.

What Reservations sends:
- `reservationId`: bron identifikatori, masalan `R101`.
- `amount`: olinishi kerak bo‘lgan depozit summasi.

The answer and its fields:
- `status`: `Paid` yoki `Declined`.

Never crosses: Payments kontekstining karta ma’lumotlari, payment provider maxfiy ma’lumotlari va ichki tranzaksiya tafsilotlari.

### Reservations → Notifications: ReservationConfirmed (event)

Sent when: reservation `Confirmed` holatida saqlangandan keyin.

What Reservations sends:
- `reservationId`: `R101`.
- `guestEmail`: `maya@example.com`.
- `roomNumber`: `R7`.
- `checkIn`: `2026-11-12`.
- `checkOut`: `2026-11-14`.

Reservations javob kutmaydi. Xabar yuborishdagi xatolik R101 reservationini o‘zgartirmaydi (R6 qoida).

Never crosses: Reservations kontekstining barcha reservationlari ro‘yxati. Notifications bu ro‘yxatni o‘qimaydi.
