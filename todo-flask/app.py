from flask import Flask, render_template, request, redirect, session,flash
from connection import insert,find,find_one,delete_one,update_one
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'twinklemehta'
@app.route('/')
def index():
    if 'username' in session:
        todos = find("todos",{'user_id': session['user_id']})
        return render_template('index.html', todos=todos)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = find_one('users',{'username': username})
        if existing_user:
            flash('Username already exists', 'error')
            return redirect('/register')

        hashed_password = generate_password_hash(password)
        user_id = insert('users',{'username': username, 'password': hashed_password}).inserted_id
        session['user_id'] = str(user_id)
        session['username'] = username

        return redirect('/')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = find_one('users',{'username': username})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            return redirect('/')

        flash('Incorrect username or password', 'error')

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/add', methods=['POST'])
def add():
    if 'user_id' in session:
        title = request.form['title']
        description = request.form['description']
        status = 'pending'
        user_id = session['user_id']
        insert('todos', {'title': title, 'description': description,'status': status, 'user_id': user_id})
    return redirect('/')


@app.route('/delete/<todo_id>')
def delete(todo_id):
    if 'user_id' in session:
        delete_one('todos',{'_id': ObjectId(todo_id)})
    return redirect('/')

@app.route('/edit/<todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    if 'user_id' in session:
        todo = find_one('todos',{'_id': ObjectId(todo_id)})
        if request.method == 'POST':
            updated_title = request.form['title']
            updated_description = request.form['description']
            update_one('todos',{'_id': ObjectId(todo_id)}, {'$set': {'title': updated_title,'description':updated_description}})
            return redirect('/')
        return render_template('edit.html', todo=todo)
    return redirect('/')


@app.route('/update/<todo_id>', methods=['GET', 'POST'])
def update(todo_id):
    if 'user_id' in session:
        todo = find_one('todos',{'_id': ObjectId(todo_id)})
        if request.method == 'POST':
            status = request.form['status']
            update_one('todos',{'_id': ObjectId(todo_id)}, {'$set': {'status': status}})
            return redirect('/')
        return render_template('update.html', todo=todo)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
