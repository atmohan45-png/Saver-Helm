from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import db, User, Helmet, Reading
import os
from datetime import datetime
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@main.route('/manage-helmets', methods=['GET', 'POST'])
@login_required
def manage_helmets():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            h_id = request.form.get('helmet_id')
            h_name = request.form.get('helmet_name')
            w_name = request.form.get('worker_name')
            loc = request.form.get('location')
            e_contact = request.form.get('emergency_contact')
            b_group = request.form.get('blood_group')
            
            existing = Helmet.query.filter_by(helmet_id=h_id).first()
            if existing:
                flash('Helmet ID already exists')
            else:
                new_h = Helmet(
                    helmet_id=h_id, 
                    helmet_name=h_name, 
                    worker_name=w_name, 
                    location=loc, 
                    user_id=current_user.id,
                    emergency_contact=e_contact,
                    blood_group=b_group
                )
                db.session.add(new_h)
                db.session.commit()
                flash('Helmet added successfully')
        
        elif action == 'delete':
            h_id = request.form.get('helmet_id')
            h = Helmet.query.filter_by(helmet_id=h_id, user_id=current_user.id).first()
            if h:
                Reading.query.filter_by(helmet_id=h_id).delete()
                db.session.delete(h)
                db.session.commit()
                flash('Helmet deleted')

    helmets = Helmet.query.all()
    return render_template('manage_helmets.html', helmets=helmets)

@main.route('/helmet/<h_id>')
@login_required
def helmet_history(h_id):
    helmet = Helmet.query.filter_by(helmet_id=h_id).first_or_404()
    readings = Reading.query.filter_by(helmet_id=h_id).order_by(Reading.timestamp.desc()).limit(50).all()
    return render_template('history.html', helmet=helmet, readings=readings)

@main.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

@main.route('/emergency-logs')
@login_required
def emergency_logs():
    helmets = Helmet.query.all()
    return render_template('emergency_logs.html', helmets=helmets)

@main.route('/device-status')
@login_required
def device_status():
    helmets = Helmet.query.all()
    return render_template('device_status.html', helmets=helmets, datetime=datetime)

@main.route('/control-panel')
@login_required
def control_panel():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    return render_template('admin.html', users=users)

@main.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # Handle Profile Picture
        file = request.files.get('profile_pic')
        if file and allowed_file(file.filename):
            filename = secure_filename(f"user_{user.id}_{file.filename}")
            upload_path = os.path.join('app', 'static', 'uploads')
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, filename))
            user.profile_pic = filename

        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.dob = request.form.get('dob')
        user.gender = request.form.get('gender')
        
        password = request.form.get('password')
        if password:
            user.set_password(password)
            
        db.session.commit()
        flash(f'Profile for {user.username} updated.')
        return redirect(url_for('main.control_panel'))
        
    return render_template('admin_edit_user.html', user=user)

@main.route('/admin/delete-user/<int:user_id>')
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if current_user.id == user_id:
        flash('You cannot delete your own admin account.', 'warning')
        return redirect(url_for('main.control_panel'))
        
    user = User.query.get_or_404(user_id)
    # Delete related helmets first
    Helmet.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash(f'Account for {user.username} has been permanently deleted.', 'success')
    return redirect(url_for('main.control_panel'))

@main.route('/edit-helmet/<h_id>', methods=['GET', 'POST'])
@login_required
def edit_helmet(h_id):
    if not current_user.is_admin:
        flash('Only administrators can edit helmets.', 'error')
        return redirect(url_for('main.dashboard'))
        
    helmet = Helmet.query.filter_by(helmet_id=h_id).first_or_404()
    if request.method == 'POST':
        helmet.helmet_name = request.form.get('helmet_name')
        helmet.worker_name = request.form.get('worker_name')
        helmet.location = request.form.get('location')
        helmet.emergency_contact = request.form.get('emergency_contact')
        helmet.blood_group = request.form.get('blood_group')
        
        db.session.commit()
        flash('Helmet details updated.', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('edit_helmet.html', helmet=helmet)

@main.route('/delete-helmet/<h_id>')
@login_required
def delete_helmet(h_id):
    if not current_user.is_admin:
        flash('Only administrators can delete helmets.', 'error')
        return redirect(url_for('main.dashboard'))
        
    h = Helmet.query.filter_by(helmet_id=h_id).first_or_404()
    Reading.query.filter_by(helmet_id=h_id).delete()
    db.session.delete(h)
    db.session.commit()
    flash('Helmet removed successfully.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        password = request.form.get('password')

        # Handle Profile Picture
        file = request.files.get('profile_pic')
        if file and allowed_file(file.filename):
            filename = secure_filename(f"user_{current_user.id}_{file.filename}")
            upload_path = os.path.join('app', 'static', 'uploads')
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, filename))
            current_user.profile_pic = filename

        current_user.username = username
        current_user.email = email
        current_user.dob = dob
        current_user.gender = gender
        
        if password:
            current_user.set_password(password)
        
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html', user=current_user)
