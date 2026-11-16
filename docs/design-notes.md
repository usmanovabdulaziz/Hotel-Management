
# Dizayn qaydlari

## Nima uchun kod yozishdan oldin dizayn kerak?

Kod yozishdan oldin dizayn qilish tizimning tuzilishini tushunishga, sinflarning vazifalarini aniqlashga va obyektlar o‘zaro qanday ishlashini rejalashtirishga yordam beradi. Bu kod yozish jarayonini tartibli qiladi.

## Metodlar qayerda joylashgan?

- `Cancel()` metodi `Reservation` sinfida joylashgan, chunki bandlov o‘z holatini bekor qilinganda o‘zi o‘zgartiradi.
- `HasOverlap()` metodi `ReservationStore` sinfida joylashgan, chunki saqlangan bandlovlar orasidan sanalari ustma-ust keladigan bandlovlarni tekshirish omborning vazifasidir.

## Faoliyat jarayonlari

Bu bo‘limga topshiriqda berilgan faoliyat diagrammasi asosida bajarilgan jarayonlar va ularning kuzatuvlari yoziladi.

## Bashorat

Nora R7 xonasini 14–16 noyabr kunlariga band qilganda natija `Accepted R102` bo‘ladi. Chunki Maya bandlovi 12–14 noyabr kunlarini qamrab oladi, Nora esa 14-noyabr kuni kiradi. Chiqish sanasi bandlovga kirmagani uchun ular orasida umumiy tun yo‘q.

## Race condition

### Bashorat

Maya va Omar bir vaqtning o‘zida R7 xonasini 12–14 noyabr kunlariga band qilishga urinsa, ikkala bandlov ham `Confirmed` holatida saqlanadi. Chunki ikkala so‘rov ham xona bo‘shligini tekshiradi va bandlov saqlanishidan oldin tekshiruvdan o‘tadi.

### Haqiqiy natija

Test natijasida Maya `Accepted R101`, Omar esa `Accepted R102` javobini oldi. R7 xonasi uchun bir xil sanalarda ikkita `Confirmed` bandlov saqlanib qoldi.

### Muammoning sababi

Muammo `BookingService` sinfidagi `reserve()` metodi ichida yuzaga keladi. `has_overlap()` orqali xona bo‘shligi tekshirilishi va `save()` orqali bandlov saqlanishi orasida atomar himoya mavjud emas.

Ikkala so‘rov ham bandlov saqlanishidan oldin xona bo‘shligini tekshirishi mumkin. Natijada ikkalasi ham bandlovni muvaffaqiyatli saqlaydi va double booking yuzaga keladi.
