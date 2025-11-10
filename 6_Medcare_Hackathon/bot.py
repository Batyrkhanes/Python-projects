import logging
import qrcode
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import datetime
import sys

# CONSTANTS
SPECIALIST_NAME = "Specialist Name Here" 
SPECIALIST_ID = "AGM" 
INVISIBLE_TEXT = "." 
BOT_TOKEN = "BOT_TOKEN_Here" 

# CONTACTS (YOUR DETAILS)
SUPPORT_PHONE = "Phone_Number_Here"
SUPPORT_EMAIL = "Email_Address_Here"

# ADMIN PANEL CONSTANTS (CRM LITE)
ADMIN_PASSWORD = "07042009" 
ADMIN_ID = 12345678 # !!! IMPORTANT: REPLACE THIS ID WITH YOUR ACTUAL TELEGRAM ID

# LANGUAGE SUPPORT
TEXTS = {
    'kz': {
        'start_welcome': "Қош келдіңіз! Қызметтерді пайдалану үшін **12 саннан тұратын ЖСН-іңізді** енгізіңіз.",
        'iin_invalid': "❌ Қате. ЖСН 12 саннан тұруы керек.",
        'iin_success': "✅ Қош келдіңіз! Сіздің МӘМС мәртебеңіз: **{}**.",
        'main_menu_text': "➡️ **Бас мәзір.** Әрекетті таңдаңыз:",
        
        # Main Buttons
        'btn_appoint': "🗓️ Дәрігерге Жазылу",
        'btn_osms': "✅ МӘМС тексеру",
        'btn_analysis': "🔬 Анализдерім", 
        'btn_recipes': "💊 Рецепттерім (QR)",
        'btn_certs': "📄 Анықтамаларым (QR)",
        'btn_ticket_qr': "📃 Талонымды Көрсету (QR)",
        'btn_log': "📘 Журнал (Тарих)",
        'btn_tracker': "🩺 A51.Демалыс (Трекер)",
        'btn_lang': "🌐 Тілді Өзгерту",
        'btn_my_doctor': "👨‍⚕️ Менің Дәрігерім",
        'btn_help': "❓ Көмек / Байланыс", 
        'btn_back_main': "⬅️ Бас мәзірге",
        
        # Help Menu
        'help_menu_text': "**❓ Көмек және Байланыс**\n\nСұрақтарыңыз болса, бізбен хабарласыңыз:\n\n**📞 Телефон:** [{}](tel:{})\n**📧 E-mail:** `{}`\n\n*Назар аударыңыз: Бот тек ақпараттық қызмет көрсетеді.*".format(SUPPORT_PHONE, SUPPORT_PHONE, SUPPORT_EMAIL),
        
        # Admin Panel
        'admin_auth_start': "🛡️ **АДМИН-ПАНЕЛЬ.** Құпия сөзді енгізіңіз:",
        'admin_auth_success': "✅ Қатынау рұқсат етілді. Сіз админ-мәзірдесіз.",
        'admin_auth_failed': "❌ Қате құпия сөз немесе ID.",
        'admin_menu_text': "💼 **Админ-Мәзір.** Әрекетті таңдаңыз:",
        'btn_admin_appointments': "📝 Жазылуларды Қарау",
        'btn_admin_schedule': "⏰ Кестені Басқару (Mock)",
        'btn_admin_broadcast': "📣 Жаппай Жіберу",
        'btn_admin_analytics': "📊 Аналитика (Mock)",
        'btn_admin_back_main': "⬅️ Админкадан Шығу",
        'admin_appointments_list': "📝 **Жазылулар Тізімі ({count}):**\n\n{list}",
        'admin_no_appointments': "Белсенді жазылулар жоқ.",
        'admin_analytics_mock': "📊 **Аналитика (Mock):**\n\nБүгінгі жазылулар: 5\nЕң танымал дәрігер: AGM\nМӘМС тексерулер: 24",
        'admin_schedule_mock': "⏰ **Кестені Басқару (Mock):**\n\nКесте жаңартылды.\n(Нақты нұсқада: МИС-тегі слоттарды өзгерту үшін API-шақыру)",
        'admin_broadcast_prompt': "Жаппай жіберу үшін мәтінді енгізіңіз:",
        'admin_broadcast_success': "✅ Жаппай жіберу имитацияланды. Алушылар: {count}",
        
        # Other texts
        'my_doctor_info': "**👨‍⚕️ Учаскелік Дәрігер**\nАты-жөні: {name}\nКабинет №: {room}\nЖұмыс уақыты: {schedule}\nБайланыс: {phone}",
        'osms_menu_text': "**✅ МӘМС Қызметтері**",
        'osms_status': "Мәртебені Тексеру", 
        'osms_history': "Төлемдер Тарихы",
        'status_checked': "✅ МӘМС мәртебесі тексерілді:",
        'current_status': "Ағымдағы мәртебе: **{}**\nҚарыз (үлгі): `{}`",
        'payments_mock': "**🗓️ Төлемдер тарихы (Үлгі):**\n\n2025.10.05: 3500 KZT (Аударылды)\nЕскерту: Бұл тек үлгілік деректер.",
        'analysis_menu_text': "**🔬 Анализдерім.** Қажетті әрекетті таңдаңыз:", 
        'analysis_list': "Соңғы 5 анализ тізімі:", 
        'analysis_get_latest': "Соңғы нәтижені алу", 
        'analysis_not_found': "❌ Нәтиже табылмады. Қайта тексеріңіз.", 
        'analysis_data': "**🔬 Анализ №{id}**\n**Күні:** {date}\n**Түрі:** {type}\n**Нәтиже:** {result}\n**Комментарий:** {comment}", 
        'select_date': "**🗓️ Жазылу.** Дәрігерге баратын күнді таңдаңыз:",
        'select_time': f"**🗓️ {SPECIALIST_NAME} ({'{}'})**\n\nБос уақытты таңдаңыз:", 
        'booked_time': "❌ Бұл уақыт бос емес.",
        'appointment_success': "**✅ Сіз жазылдыңыз!** **Талон №{}**\nКүні/Уақыты: {} / {}\nДәрігер: {}",
        'no_appointment': "❌ **Қате: Талон табылмады.** Алдымен **'🗓️ Дәрігерге Жазылу'** батырмасы арқылы жазылыңыз.",
        'certificate_menu': "**📄 Менің Анықтамаларым**\n\nҚажетті анықтаманы таңдаңыз:",
        'cert_health': "Денсаулық туралы анықтама (QR)",
        'tracker_menu': "**🩺 А51. Ауру Демалысы Трекері**\n\nЕң соңғы ауру демалысы бойынша ақпарат:",
        'tracker_data': "**ID:** {}\n**Дәрігер:** {}\n**Басталған күні:** {}\n**Жарамдылық мерзімі:** {}\n**Диагноз (МКБ-10):** {}",
        'log_text': "**📘 Журнал (Соңғы әрекеттер)**\n\n{}",
        'unrecognized_command': "Түсініксіз сұрау. Әрекетті таңдаңыз немесе **'⚙️ Menu'** батырмасын басыңыз.",
    },
    'ru': {
        'start_welcome': "Добро пожаловать! Для использования сервисов введите **свой 12-значный ИИН**.",
        'iin_invalid': "❌ Ошибка. ИИН должен состоять из 12 цифр.",
        'iin_success': "✅ Добро пожаловать! Ваш статус ОСМС: **{}**.",
        'main_menu_text': "➡️ **Главное меню.** Выберите действие:",
        
        'btn_appoint': "🗓️ Запись к Врачу",
        'btn_osms': "✅ Проверка ОСМС",
        'btn_analysis': "🔬 Мои Анализы", 
        'btn_recipes': "💊 Мои Рецепты (QR)",
        'btn_certs': "📄 Мои Справки (QR)",
        'btn_ticket_qr': "📃 Показать Талон (QR)",
        'btn_log': "📘 Журнал (История)",
        'btn_tracker': "🩺 A51.Больничный (Трекер)",
        'btn_lang': "🌐 Изменить Язык",
        'btn_my_doctor': "👨‍⚕️ Мой Врач",
        'btn_help': "❓ Помощь / Контакты",
        'btn_back_main': "⬅️ В Главное меню",
        
        # Help Menu
        'help_menu_text': "**❓ Помощь и Контакты**\n\nЕсли у вас есть вопросы, свяжитесь с нами:\n\n**📞 Телефон:** [{}](tel:{})\n**📧 E-mail:** `{}`\n\n*Внимание: Бот предоставляет только информационные услуги.*".format(SUPPORT_PHONE, SUPPORT_PHONE, SUPPORT_EMAIL),

        # Admin Panel
        'admin_auth_start': "🛡️ **АДМИН-ПАНЕЛЬ.** Введите пароль:",
        'admin_auth_success': "✅ Доступ разрешен. Вы в админ-меню.",
        'admin_auth_failed': "❌ Неверный пароль или ID.",
        'admin_menu_text': "💼 **Админ-Меню.** Выберите действие:",
        'btn_admin_appointments': "📝 Просмотр Записей",
        'btn_admin_schedule': "⏰ Управление Расписанием (Mock)",
        'btn_admin_broadcast': "📣 Массовая Рассылка",
        'btn_admin_analytics': "📊 Аналитика (Mock)",
        'btn_admin_back_main': "⬅️ Выйти из Админки",
        'admin_appointments_list': "📝 **Список Записей ({count}):**\n\n{list}",
        'admin_no_appointments': "Нет активных записей.",
        'admin_analytics_mock': "📊 **Аналитика (Mock):**\n\nЗаписей за сегодня: 5\nСамый популярный врач: AGM\nПроверок ОСМС: 24",
        'admin_schedule_mock': "⏰ **Управление Расписанием (Mock):**\n\nРасписание обновлено.\n(В реальной версии: API-вызов для изменения слотов в МИС)",
        'admin_broadcast_prompt': "Введите текст для массовой рассылки:",
        'admin_broadcast_success': "✅ Рассылка имитирована. Получателей: {count}",
        
        # Other texts
        'my_doctor_info': "**👨‍⚕️ Участковый Врач**\nФИО: {name}\nКабинет №: {room}\nВремя работы: {schedule}\nКонтакты: {phone}",
        'osms_menu_text': "**✅ Услуги ОСМС**",
        'osms_status': "Проверить Статус", 
        'osms_history': "История Платежей",
        'status_checked': "✅ Статус ОСМС проверен:",
        'current_status': "Текущий статус: **{}**\nЗадолженность (mock): `{}`",
        'payments_mock': "**🗓️ История платежей (Mock):**\n\n2025.10.05: 3500 KZT (Переведено)\nПримечание: Это демонстрационные данные.",
        'analysis_menu_text': "**🔬 Мои Анализы.** Выберите необходимое действие:", 
        'analysis_list': "Список последних 5 анализов:", 
        'analysis_get_latest': "Получить последний результат", 
        'analysis_not_found': "❌ Результаты не найдены. Проверьте позже.", 
        'analysis_data': "**🔬 Анализ №{id}**\n**Дата:** {date}\n**Тип:** {type}\n**Результат:** {result}\n**Комментарий:** {comment}", 
        'select_date': "**🗓️ Запись.** Выберите дату приема к врачу:",
        'select_time': f"**🗓️ {SPECIALIST_NAME} ({'{}'})**\n\nВыберите свободный слот:",
        'booked_time': "❌ Это время занято.",
        'appointment_success': "**✅ Вы записаны!** **Талон №{}**\nДата/Время: {} / {}\nВрач: {}",
        'no_appointment': "❌ **Ошибка: Талон не найден.** Пожалуйста, сначала запишитесь через **'🗓️ Запись к Врачу'**.",
        'certificate_menu': "**📄 Мои Справки**\n\nВыберите необходимую справку:",
        'cert_health': "Справка о здоровье (QR)",
        'tracker_menu': "**🩺 А51. Трекер Больничных**\n\nИнформация по последнему больничному листу:",
        'tracker_data': "**ID:** {}\n**Врач:** {}\n**Дата начала:** {}\n**Действителен до:** {}\n**Диагноз (МКБ-10):** {}",
        'log_text': "**📘 Журнал (Последние действия)**\n\n{}",
        'unrecognized_command': "Неопознанный запрос. Выберите действие или нажмите **'⚙️ Menu'**.",
    },
    'en': {
        'start_welcome': "Welcome! Enter your 12-digit IIN.",
        'iin_invalid': "❌ Error. IIN must be 12 digits.",
        'iin_success': "✅ Welcome! Your OSMS status is: **{}**.",
        'main_menu_text': "➡️ **Main Menu.** Choose an action:",
        'btn_appoint': "🗓️ Book Appointment",
        'btn_osms': "✅ Check OSMS Status",
        'btn_analysis': "🔬 My Analysis", 
        'btn_recipes': "💊 My Prescriptions (QR)",
        'btn_certs': "📄 My Certificates (QR)",
        'btn_ticket_qr': "📃 Show Ticket (QR)",
        'btn_log': "📘 Log (History)",
        'btn_tracker': "🩺 A51.Sick Leave (Tracker)",
        'btn_lang': "🌐 Change Language",
        'btn_my_doctor': "👨‍⚕️ My Doctor",
        'btn_help': "❓ Help / Contacts",
        'btn_back_main': "⬅️ To Main Menu",
        
        # Help Menu
        'help_menu_text': "**❓ Help and Contacts**\n\nIf you have any questions, please contact us:\n\n**📞 Phone:** [{}](tel:{})\n**📧 E-mail:** `{}`\n\n*Note: The bot provides informational services only.*".format(SUPPORT_PHONE, SUPPORT_PHONE, SUPPORT_EMAIL),
        
        # Admin Panel
        'admin_auth_start': "🛡️ **ADMIN PANEL.** Enter password:",
        'admin_auth_success': "✅ Access granted. You are in the admin menu.",
        'admin_auth_failed': "❌ Incorrect password or ID.",
        'admin_menu_text': "💼 **Admin Menu.** Select action:",
        'btn_admin_appointments': "📝 View Appointments",
        'btn_admin_schedule': "⏰ Manage Schedule (Mock)",
        'btn_admin_broadcast': "📣 Mass Broadcast",
        'btn_admin_analytics': "📊 Analytics (Mock)",
        'btn_admin_back_main': "⬅️ Exit Admin Panel",
        'admin_appointments_list': "📝 **Appointment List ({count}):**\n\n{list}",
        'admin_no_appointments': "No active appointments.",
        'admin_analytics_mock': "📊 **Analytics (Mock):**\n\nAppointments today: 5\nMost popular doctor: AGM\nOSMS checks: 24",
        'admin_schedule_mock': "⏰ **Schedule Management (Mock):**\n\nSchedule updated.\n(In real version: API call to change slots in MIS)",
        'admin_broadcast_prompt': "Enter text for mass broadcast:",
        'admin_broadcast_success': "✅ Broadcast simulated. Recipients: {count}",
        
        'my_doctor_info': "**👨‍⚕️ District Doctor**\nFull Name: {name}\nRoom №: {room}\nSchedule: {schedule}\nContact: {phone}",
        'osms_menu_text': "**✅ OSMS Services**",
        'osms_status': "Check Status", 
        'osms_history': "Payment History",
        'status_checked': "✅ OSMS status checked:",
        'current_status': "Current status: **{}**\nDebt (mock): `{}`",
        'payments_mock': "**🗓️ Payment History (Mock):**\n\n2025.10.05: 3500 KZT (Paid)\nNote: This is mock data.",
        'analysis_menu_text': "**🔬 My Analysis.** Select the required action:", 
        'analysis_list': "List of last 5 analyses:", 
        'analysis_get_latest': "Get latest result", 
        'analysis_not_found': "❌ Results not found. Check again.", 
        'analysis_data': "**🔬 Analysis №{id}**\n**Date:** {date}\n**Type:** {type}\n**Result:** {result}\n**Comment:** {comment}", 
        'select_date': "**🗓️ Booking.** Select the date for your doctor's appointment:",
        'select_time': f"**🗓️ {SPECIALIST_NAME} ({'{}'})**\n\nSelect an available time slot:",
        'booked_time': "❌ This time slot is busy.",
        'appointment_success': "**✅ You are booked!** **Ticket №{}**\nDate/Time: {} / {}\nDoctor: {}",
        'no_appointment': "❌ **Error: Ticket not found.** Please book first via **'🗓️ Book Appointment'**.",
        'certificate_menu': "**📄 My Certificates**\n\nSelect the required certificate:",
        'cert_health': "Health Certificate (QR)",
        'tracker_menu': "**🩺 A51. Sick Leave Tracker**\n\nInformation on your last sick leave:",
        'tracker_data': "**ID:** {}\n**Doctor:** {}\n**Start Date:** {}\n**Valid until:** {}\n**Diagnosis (ICD-10):** {}",
        'log_text': "**📘 Log (Recent actions)**\n\n{}",
        'unrecognized_command': "Unrecognized request. Please select an action or press **'⚙️ Menu'**.",
    }
}

