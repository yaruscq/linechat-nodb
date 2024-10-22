document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    let room = "Lounge";
    joinRoom('Lounge');

    // Setup a pre-defined event bucket called 'connect' at the server side in JS
    
    //For testing
    // socket.on('connect', () => { // client connected, and send 'connected' to the server
    //     // since 'send()' is used here, the msg will be sent to the server into a pre-defined bucket 'message'
    //     socket.send('I\'m connected!'); 
    // });


    // Display incoming message
    socket.on('message', data => {
        // console.log(`Message received: ${data}`)  // coming from the server
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');

        if (data.username){
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        } else [
            printSysMsg(data.msg)
        ]

        
    })


    //Demo
    // socket.on('some-event', data => {

    //     // console.log(`Message received: ${data}`)  
    //     console.log(data) // coming from server 'some-event' bucket
    // })



    // Send message
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg' : document.querySelector('#user_message').value, 'username': username, 'room' : room });

        // Clear input area
        document.querySelector('#user_message').value = '';

    }


    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {

        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg =`You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom; 

            }
        }
    })


    // Leave Room
    function leaveRoom(room) {
        socket.emit('leave', {'username' : username, 'room' : room });
    }


    // Join Room
    function joinRoom(room) {
        socket.emit('join', {'username' : username, 'room' : room });
        // Clear message area
        document.querySelector('#display-message-section')
        document.querySelector('#user_message').focus();
    }

    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }

})