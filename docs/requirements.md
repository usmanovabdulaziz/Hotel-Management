
# Talablar: Mehmonxona band qilish ilovasi, 1-versiya

## R1 · Xonalarni qidirish
Mehmon yoki administrator berilgan sanalar oralig‘ida bo‘sh xonalar ro‘yxatini ko‘ra oladi.

Tekshirish: mehmonxona bo‘sh bo‘lsa, 12–14 noyabr sanalari uchun → R7, R8.

## R2 · Xonani band qilish
Mehmon yoki administrator bo‘sh xonani band qila oladi. Ilova band qilish natijasida reservation ID qaytaradi.

Tekshirish: Maya R7 xonasini 12–14 noyabrga band qiladi → Accepted R101.

## R3 · Bir vaqtga ikki marta band qilishni oldini olish
Bir xonada bir xil tun uchun ikkita Confirmed bandlov bo‘lishi mumkin emas. Chiqish sanasi kirish sanasidan keyin bo‘lishi shart.

Tekshirish:
- Omar R7 xonasini 13–15 noyabrga band qilmoqchi → Unavailable.
- Omar R7 xonasini 15–15 noyabrga band qilmoqchi → InvalidDates.

**Qo‘shimcha misollar (R7):**
- Maya R7 xonasini 12–14 noyabrga band qilgan → Confirmed (12 va 13-noyabr tunlari).
- Omar R7 xonasini 13–15 noyabrga band qilmoqchi → Unavailable (13-noyabr tuni umumiy).
- Nora R7 xonasini 14–16 noyabrga band qilmoqchi → Accepted (umumiy tun yo‘q).

**Qo‘shimcha misollar (R8):**
- R8 xonasi 20–22 noyabr kunlariga band qilingan.
- Mehmon R8 xonasini 22–24 noyabrga band qilmoqchi → Accepted (umumiy tun yo‘q).
- Mehmon R8 xonasini 21–23 noyabrga band qilmoqchi → Unavailable (21-noyabr tuni umumiy).

## R4 · Bandlovni bekor qilish
Bandlovni bekor qilish mumkin. Bandlov Cancelled holatida saqlanadi va bekor qilingandan keyin xona boshqa bandlovlar uchun bo‘sh hisoblanadi.

Tekshirish: Maya R101 bandlovini bekor qiladi → R7 xonasi 12–14 noyabr sanalari uchun yana bo‘sh bo‘ladi.

## R5 · Bandlovni ko‘rish
Bandlovni uning ID raqami orqali qidirish mumkin.

Tekshirish: R101 → Maya, R7, 12–14 noyabr, Confirmed.

## R6 · Xabarnoma yuborishdagi xatolik (Failed message)

Agar booking tasdiqlangani haqidagi xabarnomani yuborish muvaffaqiyatsiz bo‘lsa, booking bazada saqlangan va Accepted holatida qolishi kerak. Xabarnoma yuborishdagi xatolik haqida tizim xabar berishi kerak.