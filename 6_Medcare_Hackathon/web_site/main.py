from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from database import Database
from ai_service import GitHubModelsAI
from osms import OSMSService
from bot import API as bot_api
import os

app = Flask(__name__)
app.secret_key = Config.SESSION_SECRET

db = Database()
ai = GitHubModelsAI()
osms = OSMSService()

@app.route('/')
def index():
    return render_template('index.html', cache_buster=os.urandom(12).hex())

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = db.get_web_user(email)
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['email'] = email
        return jsonify({
            'success': True,
            'redirect': url_for('dashboard')
        })
    return jsonify({
        'success': False,
        'error': 'Неверный email или пароль'
    }), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    iin = data.get('iin')
    
    if db.get_web_user(email):
        return jsonify({
            'success': False,
            'error': 'Пользователь с таким email уже существует'
        }), 400
        
    password_hash = generate_password_hash(password)
    user_id = db.create_web_user(email, password_hash, name, iin)
    
    session['user_id'] = user_id
    session['email'] = email
    
    return jsonify({
        'success': True,
        'redirect': url_for('dashboard')
    })

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/user/link-telegram', methods=['POST'])
def link_telegram():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
        
    data = request.json
    telegram_id = data.get('telegram_id')
    
    if not telegram_id:
        return jsonify({'success': False, 'error': 'Не указан Telegram ID'}), 400
        
    db.link_telegram_to_web(session['user_id'], telegram_id)
    return jsonify({'success': True})

@app.route('/api/patients', methods=['GET'])
def get_patients():
    try:
        patients = db.get_patients()
        return jsonify({'success': True, 'patients': patients})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patients', methods=['POST'])
def add_patient():
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Не авторизован'}), 401
            
        data = request.json
        user_id = session['user_id']
        
    # Get user data
        user = db.get_web_user_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
        
        priority = 5
        temp = float(data.get('temperature', 0) or 0)
        hr = int(data.get('heart_rate', 0) or 0)
        br = int(data.get('breathing_rate', 0) or 0)
        
        if temp > 39 or hr > 120 or hr < 50 or br > 25 or br < 12:
            priority = 9
        elif temp > 38 or hr > 100 or hr < 60:
            priority = 6
        
        status = 'Критическое' if priority >= 8 else 'Срочно' if priority >= 5 else 'Плановое'
        
        ai_analysis = ai.analyze_patient(data)
        
        patient_data = {
            'name': data.get('name'),
            'age': data.get('age'),
            'iin': data.get('iin'),
            'temperature': temp if temp > 0 else None,
            'heart_rate': hr if hr > 0 else None,
            'breathing_rate': br if br > 0 else None,
            'symptoms': data.get('symptoms'),
            'priority': priority,
            'status': status,
            'ai_analysis': ai_analysis,
            'web_user_id': user_id,
            'telegram_user_id': user.get('telegram_user_id')
        }
        
    # Save patient
        patient_id = db.add_patient(patient_data)
        
    # If user has linked Telegram, send notification
        if patient_data['telegram_user_id']:
            appointment_data = {
                'telegram_user_id': patient_data['telegram_user_id'],
                'iin': patient_data['iin'],
                'specialist': data.get('specialist', 'Терапевт'),
                'appointment_date': data.get('appointment_date'),
                'appointment_time': data.get('appointment_time'),
                'patient_id': patient_id
            }
            # Sync with bot
            bot_api.sync_appointment_to_telegram(appointment_data)
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'ai_analysis': ai_analysis
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    try:
        success = db.delete_patient(patient_id)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        user_id = session.get('user_id', 'web_user')
        
        if not user_id:
            user_id = 'web_user'
            session['user_id'] = user_id
        
        db.save_chat_message(user_id, 'user', message)
        
        ai_response = ai.chat(message)
        
        db.save_chat_message(user_id, 'assistant', ai_response)
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/osms/calculate', methods=['POST'])
def calculate_osms():
    try:
        data = request.json
        income = float(data.get('income', 0))
        employment_status = data.get('employment_status', 'individual')
        services = data.get('services', [])
        
    # Calculate monthly payment
        monthly_payment = osms.calculate_payment(income, employment_status)
        
        # Calculate services cost and savings
        total_cost = 0
        for service in services:
            total_cost += osms.get_service_cost(service)
            
        # Get list of covered services
        covered_services = osms.get_covered_services('Застрахован')
        
        return jsonify({
            'success': True,
            'monthly_payment': monthly_payment,
            'services_cost': total_cost,
            'covered_services': covered_services
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/osms/status', methods=['GET'])
def check_osms_status():
    try:
        iin = request.args.get('iin')
        if not iin:
            return jsonify({'success': False, 'error': 'ИИН не указан'}), 400
            
        result = osms.check_osms_status(iin)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    try:
        user_id = session.get('user_id', 'web_user')
        history = db.get_chat_history(user_id)
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat():
    try:
        user_id = session.get('user_id', 'web_user')
        db.clear_chat_history(user_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def run_web():
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )

if __name__ == '__main__':
    run_web()
