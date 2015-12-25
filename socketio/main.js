var app = require("express")();
var http = require("http").createServer(app);
var io = require("socket.io")(http);

io.on("connection", function(socket){

    socket.username = "Anon";
    console.log("An user connected");

    socket.on("add user", function(username){
        console.log("Username: " + username)
        socket.username = username;
    });

    socket.on("join", function(draw_id){

        console.log(socket.username + " - draw: " + draw_id);
        socket.join(draw_id);

        /**
         * Sends a message to all sockets in a draw
         */
        function draw_broadcast(subject, message) {
            console.log("Broadcasting: ", subject, "(", message, ")");
            socket.broadcast.to(draw_id).emit(subject, message);
        }

        socket.on("disconnect", function() {
            console.log(socket.username + " - disconected ");
            socket.leave(draw_id);
        });

        socket.on("message",  function(message) {
            console.log(socket.username + " - message: " + message);
            draw_broadcast("message", {
                username: socket.username,
                message: message
            });
        });

        socket.on("draw update",  function() {
            console.log(socket.username + " - draw update");
            draw_broadcast("draw update");
        });

        draw_broadcast("user join", socket.username);
    });

});

http.listen(8888, function(){
    console.log("listening on *:8888");
});
