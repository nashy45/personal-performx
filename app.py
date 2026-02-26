from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task, Goal
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" 

db.init_app(app)


with app.app_context():
    db.create_all()
    print("✅ All tables created successfully!")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(full_name=full_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!")
        return redirect(url_for('register'))

    return render_template('register.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password")

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks, goals=goals)

@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']

        new_task = Task(
            title=title,
            description=description,
            due_date=datetime.strptime(due_date, '%Y-%m-%d'),
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!")
        return redirect(url_for('dashboard'))

    return render_template('add_task.html')

@app.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        target_date = request.form['target_date']

        new_goal = Goal(
            title=title,
            description=description,
            target_date=datetime.strptime(target_date, '%Y-%m-%d'),
            user_id=current_user.id
        )
        db.session.add(new_goal)
        db.session.commit()
        flash("Goal added successfully!")
        return redirect(url_for('dashboard'))

    return render_template('add_goal.html')

@app.route('/complete_task/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Not authorized!")
        return redirect(url_for('dashboard'))

    task.completed = True
    db.session.commit()
    flash("Task marked as complete!")
    return redirect(url_for('dashboard'))

@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Not authorized!")
        return redirect(url_for('dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!")
    return redirect(url_for('dashboard'))
 
@app.route('/delete_goal/<int:goal_id>')
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        flash("Not authorized!")
        return redirect(url_for('dashboard'))

    db.session.delete(goal)
    db.session.commit()
    flash("Goal deleted!")
    return redirect(url_for('dashboard'))

def goal_completion(goal):
    from datetime import date
    total_days = (goal.target_date.date() - date.today()).days
    progress = 100 - max(min(total_days, 100), 0)
    return progress

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)