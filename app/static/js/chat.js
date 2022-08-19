var socket = io.connect('http://' + document.domain + ':' + location.port);
// socket.on('connect', function(){
socket.emit('joined');
// });
var users = document.getElementById('users');
var user_name = document.getElementById('user-name');
socket.on('give me your name', function () {
    socket.emit('take my name', { user_name: user_name.innerHTML });
});
socket.on('connect with you', function (data) {
    var div_info = document.getElementById('info');
    if (data.user_room == user_name.innerHTML) {
        div_info.innerHTML = data.msg;
    }
});
socket.on('get user list', function (data) {
    // if are users connected, show all user names in botons except mine
    if ((data.list_users).length > 0 && (data.list_users[0]).length > 0) {
        users.innerHTML = 'Select users to connect: <br>';
        for (var _i = 0, _a = data.list_users; _i < _a.length; _i++) {
            var user = _a[_i];
            if (user) {
                if (user != user_name.innerHTML) {
                    users.innerHTML += '<button type="submit" name="room" value="' + user + '" class="btn btn-info rounded-5 m-1">' + user + '</button>';
                }
            }
        }
    }
    else {
        users.innerHTML = '<button type="submit" name="room" value="" class="btn btn-primary rounded-5 m-1">Go</button>';
    }
});
socket.on('status', function (data) {
    var textare_chat = document.getElementById('chat');
    textare_chat.value += '... ' + data.msg + ' ...\n';
    textare_chat.scrollTop = textare_chat.scrollHeight;
});
socket.on('message', function (data) {
    var textare_chat = document.getElementById('chat');
    textare_chat.value += '  ' + data.name + ':\n';
    textare_chat.value += '         ' + data.msg + '\n';
    // textare_chat.value += '      ' + data.msg + '\n';
    textare_chat.scrollTop = textare_chat.scrollHeight;
});
function sendText(e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
        var text = document.getElementById('text');
        socket.emit('text', { msg: text.value });
        text.value = '';
    }
}
// if the socketio can not connect, wait 3sec and try to connect again
setTimeout(function () {
    if (users.children.length == 0) {
        socket.emit('joined');
        console.log('Reconected');
    }
}, 3000);
