from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.services.membership_service import MembershipService
from functools import wraps
import uuid

bp = Blueprint('main', __name__)
membership_service = MembershipService()

# Password for the application
APP_PASSWORD = "voyo4ever"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == APP_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('main.index'))
        flash('Nesprávné heslo')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('main.login'))

@bp.route('/')
@login_required
def index():
    """Hlavní stránka s kalkulačkou"""
    return render_template('index.html', plans=membership_service.list_plans())

@bp.route('/calculate-change', methods=['POST'])
@login_required
def calculate_change():
    """Endpoint pro výpočet změny plánu"""
    try:
        data = request.json
        
        # Validace vstupních dat
        if not data.get('current_plan'):
            return jsonify({'error': 'Chybí současný plán'}), 400
            
        if not data.get('start_date'):
            return jsonify({'error': 'Chybí datum začátku'}), 400

        # Generování unikátního ID pro dočasný výpočet
        temp_id = str(uuid.uuid4())

        # Vytvoření dočasného člena pro výpočet
        temp_member = membership_service.add_member(
            member_id=temp_id,
            name='temp',
            plan_type=data['current_plan'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
            has_package=data.get('has_package', False)
        )

        try:
            # Pokud jde o změnu plánu
            if data.get('new_plan') and data.get('change_date'):
                result = membership_service.calculate_plan_change(
                    temp_id,
                    data['new_plan'],
                    datetime.strptime(data['change_date'], '%Y-%m-%d'),
                    wants_package=data.get('wants_package', False)
                )
                # Convert Decimal objects to strings for JSON serialization
                return jsonify({
                    'current_plan': result['current_plan'],
                    'current_plan_name': result['current_plan_name'],
                    'new_plan': result['new_plan'],
                    'new_plan_name': result['new_plan_name'],
                    'days_used': result['days_used'],
                    'days_remaining': result['days_remaining'],
                    'refund_amount': str(result['refund_amount']),
                    'plan_refund': str(result['plan_refund']),
                    'package_refund': str(result['package_refund']),
                    'new_plan_price': str(result['new_plan_price']),
                    'final_price': str(result['final_price']),
                    'daily_plan_rate': str(result['daily_plan_rate']),
                    'current_plan_price': str(result['current_plan_price']),
                    'package_price': str(result['package_price'])
                })
            
            # Pokud jde o novou registraci
            result = membership_service.calculate_initial_price(
                data['current_plan'],
                data.get('has_package', False),
                data['start_date']
            )
            return jsonify({
                'plan_price': str(result['plan_price']),
                'package_price': str(result['package_price']),
                'total': str(result['total'])
            })
        finally:
            # Vyčištění dočasného člena
            if temp_id in membership_service.members:
                del membership_service.members[temp_id]
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Neočekávaná chyba: {str(e)}'}), 500

@bp.route('/member/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        member_id = request.form['member_id']
        name = request.form['name']
        package_type = request.form['package_type']
        
        try:
            membership_service.add_member(member_id, name, package_type)
            flash('Member added successfully!', 'success')
            return redirect(url_for('main.index'))
        except ValueError as e:
            flash(str(e), 'error')
    
    return render_template('add_member.html', packages=membership_service.list_packages())

@bp.route('/member/<member_id>')
def member_info(member_id):
    member = membership_service.get_member_info(member_id)
    if member:
        return render_template('member_info.html', member=member)
    flash('Member not found!', 'error')
    return redirect(url_for('main.index')) 