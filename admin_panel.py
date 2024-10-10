from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['space_claw_game']

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    user = db.admins.find_one({'username': username})
    if not user:
        return None
    return User(username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.admins.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            login_user(User(username))
            return redirect(url_for('admin_dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    prizes = db.prizes.find()
    users = db.users.find().sort('score', -1).limit(10)
    return render_template('admin_dashboard.html', prizes=prizes, users=users)

@app.route('/admin/prize', methods=['POST'])
@login_required
def update_prize():
    prize_id = request.form['prize_id']
    new_stock = int(request.form['stock'])
    new_probability = float(request.form['probability'])
    db.prizes.update_one({'_id': prize_id}, {'$set': {'stock': new_stock, 'probability': new_probability}})
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/user', methods=['POST'])
@login_required
def update_user():
    user_id = request.form['user_id']
    new_score = int(request.form['score'])
    db.users.update_one({'_id': user_id}, {'$set': {'score': new_score}})
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)