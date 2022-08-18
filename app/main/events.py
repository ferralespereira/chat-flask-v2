from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from app import list_users


@socketio.on('joined')
def joined():

    print('***----------------joined----------------***')
    print('user name:')
    print(session.get('name'))

    # if user is is loged
    name = session.get('name')
    if (name):
        
        room_send   = name+'_'+session.get('room')
        room_receive = session.get('room')+'_'+name
        join_room(room_send)

        print(room_send)
        
        emit('connect with you',{
                        'msg': name + ' wants to conect with you',
                        'user_room': session.get('room')
                        },broadcast=True)

        if session.get('room'):
            emit('status', {
                    'msg':'YOU' + ' has entered'
                    }, room=room_send)
        
            emit('status', {
                    'msg':name + ' has entered'
                    }, room=room_receive)

    # remove list_users 
    del list_users[:]
    emit('give me your name',broadcast=True)


@socketio.on('take my name')
def takeMyName(data):
    print('**********************users***********')

    # if user is loged add it to the list_users
    if data['user_name']:
        list_users.append(data['user_name'])
    print(list_users)

    emit('get user list', {
                    'msg': 'List of users',
                    'list_users': list_users
                    },broadcast=True)


@socketio.on('text')
def text(message):

    print('***----------------text----------------***')
    print('name: '+session.get('name'))
    print('room: '+session.get('room'))

    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    name = session.get('name')

    room_send   = name+'_'+session.get('room')
    room_receive = session.get('room')+'_'+name

    emit('message', {
                'name': 'YOU', 
                'msg':  message['msg']
                }, room=room_send)
    
    emit('message', {
            'name': name, 
            'msg':  message['msg']
            }, room=room_receive)