$(function(){
	var ws_scheme = window.location.portal == "https:" ? "wss" : "ws";
	var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
	console.log("connecting to "+ ws_path);
	var socket = new ReconnectingWebSocket(ws_path);

	socket.onopen = function(){
		console.log("connected to chat socket");
		};
	socket.onclose = function(){
		console.log("disconnected from chat socket");
	};


socket.onmessage = function (message) {
	//decoding JSON
	console.log("got websocket message "+ message.data);
	var data = JSON.parse(message.data);
	//handle errors
	if (data.error){
		alert(data.error);
		return;
	}
	//handle joinging
	if (data.join) {
		console.log("joining room "+ data.join);
		var roomdiv = $(
			"<div class='room' id='room-" + data.join +  "'>" +
			"<h2>" + data.title +"</h2>" +
			"<div class ='messages'></div>" +
			"<input><button>Send</button>" +
			"</div>"

			);
		$("#chats").append(roomdiv);
		roomdiv.find("button").on("click", function(){
			socket.send(JSON.stringify({
				"command": "send",
				"room": data.join,
				"message": roomdiv.find("input").val()
			}));
			roomdiv.find("input").val("");
		});
		//handle leaving

	}
	else if(data.leave){
		console.log("leaving room " + data.leave);
		$("#room-" + data.leave).remove();
	} else if (data.message || data.msg_type != 0){
		var msgdiv = $("#room-" + data.room + ".messages");
		var ok_msg = "";
		//msg types are defined in chat/settings.py
		//only for demo purposes is hardcoded, in production scenarios, consider call a service
		switch (data.msg_type){
			case 0:
			//msg
			ok_msg ="<div class='message'>" +
					"<span class='username'>" + data.username + "</span>" +
					"<span class='body'>" + data.message + "</span>"
					"</div>";
			break;
			case 1:
			//warning/advice messages
					ok_msg = "<div class='contextual-message text-warning'>" + data.message + "</div>";
                    break;
                case 2:
                    // Alert/Danger messages
                    ok_msg = "<div class='contextual-message text-danger'>" + data.message + "</div>";
                    break;
                case 3:
                    // "Muted" messages
                    ok_msg = "<div class='contextual-message text-muted'>" + data.message + "</div>";
                    break;
                case 4:
                    // User joined room
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username + " joined the room!" + "</div>";
                    break;
                case 5:
                    // User left room
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username + " left the room!" + "</div>";
                    break;
                default:
                    console.log("Unsupported message type!");
                    return;
            }
            msgdiv.append(ok_msg);
            msgdiv.scrollTop(msgdiv.prop("scrollHeight"));
		}
	 
	else {
		console.log("cannot handle message!");
	}
	};




//says if we joined a room or not by if there's a div for it
function inRoom(roomId) {
	return $("#room-" + roomId).length > 0;

};

//room join or leave

$("li.room-link").click(function(){
	roomId = $(this).attr("data-room-id");
	if(inRoom(roomId)){
		//leave room
		$(this).removeClass("joined");
		socket.send(JSON.stringify({
			"command": "leave",//determines which handler will be used(see chat/routing.py)
			"room": roomId
		}));
	}else {
		//join room
		$(this).addClass("joined");
		socket.send(JSON.stringify({
			"command": "join",
			"room": roomId
		}));
	}
});
});