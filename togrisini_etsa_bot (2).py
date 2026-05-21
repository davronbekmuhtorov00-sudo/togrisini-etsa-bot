import anthropic
import schedule
import time
import asyncio
import random
from telegram import Bot

# ============================================================
#   TOGRISINI ETSA — AVTOMATIK POST BOT
#   Kanal: @togrisini_etsa
#   Kuniga 10 ta post — har xil mavzuda
# ============================================================

BOT_TOKEN = "8807998942:AAGsAvXIuCOH2PM-9x2XKRGFtB9aThYqxZo"
CHANNEL_ID = "@togrisini_etsa"
CLAUDE_API_KEY = "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"  # <-- shu yerga yozing

# ============================================================
#   15 TA MAVZU — har kuni 10 tasi tasodifiy tanlanadi
# ============================================================

MAVZULAR = [
    "pul va boylik — odamlar buni ochiqchasiga gapirmaydi, lekin hammaning miyasida",
    "do'stlik va xiyonat — yaqin odamlar ba'zan eng katta dushman bo'ladi",
    "ota-ona va farzand munosabatlari — sevgi bor, lekin og'riq ham ko'p",
    "jamiyatda ikki yuzlamalik — ko'chada bir xil, uyda boshqacha odamlar",
    "sevgi va nikoh haqida haqiqat — romantiка emas, haqiqiy hayot",
    "ish va karyera — muvaffaqiyat uchun nima kerak, nima kerak emas",
    "vaqt va umr — yoshligimizda anglolmaydigan narsalar",
    "o'zbek mentaliteti — yaxshi tomonlari ham bor, yomon tomonlari ham",
    "muvaffaqiyatsizlik va qayta turish — yiqilganlar haqida hech kim gapirilmaydi",
    "odamlarning qilig'i — kuzatsang, ko'p narsa ko'rinadi",
    "sog'liq va hayot tarzi — e'tibor bermasak keyin afsus qilamiz",
    "orzu va maqsad — ba'zilar orzu qiladi, ba'zilar harakat qiladi",
    "yolg'iz qolish va o'z-o'zini topish — bu yomon narsa emas",
    "pul topish yo'llari va aldovlar — ko'pchilik bu haqda bilmaydi",
    "hayotda tanlov — har bir qaror keyingi 5 yilni belgilaydi",
    "yosh va tajriba — 20 yoshda va 40 yoshda dunyoni boshqacha ko'rasan",
    "insoniy munosabatlarda chegara qo'yish — nima uchun bu muhim",
    "ijtimoiy tarmoqlar va haqiqiy hayot — ko'rsatiladigan va yashiriladigan narsa",
    "maktab va ta'lim — bizga nima o'rgatdi, nima o'rgatmadi",
    "erkaklar va ayollar munosabatidagi haqiqatlar — ikki tomondan ham",
]

# ============================================================
#   KUNLIK 10 POSTNING VAQTLARI
# ============================================================

VAQTLAR = [
    "07:00",  # 1 — Erta tong, odamlar uyg'onayotgan vaqt
    "09:00",  # 2 — Ish boshlanganda
    "10:30",  # 3 — Choy vaqti
    "12:00",  # 4 — Tushlik
    "13:30",  # 5 — Tushdan keyin
    "15:00",  # 6 — Kechki qism boshlandi
    "17:00",  # 7 — Ish tugayapti
    "19:00",  # 8 — Kechki ovqat
    "21:00",  # 9 — Dam olish vaqti
    "22:30",  # 10 — Yotishdan oldin
]

# Bugungi mavzular — har kuni yangilanadi
bugungi_mavzular = []


def mavzularni_yangilash():
    """Har kuni ertalab 10 ta mavzu tanlanadi"""
    global bugungi_mavzular
    bugungi_mavzular = random.sample(MAVZULAR, 10)
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M')}] Bugungi 10 mavzu tanlandi:")
    for i, m in enumerate(bugungi_mavzular, 1):
        print(f"  {i}. {m[:50]}...")


