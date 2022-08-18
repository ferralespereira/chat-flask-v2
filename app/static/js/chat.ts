let socket:any = io.connect('http://' + document.domain + ':' + location.port);

// socket.on('connect', function(){
    socket.emit('joined');
// });


let user_name:any = document.getElementById('user-name');
socket.on('give me your name', function() {
    socket.emit('take my name', { user_name: user_name.innerHTML });
});

socket.on('connect with you', function(data:any){
    let div_info:any = document.getElementById('info');
    if (data.user_room == user_name.innerHTML){
        div_info.innerHTML = data.msg;
    }
});

socket.on('get user list', function(data:any){
    let users:any = document.getElementById('users');
    
    // if are users connected, show all user names in botons except mine
    if ((data.list_users).length > 0 && (data.list_users[0]).length > 0 ){
        users.innerHTML = 'Select users to connect: <br>';
    
        for (let user of data.list_users) {
            if (user){
                if (user != user_name.innerHTML){
                    users.innerHTML += '<button type="submit" name="room" value="'+user+'" class="btn btn-info rounded-5 m-1">'+user+'</button>';
                }
            }
        }
    }else{
        users.innerHTML = '<button type="submit" name="room" value="" class="btn btn-primary rounded-5 m-1">Go</button>';
    }   
});
    

socket.on('status', function(data:any) {
    let textare_chat:any = document.getElementById('chat');
    textare_chat.value += '... ' + data.msg + ' ...\n';
    textare_chat.scrollTop = textare_chat.scrollHeight;
});

socket.on('message', function(data:any) {
    let textare_chat:any = document.getElementById('chat');
    textare_chat.value += '  '+data.name+':\n';
    textare_chat.value += '         '+data.msg+'\n';
    // textare_chat.value += '      ' + data.msg + '\n';
    textare_chat.scrollTop = textare_chat.scrollHeight;
});

function sendText(e:any){
    let code = e.keyCode || e.which;
    if (code == 13) {
        let text:any = document.getElementById('text');
        socket.emit('text', { msg: text.value });
        text.value ='';
    }
}

