from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from app.models import ShoppingList, db
from app.utils import parse_multiple_entries
from app import auth

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@auth.login_required
def index():
    lists = ShoppingList.query.order_by(ShoppingList.created_at.desc()).all()
    
    organized = {}
    for lst in lists:
        year = lst.created_at.year
        month = lst.created_at.month
        day = lst.created_at.day
        
        if year not in organized:
            organized[year] = {}
        if month not in organized[year]:
            organized[year][month] = {}
        if day not in organized[year][month]:
            organized[year][month][day] = []
            
        organized[year][month][day].append(lst)
    
    return render_template('index.html', organized=organized)

@main_bp.route('/create', methods=['GET', 'POST'])
@auth.login_required
def create():
    if request.method == 'POST':
        entries = request.form.get('entries')
        checked_states = request.form.get('checked_states')
        if entries:
            new_list = ShoppingList(entries=entries, checked_states=checked_states)
            db.session.add(new_list)
            db.session.commit()
            return redirect(url_for('main.index'))
    
    return render_template('create.html')

@main_bp.route('/create/multiple', methods=['GET', 'POST'])
@auth.login_required
def create_multiple():
    if request.method == 'POST':
        text = request.form.get('text')
        delimiter = request.form.get('delimiter', ',')
        entries = parse_multiple_entries(text, delimiter)
        
        if entries:
            new_list = ShoppingList(entries=entries)
            db.session.add(new_list)
            db.session.commit()
            return redirect(url_for('main.index'))
    
    return render_template('create_multiple.html')

@main_bp.route('/delete_list/<int:list_id>', methods=['POST'])
@auth.login_required
def delete_list(list_id):
    lst = ShoppingList.query.get_or_404(list_id)
    db.session.delete(lst)
    db.session.commit()
    
    # For AJAX requests (entry deletion), return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True}), 200
    # For regular form submission (Delete button), redirect
    else:
        return redirect(url_for('main.index'))

@main_bp.route('/update_entry/<int:list_id>/<int:entry_index>', methods=['POST'])
@auth.login_required
def update_entry(list_id, entry_index):
    lst = ShoppingList.query.get_or_404(list_id)
    entries = lst.entries.split('\n')
    
    if 0 <= entry_index < len(entries):
        entry = entries[entry_index].strip()
        if entry.startswith('- ['):
            # Get the checked state from the request
            data = request.get_json()
            new_state = '[x]' if data.get('checked', False) else '[ ]'
            
            # Update the entry
            if '[ ]' in entry:
                entries[entry_index] = entry.replace('[ ]', new_state)
            elif '[x]' in entry:
                entries[entry_index] = entry.replace('[x]', new_state)
            
            # Save to database
            lst.entries = '\n'.join(entries)
            db.session.commit()
            return jsonify(success=True)
    
    return jsonify(success=False), 400

@main_bp.route('/edit/<int:list_id>', methods=['GET', 'POST'])
@auth.login_required
def edit_list(list_id):
    lst = ShoppingList.query.get_or_404(list_id)
    
    if request.method == 'POST':
        entries = request.form.get('entries')
        new_date = request.form.get('date')
        
        if entries:
            lst.entries = entries
            if new_date:
                try:
                    lst.created_at = datetime.strptime(new_date, '%Y-%m-%d')
                except ValueError:
                    pass
            db.session.commit()
            return redirect(url_for('main.view_list', 
                                year=lst.created_at.year,
                                month=lst.created_at.month,
                                day=lst.created_at.day))
    
    return render_template('edit_list.html', lst=lst)

@main_bp.route('/settings')
@auth.login_required
def settings():
    return render_template('settings.html')

@main_bp.route('/list/<int:year>/<int:month>/<int:day>')
def view_list(year, month, day):
    # Get all lists for the specific day
    start_date = datetime(year, month, day)
    end_date = datetime(year, month, day + 1) if day < 31 else datetime(year, month + 1, 1)
    
    lists = ShoppingList.query.filter(
        ShoppingList.created_at >= start_date,
        ShoppingList.created_at < end_date
    ).order_by(ShoppingList.created_at.desc()).all()
    
    return render_template('view_list.html', lists=lists, date=start_date)