def post_yarat(mavzu, post_raqami):
    """AI yordamida yangi post yaratadi"""
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    # Vaqtga qarab kayfiyat
    soat = int(time.strftime("%H"))
    if soat < 9:
        kayfiyat = "erta tong — o'ylantiradigan, chuqur"
    elif soat < 12:
        kayfiyat = "ertalab — energetik, harakatga undovchi"
    elif soat < 15:
        kayfiyat = "tush — amaliy, foydali maslahat"
    elif soat < 18:
        kayfiyat = "kechki qism — kuzatuv, hayotiy tajriba"
    elif soat < 21:
        kayfiyat = "kechqurun — samimiy, hissiyotli"
    else:
        kayfiyat = "kech kechqurun — falsafiy, chuqur o'ylash"

    prompt = f"""Sen "Тоғрисини этсам" Telegram kanali uchun post yozayapsan.

KANAL RUHI:
- Ism: "Тоғрисини этсам" — ya'ni "to'g'risini aytadigan bo'lsam"
- Uslub: oddiy odam gapirganday, lekin keskin va haqiqiy
- Na maqtov, na yolg'on — faqat ko'pchilik biladi lekin aytishdan qo'rqadi degan narsalar
- O'quvchi "ha, aniq shunday!" deb o'ylashi kerak

BUGUNGI POST #{post_raqami}:
Mavzu: {mavzu}
Vaqt kayfiyati: {kayfiyat}

POST TALABLARI:
- 180-250 so'z
- Birinchi jumla — to'xtatib o'ylatadigan, "voy" dedirtiradigan
- O'rtada — konkret misol yoki hayotiy holat
- Oxirda — savol yoki fikr (o'quvchi komment yozgisi kelsin)
- 2-4 emoji (ortiqcha emas)
- 3-4 hashtag: #togrisini #haqiqat va mavzuga mos
- O'zbek tili, lotin alifbosi
- Faqat post matnini yoz"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=700,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


# Post raqamini kuzatish
post_raqami_hisoblagich = [0]


async def post_yuborish():
    """Postni Telegram kanaliga yuboradi"""
    global bugungi_mavzular

    if not bugungi_mavzular:
        mavzularni_yangilash()

    post_raqami_hisoblagich[0] += 1
    raqam = post_raqami_hisoblagich[0]

    # Mavzu tanlash (10 tagacha ketma-ket, keyin qayta)
    mavzu_index = (raqam - 1) % 10
    mavzu = bugungi_mavzular[mavzu_index]

    try:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M')}] Post #{raqam} yaratilmoqda...")
        print(f"  Mavzu: {mavzu[:60]}...")

        matn = post_yarat(mavzu, raqam)

        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=matn,
            parse_mode="HTML"
        )
        print(f"[{time.strftime('%Y-%m-%d %H:%M')}] ✓ Post #{raqam} yuborildi!")

    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M')}] ✗ Xatolik (Post #{raqam}): {e}")


def ishga_tushir():
    asyncio.run(post_yuborish())


# ============================================================
#   JADVAL SOZLASH
# ============================================================

# Har kuni ertalab mavzularni yangilash
schedule.every().day.at("06:55").do(mavzularni_yangilash)

# 10 ta post vaqtlari
for vaqt in VAQTLAR:
    schedule.every().day.at(vaqt).do(ishga_tushir)


# ============================================================
#   ISHGA TUSHIRISH
# ============================================================

if __name__ == "__main__":
    print("=" * 55)
    print("   ТОҒРИСИНИ ЭТСАМ — BOT ISHGA TUSHDI")
    print("=" * 55)
    print(f"   Kanal  : {CHANNEL_ID}")
    print(f"   Kuniga : 10 ta post")
    print(f"   Vaqtlar: {' | '.join(VAQTLAR)}")
    print(f"   Mavzular: {len(MAVZULAR)} ta havza ichidan 10 tasi")
    print("=" * 55)
    print("   To'xtatish: Ctrl+C")
    print()

    # Dastur ishga tushganda mavzularni yuklash
    mavzularni_yangilash()

    # Ixtiyoriy: hozir darhol bitta test post yuborish
    # Quyidagi izohni olib tashlang (#) test uchun:
    # ishga_tushir()

    while True:
        schedule.run_pending()
        time.sleep(30)
