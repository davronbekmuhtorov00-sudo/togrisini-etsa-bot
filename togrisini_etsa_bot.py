import os
import schedule
import time
import asyncio
import random
from telegram import Bot
import google.generativeai as genai

BOT_TOKEN = "8807998942:AAGsAvXIuCOH2PM-9x2XKRGFtB9aThYqxZo"
CHANNEL_ID = "@togrisini_etsa"

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

MAVZULAR = [
    "пул ва бойлик — одамлар буни очиқчасига гапирмайди, лекин ҳамманинг миясида",
    "дўстлик ва хиёнат — яқин одамлар баъзан энг катта душман бўлади",
    "ота-она ва фарзанд муносабатлари — севги бор, лекин оғриқ ҳам кўп",
    "камиятда икки юзламалик — кўчада бир хил, уйда бошқача одамлар",
    "севги ва никоҳ ҳақида ҳақиқат — романтика эмас, ҳақиқий ҳаёт",
    "иш ва карьера — муваффақият учун нима керак, нима керак эмас",
    "вақт ва умр — ёшлигимизда англолмайдиган нарсалар",
    "ўзбек менталитети — яхши томонлари ҳам бор, ёмон томонлари ҳам",
    "муваффақиятсизлик ва қайта туриш — йиқилганлар ҳақида ҳеч ким гапирмайди",
    "одамларнинг қилиғи — кузатсанг, кўп нарса кўринади",
    "соғлиқ ва ҳаёт тарзи — эътибор бермасак кейин афсус қиламиз",
    "орзу ва мақсад — баъзилар орзу қилади, баъзилар ҳаракат қилади",
    "ёлғиз қолиш ва ўз-ўзини топиш — бу ёмон нарса эмас",
    "пул топиш йўллари ва алдовлар — кўпчилик бу ҳақда билмайди",
    "ҳаётда танлов — ҳар бир қарор кейинги 5 йилни белгилайди",
    "ёш ва тажриба — 20 ёшда ва 40 ёшда дунёни бошқача кўрасан",
    "инсоний муносабатларда чегара қўйиш — нима учун бу муҳим",
    "ижтимоий тармоқлар ва ҳақиқий ҳаёт — кўрсатиладиган ва яширилаган нарса",
    "мактаб ва таълим — бизга нима ўргатди, нима ўргатмади",
    "эркаклар ва аёллар муносабаттидаги ҳақиқатлар — икки томондан ҳам",
    "ишонч ва алданиш — одамларга ишонишнинг нархи",
    "бахт нима — кўпчилик нотўғри жойдан қидиради",
    "мақтов ва танқид — ортингдан гапиришади, юзингга эса бошқача",
    "пул ва дўстлик — пул борида дўст кўп, йўқида ҳеч ким йўқ",
    "ҳаётнинг ўтиши — кеча бола эдинг, бугун ўзинг ҳам билмайсан қаерга кетаётганингни",
]

bot = Bot(token=BOT_TOKEN)
bugungi_mavzular = []

def mavzularni_yangilash():
    global bugungi_mavzular
    bugungi_mavzular = random.sample(MAVZULAR, 15)
    print(f"[{time.strftime('%H:%M')}] 15 та мавзу танланди.")

def post_yarat(mavzu):
    # 'gemini-1.5-flash' o'rniga 'gemini-1.5-flash-001' yoki shunchaki 'gemini-1.5-flash' ni tekshirib ko'ring
    # Agar baribir 404 chiqsa, demak API kalitingizda cheklov bor.
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    prompt = f"""Сен Telegram канали учун жуда қисқа (20-25 сўз), аччиқ ҳақиқатларни ёзувчи ботсан.
    
    ҚАТЪИЙ ТАЛАБЛАР:
    1. Жуда муҳим: Постни ҳеч қачон "Тоғрисини этсам" ёки "Тоғрисини айтганда" иборалари билан БОШЛАМА!
    2. Постни тўғридан-тўғри мавзунинг ўзидан ёки фикрдан бошла.
    3. СТИКЕР ИШЛАТМА!
    4. Ўзбек тилида, кирилл алифбосида ёз.
    5. Мавзу: {mavzu}
    6. Охирида #тогрисини #хакикат хаштагларини қўй."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

async def post_yuborish_async():
    global bugungi_mavzular
    if not bugungi_mavzular: mavzularni_yangilash()
    mavzu = bugungi_mavzular.pop(0)
    try:
        matn = post_yarat(mavzu)
        await bot.send_message(chat_id=CHANNEL_ID, text=matn)
        print(f"✅ Пост муваффақиятли кетди: {mavzu[:20]}")
    except Exception as e:
        print(f"❌ XATOLIK YUZ BERDI: {str(e)}")

def ishga_tushir():
    asyncio.run(post_yuborish_async())

if __name__ == "__main__":
    print("Бот ишга тушди...")
    mavzularni_yangilash()
    
    # ТЕСТ УЧУН: Бот ишга тушгандан 10 сония ўтиб битта пост синов тариқасида юборади
    print("TEST: 10 сониядан сўнг биринчи пост юборилади...")
    asyncio.run(post_yuborish_async())
    
    # Jadval - 15 ta vaqtni qaytardik
    schedule.every().day.at("06:55").do(mavzularni_yangilash)
    
    vaqtlar_listi = ["07:00", "08:40", "10:00", "11:30", "13:00", "14:30", 
                     "16:00", "17:30", "19:00", "20:30", "21:30", "22:30", 
                     "23:30", "00:30", "02:00"]
    
    for vaqt in vaqtlar_listi:
        schedule.every().day.at(vaqt).do(ishga_tushir)

    while True:
        schedule.run_pending()
        time.sleep(30)
