# Sifat ssenariylari (Quality scenarios)

## Manfaatdor tomonlar (Stakeholders)

| Kim? | U nimaga ahamiyat beradi? |
|---|---|
| Guest (Mehmon) | Bo‘sh xonani tez topish va bron hech qachon yo‘qolmasligi. |
| Receptionist (Qabulxona xodimi) | Bir xonani ikki mehmonga va’da qilmaslik; bronni qabulxonada bekor qila olish. |
| Hotel manager (Mehmonxona menejeri, domain expert) | Biznes qoidalarini bilish; depozit va SMS imkoniyatlarini tez orada qo‘shish. |
| Development team (Dasturchilar jamoasi) | Bir biznes sohasini o‘zgartirganda boshqalarini buzmaslik. |
| Email/SMS va payment providers (Tashqi xizmatlar) | Tizim bilan integratsiya; xizmat sekin yoki ishlamay qolgan holatlarni hisobga olish. |

## S1 · Performance (Ishlash tezligi)

| Qism | S1 |
|---|---|
| Source (Manba) | 200 ta mehmon. |
| Stimulus (Ta’sir) | Ular 12–14 Nov sanalari uchun bo‘sh xonalarni qidiradi. |
| Environment (Sharoit) | Qidiruvlar bir daqiqa ichida amalga oshiriladi. |
| Artifact (Tizim qismi) | `BookingService.find_free_rooms` va unga kerakli xona/bron ma’lumotlari. |
| Response (Javob) | Tizim to‘g‘ri bo‘sh xonalar ro‘yxatini qaytaradi. |
| Measure (O‘lchov) | Javob vaqtining p95 qiymati 1 sekunddan oshmaydi (≤ 1 second). |
| Checked in (Qayerda tekshiriladi) | P08 (cache), P23 (load test). |

## S2 · Data integrity (Ma’lumotlar yaxlitligi)

| Qism | S2 |
|---|---|
| Source (Manba) | Bir vaqtda bron qilmoqchi bo‘lgan 100 juft mehmon. |
| Stimulus (Ta’sir) | Har bir juftlik bir xil xona va bir xil tunlar uchun bir vaqtda bron yuboradi. |
| Environment (Sharoit) | 100 ta juftlikning so‘rovlari bir vaqtda bajariladi. |
| Artifact (Tizim qismi) | `BookingService.reserve` va reservation storage. |
| Response (Javob) | Har bir juftlik uchun faqat bitta bron `Confirmed` bo‘ladi. |
| Measure (O‘lchov) | 0 ta double booking; har bir juftlikda aynan 1 ta `Confirmed` reservation. |
| Checked in (Qayerda tekshiriladi) | P09. |

## S3 · Availability (Mavjudlik)

| Qism | S3 |
|---|---|
| Source (Manba) | Email provider. |
| Stimulus (Ta’sir) | Email provider javob berishni to‘xtatadi. |
| Environment (Sharoit) | Oddiy bron jarayoni davomida xizmat 10 daqiqa ishlamaydi. |
| Artifact (Tizim qismi) | `BookingService.reserve` va notification sender. |
| Response (Javob) | Har bir yaroqli bron `Accepted` holatida saqlanadi; xabar yuborishdagi xatolik qayd etiladi. |
| Measure (O‘lchov) | 0 ta yo‘qolgan booking; muvaffaqiyatsiz xabarlarning barchasi hisobga olinadi. |
| Checked in (Qayerda tekshiriladi) | P04 (R6 testi, bajarilgan) va P10. |

## S4 · Security (Xavfsizlik)

| Qism | S4 |
|---|---|
| Source (Manba) | Boshqa mehmonning bronini ko‘rishga urinayotgan mehmon. |
| Stimulus (Ta’sir) | U boshqa mehmonning reservation ma’lumotlarini 100 marta o‘qishga urinadi. |
| Environment (Sharoit) | Tizimdan odatiy foydalanish vaqti; foydalanuvchi autentifikatsiyadan o‘tgan. |
| Artifact (Tizim qismi) | Reservation ma’lumotlarini ko‘rsatadigan API yoki application qismi. |
| Response (Javob) | Tizim boshqa mehmonning reservation ma’lumotlarini oshkor qilmaydi. |
| Measure (O‘lchov) | Noto‘g‘ri foydalanuvchiga ko‘rsatilgan reservationlar soni 0. |
| Checked in (Qayerda tekshiriladi) | P21. |

## S5 · Modifiability (O‘zgartirish qulayligi)

| Qism | S5 |
|---|---|
| Source (Manba) | Hotel manager (mehmonxona menejeri). |
| Stimulus (Ta’sir) | Tizimga SMS confirmation kanalini qo‘shishni so‘raydi. |
| Environment (Sharoit) | Mavjud email confirmation ishlashda davom etishi kerak. |
| Artifact (Tizim qismi) | Notification integratsiyasi va `BookingService`. |
| Response (Javob) | Yangi SMS sender qo‘shiladi; `BookingService` kodi o‘zgartirilmaydi. |
| Measure (O‘lchov) | `BookingService` o‘zgarmaydi; ko‘pi bilan 2 ta fayl o‘zgartiriladi. |
| Checked in (Qayerda tekshiriladi) | P04 (SMS sender, bajarilgan). |

## S6 · Sustainability (Energiya samaradorligi)

| Qism | S6 |
|---|---|
| Source (Manba) | Development team (dasturchilar jamoasi). |
| Stimulus (Ta’sir) | Bo‘sh xonalarni qidirish uchun bir xil 1 000 ta so‘rov bajariladi. |
| Environment (Sharoit) | Tizim o‘zgarishidan oldin va keyin bir xil sharoitda o‘lchanadi. |
| Artifact (Tizim qismi) | Free-room search va uni bajarishga sarflangan hisoblash resurslari. |
| Response (Javob) | Tizim qidiruvlarni kamroq energiya sarflab bajaradi. |
| Measure (O‘lchov) | Har 1 000 ta yakunlangan qidiruv uchun sarflangan energiya kamida 20% ga kamayadi. |
| Checked in (Qayerda tekshiriladi) | P08 va P24. |
