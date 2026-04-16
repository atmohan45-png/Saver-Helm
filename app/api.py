from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Helmet, Reading
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/data', methods=['POST'])
def post_data():
    data = request.get_json()
    print("📥 Received from ESP32:", data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    helmet_id = data.get('helmet_id')
    temp = data.get('temperature')
    gas = data.get('gas')
    battery = data.get('battery', 100.0)

    if not helmet_id or temp is None or gas is None:
        return jsonify({"error": "Missing required fields"}), 400

    helmet = Helmet.query.filter_by(helmet_id=helmet_id).first()
    if not helmet:
        return jsonify({"error": "Helmet not found"}), 404

    # Update Helmet health
    helmet.battery_level = float(battery)
    helmet.last_seen = datetime.utcnow()

    new_reading = Reading(helmet_id=helmet_id, temperature=temp, gas=gas)
    db.session.add(new_reading)
    db.session.commit()

    return jsonify({"status": "ok"}), 201

@api.route('/latest-data', methods=['GET'])
@login_required
def get_latest_data():
    # Global visibility: All helmets are visible to everyone
    helmets = Helmet.query.all()
    output = []
    for h in helmets:
        latest = h.get_latest_reading()
        # Online if seen in last 30 seconds
        is_online = (datetime.utcnow() - h.last_seen).total_seconds() < 30 if h.last_seen else False
        
        output.append({
            "helmet_id": h.helmet_id,
            "helmet_name": h.helmet_name,
            "worker_name": h.worker_name,
            "temperature": latest.temperature if latest else 0,
            "gas": latest.gas if latest else 0,
            "status": "danger" if (latest and latest.gas > 650) else "safe",
            "last_updated": latest.timestamp.strftime('%Y-%m-%d %H:%M:%S') if latest else "N/A",
            "battery": h.battery_level,
            "is_online": is_online,
            "is_admin": current_user.is_admin # Include admin status for UI logic
        })
    return jsonify(output)

@api.route('/analytics-data', methods=['GET'])
@login_required
def get_analytics_data():
    # Global visibility: Show trends for all helmets
    helmets = Helmet.query.all()
    result = {}
    for h in helmets:
        readings = Reading.query.filter_by(helmet_id=h.helmet_id).order_by(Reading.timestamp.desc()).limit(20).all()
        readings.reverse() # Chronological
        result[h.helmet_name] = {
            "labels": [r.timestamp.strftime('%H:%M') for r in readings],
            "temp": [r.temperature for r in readings],
            "gas": [r.gas for r in readings]
        }
    return jsonify(result)

@api.route('/history/<h_id>', methods=['GET'])
@login_required
def get_helmet_history(h_id):
    helmet = Helmet.query.filter_by(helmet_id=h_id, user_id=current_user.id).first_or_404()
    readings = Reading.query.filter_by(helmet_id=h_id).order_by(Reading.timestamp.desc()).limit(50).all()
    output = []
    for r in readings:
        output.append({
            "timestamp": r.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": r.temperature,
            "gas": r.gas
        })
    return jsonify(output)
