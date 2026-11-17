# ADR-001: Mehmonxona bronlash ilovasini modular monolith sifatida boshlash

**Holat:** Qabul qilindi, 2026-yil 17-noyabr

## Kontekst

Bitta kichik jamoa butun ilovani ishlab chiqadi va chiqaradi. Mehmonxona biznesi to‘rtta sohani o‘z ichiga oladi: Rooms, Reservations, Payments va Notifications. Eng muhim sifat ssenariylari — S2 (bir xonani bir xil tunlarga ikki marta band qilmaslik) va S3 (xabar yuborilmasa ham bron saqlanib qolishi). Hozircha hech bir modulni alohida chiqarish yoki alohida masshtablash talabi yo‘q.

## Qaror

Ilova bitta deploy qilinadigan tizim bo‘lib qoladi, lekin to‘rtta modulga ajratiladi. Har bir modul public contract va internal code ga ega. Reservations bronlash qoidasiga egalik qiladi. Architecture tests modullarning boshqa modul ichki kodidan foydalanishini taqiqlaydi.

## Ko‘rib chiqilgan alternativalar

Payments va Notifications ni alohida servislar qilish. Bu mustaqil deploy va masshtablash imkonini beradi, ammo tarmoq xatolari, retry, ko‘proq deploy va monitoring murakkabligini ham olib keladi.

## Oqibatlar

- Bitta build va bitta deploy; modullar orasidagi chaqiruvlar lokal method call bo‘ladi.
- Bronlash qoidasi Reservations ichida bir joyda saqlanadi.
- Barcha modullar birgalikda chiqariladi.
- Chegaralar architecture tests ishga tushirilgandagina himoyalanadi; P25 da CI ga qo‘shiladi.

## Qachon qayta ko‘rib chiqiladi?

Modulga o‘z deploy jadvali yoki alohida masshtablash zarurati real o‘lchovlar bilan isbotlansa (L07/P13).