# MOCKUP API, DB_LOGS, DB_APPOINTMENTS
class MedserviceAPI:
    """OSMS class for healthcare services: insurance, appointments, prescriptions, certificates and health tracking. Simulates medical information system integration."""
    
    def __init__(self):
        self.mock_statuses = {
            '123456789012': {'status': 'Сақтандырылған', 'debt': '0 KZT', 'last_payment': '2025.10.01'},
            '000000000000': {'status': 'Сақтандырылмаған', 'debt': '17,500 KZT', 'last_payment': '2025.07.01'},
        }
        self.mock_analyses = [
            {'id': 'A005', 'date': '2025.11.01', 'type': 'Жалпы қан анализі', 'result': 'Норма', 'comment': 'Ешқандай ауытқулар жоқ.'},
            {'id': 'A004', 'date': '2025.10.25', 'type': 'Биохимиялық қан анализі', 'result': 'Жоғары', 'comment': 'Холестерин деңгейі жоғары.'},
            {'id': 'A003', 'date': '2025.10.10', 'type': 'Зәр анализі', 'result': 'Норма', 'comment': 'Бәрі қалыпты.'},
        ]
        self.mock_doctor_data = {
            'name': "Рахимжанова А.И.",
            'room': "103",
            'schedule': "Дс-Жм: 08:00 - 16:00",
            'phone': "8 (7172) 70-80-80"
        }

    # MAIN API CALLS
    def check_osms_status(self, iin: str) -> dict:
        if len(iin) != 12 or not iin.isdigit():
            return {'success': False, 'message': 'ЖСН форматы дұрыс емес.'}
        if iin in self.mock_statuses:
            return {'success': True, 'data': self.mock_statuses[iin]}
        else:
            return {'success': True, 'data': {'status': 'Сақтандырылған', 'debt': '0 KZT', 'last_payment': '2025.11.01'}}
            
    def issue_appointment(self, iin: str, specialist_id: str, date: str, time: str) -> dict:
        specialist = SPECIALIST_NAME if specialist_id == SPECIALIST_ID else "Белгісіз маман"
        return {
            'success': True,
            'data': {
                'id': f"{time.replace(':', '')}{datetime.datetime.now().second}",
                'date': date, 'time': time, 'specialist': specialist, 'mo': '№5 Қалалық емхана'
            }
        }
        
    def get_available_slots(self, specialist_id: str, date: str) -> list:
        try:
            date_obj = datetime.datetime.strptime(date, '%Y.%m.%d').date()
            if date_obj >= (datetime.date.today() + datetime.timedelta(days=1)):
                return [{'time': '09:00', 'available': True, 'id': 'T900'}, {'time': '09:30', 'available': True, 'id': 'T930'}, {'time': '10:00', 'available': False, 'id': 'T1000'}, {'time': '10:30', 'available': True, 'id': 'T1030'}]
        except ValueError:
            pass 
        return []

    # Other mock functions
    def get_last_prescription(self, iin: str) -> dict:
        return {'prescription_id': 'RX-987654', 'doctor': SPECIALIST_NAME, 'date': datetime.date.today().strftime('%Y.%m.%d'),
                'medications': [{'name': 'Парацетамол', 'dosage': '500 мг', 'instruction': '1 таб. x 3 рет/күн'}], 'pharmacy_code': 'KZ-PHARMA-101'}

    def get_analyses_list(self, iin: str, limit: int = 5) -> list:
        return self.mock_analyses[:limit]

    def get_analysis_result(self, iin: str, analysis_id: str = None) -> dict:
        if self.mock_analyses:
            return self.mock_analyses[0]
        return {}

    def issue_health_certificate(self, iin: str) -> dict:
        return {'certificate_id': 'CERT-0042-KZ', 'doctor': SPECIALIST_NAME,
                'issue_date': datetime.date.today().strftime('%Y.%m.%d'),
                'valid_until': (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y.%m.%d'),
                'type': 'Жұқпалы аурумен контакті жоқ туралы', 'status': 'ДЕНІ САУ'}
    
    def get_a51_tracker(self, iin: str) -> dict:
        return {'tracker_id': 'A51-2025-001', 'doctor': SPECIALIST_NAME,
                'start_date': (datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y.%m.%d'),
                'valid_until': (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y.%m.%d'),
                'diagnosis': 'J02.9 Жұқпалы фарингит'}

    def get_my_doctor_info(self, iin: str) -> dict: 
        return self.mock_doctor_data

    # NEW METHODS FOR MEDICAL SYSTEM INTEGRATION (MOCK)
    def sync_appointment_to_mis(self, appointment_data: dict) -> bool:
        """Имитирует отправку новой записи в МИС клиники."""
        print(f"MIS SYNC: Отправлена новая запись - {appointment_data}")
        return True 
        
    def sync_cancel_to_mis(self, appointment_id: str) -> bool:
        """Имитирует отправку отмены записи в МИС."""
        print(f"MIS SYNC: Отправлена отмена талона ID - {appointment_id}")
        return True 

    def update_schedule_via_mis(self, specialist_id: str, new_schedule: dict) -> bool:
        """Имитирует обновление расписания врачей через API."""
        print(f"MIS CONTROL: Расписание врача {specialist_id} обновлено.")
        return True 
    
API = MedserviceAPI()

# Data storage (Mock DB: Only languages, appointments and logs)
DB_USERS_LANG = {} 
DB_APPOINTMENTS = {} 
DB_LOGS = {} 

def get_text(user_id, key):
    lang = DB_USERS_LANG.get(user_id, 'kz')
    return TEXTS[lang].get(key, TEXTS['kz'].get(key, f"<{key} аудармасы жоқ>"))

def add_log(user_id, action):
    if user_id not in DB_LOGS: DB_LOGS[user_id] = []
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    DB_LOGS[user_id].insert(0, f"[{timestamp}] {action}")
    if len(DB_LOGS[user_id]) > 10: DB_LOGS[user_id].pop()

# MAIN ACTIONS (START, IIN, MENU)

async def send_main_menu_message(update: Update, context, chat_id: int) -> None:
    """Sends the main menu as a new message."""
    user_id = context.user_data['user_id']
    T = lambda key: get_text(user_id, key)
    
    keyboard = [
        [InlineKeyboardButton(T('btn_appoint'), callback_data='select_specialist'), 
         InlineKeyboardButton(T('btn_osms'), callback_data='osms_menu')],
        [InlineKeyboardButton(T('btn_analysis'), callback_data='analysis_menu'), 
         InlineKeyboardButton(T('btn_recipes'), callback_data='show_medicines')],
        [InlineKeyboardButton(T('btn_my_doctor'), callback_data='show_my_doctor'), 
         InlineKeyboardButton(T('btn_certs'), callback_data='show_certificate_menu')],
        [InlineKeyboardButton(T('btn_tracker'), callback_data='show_a51_tracker'), 
         InlineKeyboardButton(T('btn_log'), callback_data='show_log')],
        [InlineKeyboardButton(T('btn_ticket_qr'), callback_data='show_qr_ticket')],
        [InlineKeyboardButton(T('btn_help'), callback_data='show_help_menu')],
        [InlineKeyboardButton(T('btn_lang'), callback_data='lang_menu')],
    ]
    reply_markup_inline = InlineKeyboardMarkup(keyboard)
    reply_markup_menu = ReplyKeyboardMarkup([[KeyboardButton("⚙️ Menu")]], resize_keyboard=True)
    text_to_send = T('main_menu_text')
    
    await context.bot.send_message(chat_id, text_to_send, reply_markup=reply_markup_inline, parse_mode='Markdown')
    await context.bot.send_message(chat_id, INVISIBLE_TEXT, reply_markup=reply_markup_menu)


async def start(update: Update, context) -> None:
    """Welcome message and request for IIN (Individual Identification Number)."""
    user_id = update.effective_user.id
    context.user_data['user_id'] = user_id
    if context.user_data.get('iin'):
        return await main_menu(update, context)

    if user_id not in DB_USERS_LANG:
        DB_USERS_LANG[user_id] = 'kz'

    await update.message.reply_text(
        get_text(user_id, 'start_welcome'),
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )

async def main_menu(update: Update, context) -> None:
    """Shows the main menu."""
    user_id = update.effective_user.id
    context.user_data['user_id'] = user_id
    T = lambda key: get_text(user_id, key)
    
    if not context.user_data.get('iin'):
        if update.callback_query: await update.callback_query.answer("❌ Авторизация қажет.")
        return await start(update, context)
        
    keyboard = [
        [InlineKeyboardButton(T('btn_appoint'), callback_data='select_specialist'), 
         InlineKeyboardButton(T('btn_osms'), callback_data='osms_menu')],
        [InlineKeyboardButton(T('btn_analysis'), callback_data='analysis_menu'), 
         InlineKeyboardButton(T('btn_recipes'), callback_data='show_medicines')],
        [InlineKeyboardButton(T('btn_my_doctor'), callback_data='show_my_doctor'), 
         InlineKeyboardButton(T('btn_certs'), callback_data='show_certificate_menu')],
        [InlineKeyboardButton(T('btn_tracker'), callback_data='show_a51_tracker'), 
         InlineKeyboardButton(T('btn_log'), callback_data='show_log')],
        [InlineKeyboardButton(T('btn_ticket_qr'), callback_data='show_qr_ticket')],
        [InlineKeyboardButton(T('btn_help'), callback_data='show_help_menu')],
        [InlineKeyboardButton(T('btn_lang'), callback_data='lang_menu')],
    ]
    reply_markup_inline = InlineKeyboardMarkup(keyboard)
    text_to_send = T('main_menu_text')

    if update.callback_query:
        try:
             await update.callback_query.edit_message_text(text_to_send, reply_markup=reply_markup_inline, parse_mode='Markdown')
        except Exception:
             await send_main_menu_message(update, context, update.callback_query.message.chat_id)
    else:
        await send_main_menu_message(update, context, update.message.chat_id)

# ADMIN PANEL AND MAIN TEXT HANDLING

async def handle_admin_password(update: Update, context) -> None:
    """Validates admin password, broadcast text or IIN."""
    user_id = update.effective_user.id
    T = lambda key: get_text(user_id, key)
    
    # 1. Handling broadcast text
    if context.user_data.get('state') == 'awaiting_broadcast_text':
        return await admin_send_broadcast(update, context)
    
    # 2. Handling admin password
    if context.user_data.get('state') == 'awaiting_admin_password':
        password = update.message.text.strip()
        context.user_data['state'] = None # Reset state
        
        if password == ADMIN_PASSWORD or user_id == ADMIN_ID:
            context.user_data['is_admin'] = True
            await update.message.reply_text(T('admin_auth_success'), parse_mode='Markdown')
            return await show_admin_menu(update, context, new_message=True)
        else:
            await update.message.reply_text(T('admin_auth_failed'), parse_mode='Markdown')
            return await main_menu(update, context) 

    # 3. Handling other texts/IIN
    text = update.message.text.strip()
    context.user_data['user_id'] = user_id

    if text == '⚙️ Menu':
        return await main_menu(update, context)

    if not context.user_data.get('iin'):
        iin = text
        if not (iin.isdigit() and len(iin) == 12):
            await update.message.reply_text(T('iin_invalid'), parse_mode='Markdown')
            return

        api_response = API.check_osms_status(iin)
        if not api_response['success']:
            await update.message.reply_text(f"❌ Қате: {api_response['message']}")
            return

        status_data = api_response['data']
        context.user_data['iin'] = iin
        context.user_data['osms_data'] = status_data
        
        add_log(user_id, "ЖСН арқылы авторизацияланды")
        
        await update.message.reply_text(T('iin_success').format(status_data['status']), parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
        return await main_menu(update, context)
    
    if context.user_data.get('iin'):
        await update.message.reply_text(T('unrecognized_command'), parse_mode='Markdown')


async def admin_start(update: Update, context) -> None:
    """Entry point to admin panel."""
    user_id = update.effective_user.id
    context.user_data['user_id'] = user_id
    
    # If ID matches super-admin, log in immediately
    if user_id == ADMIN_ID:
        T = lambda key: get_text(user_id, key)
        await update.message.reply_text(T('admin_auth_success'), parse_mode='Markdown')
        return await show_admin_menu(update, context, new_message=True)
    
    # Парольді сұрау
    context.user_data['state'] = 'awaiting_admin_password'
    await update.message.reply_text(get_text(user_id, 'admin_auth_start'), parse_mode='Markdown')

async def show_admin_menu(update: Update, context, new_message=False) -> None:
    """Показывает главное меню администратора. ИСПРАВЛЕНА ОШИБКА TypeError: CallbackQuery.edit_message_text()."""
    user_id = context.user_data.get('user_id'); T = lambda key: get_text(user_id, key)
    
    keyboard = [
        [InlineKeyboardButton(T('btn_admin_appointments'), callback_data='admin_show_appointments')],
        [InlineKeyboardButton(T('btn_admin_schedule'), callback_data='admin_schedule_mock')],
        [InlineKeyboardButton(T('btn_admin_broadcast'), callback_data='admin_broadcast_prompt_start')],
        [InlineKeyboardButton(T('btn_admin_analytics'), callback_data='admin_analytics_mock')],
        [InlineKeyboardButton(T('btn_admin_back_main'), callback_data='back_to_main')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if new_message or update.callback_query:
        if update.callback_query: 
            await update.callback_query.answer()
            # 1. CASE: EDITING (edit_message_text does not require chat_id)
            await update.callback_query.edit_message_text(
                text=T('admin_menu_text'),
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            # 2. CASE: NEW MESSAGE (send_message requires chat_id)
            chat_id = update.effective_chat.id
            await context.bot.send_message(
                chat_id=chat_id,
                text=T('admin_menu_text'),
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )

async def admin_show_appointments(update: Update, context) -> None:
    """Барлық активті жазылуларды көрсетеді."""
    query = update.callback_query; await query.answer()
    user_id = context.user_data.get('user_id'); T = lambda key: get_text(user_id, key)
    
    appointments_list = []
    count = 0
    
    all_user_data = context.application.user_data
    
    for patient_id, appointments in DB_APPOINTMENTS.items():
        if appointments:
            last_app = appointments[-1]
            iin = all_user_data.get(patient_id, {}).get('iin', 'N/A')
            
            try:
                app_date = datetime.datetime.strptime(last_app['date'], '%Y.%m.%d').date()
                if app_date >= datetime.date.today():
                    count += 1
                    appointments_list.append(f"• Талон {last_app['id']} | ИИН: {iin} | {last_app['date']} {last_app['time']} ({last_app['specialist']})")
            except ValueError:
                pass 
            
    list_output = "\n".join(appointments_list)
    text = T('admin_appointments_list').format(
        count=count, 
        list=list_output if count > 0 else T('admin_no_appointments')
    )
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='admin_menu')]]), parse_mode='Markdown')

async def admin_schedule_mock(update: Update, context) -> None:
    """Кестені басқару API-ын имитациялайды."""
    query = update.callback_query; await query.answer()
    user_id = context.user_data.get('user_id'); T = lambda key: get_text(user_id, key)
    
    API.update_schedule_via_mis(SPECIALIST_ID, {'new_slots': ['11:00', '11:30']})
    
    await query.edit_message_text(T('admin_schedule_mock'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='admin_menu')]]), parse_mode='Markdown')

