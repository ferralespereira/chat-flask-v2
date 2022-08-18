#!/bin/env python
from app import create_app, socketio
from flask import session

app = create_app(debug=True)

# context processor
@app.context_processor
def userName():
    if session.get('name'):
        return{
                'user_name': session['name'],
                'room': session['room']
            }
    else:
        return{
                'user_name': '',
                'room': ''
            }

if __name__ == '__main__':
    socketio.run(app)
