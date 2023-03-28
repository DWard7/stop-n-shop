from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.user_model import User

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register/user')
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    if not User.register_validation(request.form):
        return redirect('/')
    data={
        **request.form,
        'user_name':request.form['user_name'],
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':bcrypt.generate_password_hash(request.form['password']),
        'confirm_password':bcrypt.generate_password_hash(request.form['confirm_password'])
        }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/home')

@app.route("/login", methods=["POST"])
def login_validation():
    found_user = User.login_validation(request.form)
    found_user = User.get_by_email(request.form)
    if not found_user:
        return redirect("/")
    session["user_id"] = found_user.id
    print(request.form)
    return redirect("/home")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")