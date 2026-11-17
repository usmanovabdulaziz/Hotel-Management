
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

# P04 design notes

## Refactoring

Refactoring — dastur kodining ichki tuzilishini o‘zgartirish, lekin uning tashqi xatti-harakati va natijalarini o‘zgartirmaslik jarayonidir.

### O‘zgarmasligi kerak bo‘lgan holatlar (Must stay the same)

- Refactoringdan keyin dastlabki 6 ta testning barchasi muvaffaqiyatli o‘tishi kerak.
- Dastur demo rejimida P03 dagi kabi aynan 9 qator natija chiqarishi kerak.
- Race demo hali ham Double booking muammosini namoyish qilishi kerak.

## What our code breaks

### 1. BookingService konkret storage klassiga bog‘langan

BookingService konkret storage klassiga to‘g‘ridan-to‘g‘ri bog‘langanligi Dependency Inversion Principle (DIP) prinsipiga zid.

Agar ma'lumotlarni saqlash uchun InMemory storage o‘rniga PostgreSQL ishlatmoqchi bo‘lsak, BookingService kodini ham o‘zgartirishimizga to‘g‘ri keladi. Bu esa dasturni kengaytirish va qo‘llab-quvvatlashni qiyinlashtiradi.

### 2. BookingService konkret Email sender klassiga bog‘langan

BookingService to‘g‘ridan-to‘g‘ri EmailSender klassiga bog‘langanligi Dependency Inversion Principle (DIP) prinsipiga zid va Open/Closed Principle (OCP) prinsipiga rioya qilishni qiyinlashtiradi.

Agar SMS xabarnomalarini qo‘shmoqchi bo‘lsak, BookingService kodini o‘zgartirishimiz kerak bo‘lardi.

Buning o‘rniga BookingService konkret Email yoki SMS klassiga emas, NotificationSender interfeysiga bog‘lanishi kerak.

### 3. Bitta faylda juda ko‘p vazifalar jamlangan

Domain klasslari, booking logikasi, storage va notification logikasining barchasi bitta faylda joylashgan.

Bu kodni o‘qish, o‘zgartirish va qo‘llab-quvvatlashni qiyinlashtiradi. Bunday tuzilma Single Responsibility Principle (SRP) prinsipiga mos kelmaydi.

## Proof

- Refactoringdan oldin dastlabki testlar: 6/6 muvaffaqiyatli.
- R6 va SMS qo‘shilgandan keyingi testlar: 8/8 muvaffaqiyatli.
- Oddiy demo P03 dagi kabi aynan 9 qator natija chiqardi.
- Race demo dastlabki Double booking muammosini hali ham namoyish qilmoqda.