async def admin_analytics_mock(update: Update, context) -> None:
    """Аналитикалық есептерді имитациялайды."""
    query = update.callback_query; await query.answer()
    user_id = context.user_data.get('user_id'); T = lambda key: get_text(user_id, key)
    await query.edit_message_text(T('admin_analytics_mock'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='admin_menu')]]), parse_mode='Markdown')

async def admin_broadcast_prompt_start(update: Update, context) -> None:
    """Рассылка мәтінін сұрайды."""
    query = update.callback_query; await query.answer()
    user_id = context.user_data.get('user_id'); T = lambda key: get_text(user_id, key)
    
    context.user_data['state'] = 'awaiting_broadcast_text'
    
    await query.edit_message_text(T('admin_broadcast_prompt'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ " + T('btn_back_main'), callback_data='admin_menu')]]))

async def admin_send_broadcast(update: Update, context) -> None:
    """Жаппай рассылканы имитациялайды."""
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    broadcast_text = update.message.text
    
    user_count = len(DB_USERS_LANG)
    
    text = T('admin_broadcast_success').format(count=user_count)
    context.user_data['state'] = 'admin_menu' 
    
    await update.message.reply_text(text, parse_mode='Markdown')
    await show_admin_menu(update, context, new_message=True) 

# OTHER SERVICES (INSURANCE, APPOINTMENTS, TESTS, QR-CODE)

async def show_my_doctor(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    iin = context.user_data.get('iin', 'mock')
    doctor_data = API.get_my_doctor_info(iin)
    text = T('my_doctor_info').format(**doctor_data)
    add_log(user_id, "Учаскелік дәрігер туралы ақпаратты қарады")
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]), parse_mode='Markdown')

