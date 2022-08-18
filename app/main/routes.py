from flask import session, redirect, url_for, render_template, request, flash
from . import main
from .forms import LoginForm
from app import list_users

@main.route('/', methods=['GET', 'POST'])
def index():

    print('***----------------index----------------***')
    print(list_users)

    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            # if user is logged
            if session.get('name'):
                # if the user wrote a different name
                if session.get('name') != form.name.data:
                    form.name.data = session.get('name')
                    print('this user is already login')
                    flash('To change you Nickname you must logout', 'warning')
            else:
                exists = form.name.data in list_users
                # if the name the user wrote is already taken
                if exists:
                    form.name.data = ''
                    print('this name exist in list_users')
                    flash('This Nickname had been taken, please chose another one', 'warning')
                else:
                    # login the user
                    session['name'] = form.name.data
                
                    print('validation true')
                    flash(session['name']+ ' Welcome!!', 'success')
            
            # create or update 'session room' (to enable switch betewn rooms)
            try:
                session['room'] = request.form['room']
            except:
                print('error, my be request.form[room] must be not exists')
        else:
            print('validation false')
            flash(form.name.errors[0], 'warning')

    if request.method == 'GET':
        if session.get('name'):
            form.name.data =  session['name']
        else:
            
            if not len(list_users):
                flash('Hi, write your Nickname and press Go!!', 'success')
            else:
                flash('Hi, write your Nickname and select one user to start!!', 'success')


    return render_template('index.html', form=form)


@main.route('/left', methods=['GET'])
def left():
    print('***----------------left GET----------------***')

    # remove the 'sesion name' and 'sesion room' (logout the user)
    try:
        session.pop('name')
        session.pop('room')
    except:
        print('error, the session values must be empty')

    print(session.get('name'))

    return redirect(url_for('main.index'))

@main.route('/leave-room', methods=['GET'])
def leaveRoom():
    session['room'] = ''
    return redirect(url_for('main.index'))
