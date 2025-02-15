from flask import Flask, render_template, request, redirect, url_for, flash
from membership_manager import MembershipManager

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
manager = MembershipManager()

@app.route('/')
def index():
    packages = manager.list_packages()
    members = manager.members
    return render_template('index.html', packages=packages, members=members)

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        member_id = request.form['member_id']
        name = request.form['name']
        package_type = request.form['package_type']
        
        try:
            manager.add_member(member_id, name, package_type)
            flash('Member added successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e), 'error')
    
    packages = manager.list_packages()
    return render_template('add_member.html', packages=packages)

@app.route('/member/<member_id>')
def member_info(member_id):
    member = manager.get_member_info(member_id)
    if member:
        return render_template('member_info.html', member=member)
    flash('Member not found!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 