async def show_help_menu(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    text = T('help_menu_text')
    add_log(user_id, "Көмек және байланыс ақпаратын сұрады")
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]), parse_mode='Markdown')

async def lang_menu(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    keyboard = [[InlineKeyboardButton("Қазақша 🇰🇿", callback_data='set_lang_kz')],
                [InlineKeyboardButton("Русский 🇷🇺", callback_data='set_lang_ru')],
                [InlineKeyboardButton("English 🇬🇧", callback_data='set_lang_en')],
                [InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]
    await query.edit_message_text("🌐 Тілді таңдаңыз / Выберите язык / Select language:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def set_language(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; lang = query.data.split('_')[-1]
    DB_USERS_LANG[user_id] = lang
    add_log(user_id, f"Тілді {lang} тіліне ауыстырды")
    await main_menu(update, context)

async def select_specialist(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    keyboard = []; today = datetime.date.today()
    
    for i in range(1, 4): 
        date = today + datetime.timedelta(days=i)
        date_str = date.strftime('%Y.%m.%d')
        keyboard.append([InlineKeyboardButton(f"🗓️ {date_str}", callback_data=f'select_date_{SPECIALIST_ID}_{date_str}')])

    keyboard.append([InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(T('select_date'), reply_markup=reply_markup, parse_mode='Markdown')

async def show_time_table(update: Update, context, data_parts: list) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    
    _, _, specialist_id, date = data_parts
    slots = API.get_available_slots(specialist_id, date) 
    keyboard = []; current_row = []
    
    for slot in slots:
        button_text = slot['time']
        callback_data = f"book_{specialist_id}_{date}_{slot['time']}" if slot['available'] else "ignore"
        if not slot['available']: button_text += " ❌"
        current_row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        if len(current_row) == 4: keyboard.append(current_row); current_row = []
    if current_row: keyboard.append(current_row)
    
    keyboard.append([InlineKeyboardButton("⬅️ Күн таңдауға", callback_data='select_specialist')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(T('select_time').format(date), reply_markup=reply_markup, parse_mode='Markdown')
    
async def book_appointment(update: Update, context, data_parts: list) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    iin = context.user_data['iin']
    
    _, specialist_id, date, time = data_parts 

    api_response = API.issue_appointment(iin, specialist_id, date, time) 
    new_appointment = api_response['data']
    DB_APPOINTMENTS.setdefault(user_id, []).append(new_appointment)
    
    # Simulating MIS integration
    API.sync_appointment_to_mis(new_appointment) 
    
    add_log(user_id, f"{new_appointment['specialist']} дәрігеріне {date} күні {time} уақытына жазылды")

    text = T('appointment_success').format(new_appointment['id'], new_appointment['date'], new_appointment['time'], new_appointment['specialist'])
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_ticket_qr'), callback_data='show_qr_ticket')],
                                           [InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]),
        parse_mode='Markdown'
    )

async def osms_service_menu(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    keyboard = [[InlineKeyboardButton(T('osms_status'), callback_data='check_status_action')], 
                [InlineKeyboardButton(T('osms_history'), callback_data='osms_payments_history_mock')], 
                [InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]
    await query.edit_message_text(T('osms_menu_text'), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def check_status_action(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    status_data = context.user_data['osms_data'] 
    text = T('status_checked') + "\n\n" + T('current_status').format(status_data['status'], status_data['debt'])
    add_log(user_id, f"МӘМС мәртебесін тексерді: {status_data['status']}")
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Артқа", callback_data='osms_menu')]]), parse_mode='Markdown')

async def show_mock_payments(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    add_log(user_id, "Төлемдер тарихын қарады (Үлгі)")
    await query.edit_message_text(T('payments_mock'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Артқа", callback_data='osms_menu')]]), parse_mode='Markdown')

async def analysis_menu(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    keyboard = [[InlineKeyboardButton(T('analysis_get_latest'), callback_data='get_latest_analysis')],
                [InlineKeyboardButton(T('analysis_list'), callback_data='list_analyses')], 
                [InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]
    await query.edit_message_text(T('analysis_menu_text'), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def get_latest_analysis(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    iin = context.user_data['iin']
    latest_result = API.get_analysis_result(iin)
    if latest_result:
        text = T('analysis_data').format(**latest_result)
        add_log(user_id, f"Соңғы анализ нәтижесін алды ({latest_result['id']})")
    else:
        text = T('analysis_not_found')
        add_log(user_id, "Анализ нәтижесі табылмады")
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Артқа", callback_data='analysis_menu')]]), parse_mode='Markdown')

async def list_analyses(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    iin = context.user_data['iin']
    analyses = API.get_analyses_list(iin)
    if analyses:
        analysis_texts = []
        for a in analyses:
            analysis_texts.append(f"• **{a['date']}** ({a['type']}): {a['result']}")
        list_output = T('analysis_list') + "\n" + "\n".join(analysis_texts)
        add_log(user_id, "Соңғы анализдер тізімін қарады")
    else:
        list_output = T('analysis_not_found')
        add_log(user_id, "Анализдер тізімі табылмады")
    await query.edit_message_text(list_output, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Артқа", callback_data='analysis_menu')]]), parse_mode='Markdown')

async def show_medicines_qr(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    iin = context.user_data['iin'] 
    prescription_data = API.get_last_prescription(iin); 
    meds_list = "\n".join([f"- {m['name']}: {m['dosage']} ({m['instruction']})" for m in prescription_data['medications']])
    qr_text_data = (f"Рецепт ID: {prescription_data['prescription_id']}; ЖСН: {iin}")
    qr = qrcode.QRCode(version=1, box_size=10, border=4); qr.add_data(qr_text_data); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white"); img_byte_arr = BytesIO(); img.save(img_byte_arr, format='PNG'); img_byte_arr.seek(0)
    caption_text = (f"**💊 Сіздің Электронды Рецептіңіз**\n**Рецепт №{prescription_data['prescription_id']}**\nДәрігер: {prescription_data['doctor']}\n{meds_list}")
    add_log(user_id, "Рецепт QR-кодын көрсетті (Бір жол)")
    reply_markup_inline = InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]])
    await query.message.delete()
    await context.bot.send_photo(chat_id=query.message.chat_id, photo=img_byte_arr, caption=caption_text, reply_markup=reply_markup_inline, parse_mode='Markdown')
    
async def show_certificate_menu(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    keyboard = [[InlineKeyboardButton(T('cert_health'), callback_data='show_certificate_qr')],
                [InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]
    await query.edit_message_text(T('certificate_menu'), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def show_certificate_qr(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    iin = context.user_data['iin'] 
    certificate_data = API.issue_health_certificate(iin)
    qr_text_data = (f"Анықтама ID: {certificate_data['certificate_id']}; ЖСН: {iin}; Түрі: {certificate_data['type']}")
    qr = qrcode.QRCode(version=1, box_size=10, border=4); qr.add_data(qr_text_data); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white"); img_byte_arr = BytesIO(); img.save(img_byte_arr, format='PNG'); img_byte_arr.seek(0)
    caption_text = (f"**📄 Сіздің Анықтамаңыз**\nҚұжат ID: `{certificate_data['certificate_id']}`\nТүрі: {certificate_data['type']}\nЖарамдылық мерзімі: {certificate_data['valid_until']}")
    add_log(user_id, "Анықтама QR-кодын көрсетті (Бір жол)")
    reply_markup_inline = InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]])
    await query.message.delete()
    await context.bot.send_photo(chat_id=query.message.chat_id, photo=img_byte_arr, caption=caption_text, reply_markup=reply_markup_inline, parse_mode='Markdown')

async def show_a51_tracker(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    iin = context.user_data['iin']
    tracker_data = API.get_a51_tracker(iin)
    text = T('tracker_menu') + "\n\n" + T('tracker_data').format(tracker_data['tracker_id'], tracker_data['doctor'], tracker_data['start_date'], tracker_data['valid_until'], tracker_data['diagnosis'])
    add_log(user_id, "Ауру демалысы трекерін қарады")
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]), parse_mode='Markdown')

async def show_log(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    log_entries = DB_LOGS.get(user_id, [])
    log_text_formatted = "\n".join(log_entries)
    text = T('log_text').format(log_text_formatted if log_text_formatted else "Журнал таза.")
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]]), parse_mode='Markdown')

async def show_qr_ticket(update: Update, context) -> None:
    query = update.callback_query; await query.answer()
    user_id = update.effective_user.id; T = lambda key: get_text(user_id, key)
    last_appointment = DB_APPOINTMENTS.get(user_id)
    if not last_appointment:
        await query.edit_message_text(T('no_appointment'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_appoint'), callback_data='select_specialist')]]), parse_mode='Markdown')
        add_log(user_id, "Талонды көрсету әрекеті (табылмады)")
        return
    appointment = last_appointment[-1] 
    qr_text_data = (f"Талон №{appointment['id']}; Дәрігер: {appointment['specialist']}; Күні: {appointment['date']}; Уақыты: {appointment['time']}")
    qr = qrcode.QRCode(version=1, box_size=10, border=4); qr.add_data(qr_text_data); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white"); img_byte_arr = BytesIO(); img.save(img_byte_arr, format='PNG'); img_byte_arr.seek(0)
    caption_text = T('appointment_success').format(appointment['id'], appointment['date'], appointment['time'], appointment['specialist'])
    add_log(user_id, f"Талон QR-кодын көрсетті (№{appointment['id']})")
    reply_markup_inline = InlineKeyboardMarkup([[InlineKeyboardButton(T('btn_back_main'), callback_data='back_to_main')]])
    await query.message.delete()
    await context.bot.send_photo(chat_id=query.message.chat_id, photo=img_byte_arr, caption=caption_text, reply_markup=reply_markup_inline, parse_mode='Markdown')

# CALLBACK QUERY HANDLING

async def handle_callback_query(update: Update, context) -> None:
    """Main function for handling all callback queries."""
    query = update.callback_query
    data = query.data
    user_id = update.effective_user.id
    
    # Check authorization (considering admin callbacks and language switching)
    if context.user_data.get('iin') is None and not data.startswith('set_lang_') and data not in ['lang_menu', 'back_to_main', 'admin_menu']:
        await query.answer(get_text(user_id, 'iin_invalid'), show_alert=True)
        return

    data_parts = data.split('_')
    
    # Return and Language switching
    if data == 'back_to_main':
        return await main_menu(update, context)
    elif data == 'lang_menu':
        return await lang_menu(update, context)
    elif data.startswith('set_lang_'):
        return await set_language(update, context)
        
    # Admin Panel
    elif data == 'admin_menu':
        return await show_admin_menu(update, context)
    elif data == 'admin_show_appointments':
        return await admin_show_appointments(update, context)
    elif data == 'admin_schedule_mock':
        return await admin_schedule_mock(update, context)
    elif data == 'admin_analytics_mock':
        return await admin_analytics_mock(update, context)
    elif data == 'admin_broadcast_prompt_start':
        return await admin_broadcast_prompt_start(update, context)

    # Appointment Services
    elif data == 'select_specialist':
        return await select_specialist(update, context)
    elif data.startswith('select_date_'):
        return await show_time_table(update, context, data_parts)
    elif data.startswith('book_'):
        if data == 'ignore':
            await query.answer(get_text(user_id, 'booked_time'), show_alert=True)
            return
        return await book_appointment(update, context, data_parts)

    # Insurance Services
    elif data == 'osms_menu':
        return await osms_service_menu(update, context)
    elif data == 'check_status_action':
        return await check_status_action(update, context)
    elif data == 'osms_payments_history_mock':
        return await show_mock_payments(update, context)
        
    # Medical Tests
    elif data == 'analysis_menu':
        return await analysis_menu(update, context)
    elif data == 'get_latest_analysis':
        return await get_latest_analysis(update, context)
    elif data == 'list_analyses':
        return await list_analyses(update, context)

    # Prescriptions, Appointments, Certificates (QR)
    elif data == 'show_medicines': 
        return await show_medicines_qr(update, context)
    elif data == 'show_qr_ticket': 
        return await show_qr_ticket(update, context)
    elif data == 'show_certificate_menu':
        return await show_certificate_menu(update, context)
    elif data == 'show_certificate_qr':
        return await show_certificate_qr(update, context)
        
    # Others
    elif data == 'show_my_doctor':
        return await show_my_doctor(update, context)
    elif data == 'show_a51_tracker':
        return await show_a51_tracker(update, context)
    elif data == 'show_log':
        return await show_log(update, context)
    elif data == 'show_help_menu':
        return await show_help_menu(update, context)
    
    else:
        await query.answer(f"Белгісіз әрекет: {data}")
        add_log(user_id, f"Белгісіз callback әрекеті: {data}")


# APPLICATION RUN
if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    try:
        application = Application.builder().token(BOT_TOKEN).build()

        # Handlers
        application.add_handler(CommandHandler("start", start))
        
        # Initialize Admin Panel
        application.add_handler(CommandHandler("admin", admin_start)) 
        
        application.add_handler(CallbackQueryHandler(handle_callback_query))
        
        # Handler for all text messages (IIN, Password, Broadcast text)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_password)) 

        logger.info("Telegram Bot started successfully. Polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES, stop_signals=None)

    except Exception as e:
        logger.error(f"Failed to run Telegram Bot: {e}")
        sys.exit(1)
