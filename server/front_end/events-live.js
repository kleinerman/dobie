var service_port_ws = 5004;

var formidable = require('formidable');
var http = require('http');

//set up the websocket server
var app = http.createServer().listen(service_port_ws);
var io = require('socket.io').listen(app);


var server = http.createServer(function(req, res) {
        //set api endpoint name and method
        if (req.url == '/readevent' && req.method.toLowerCase() == 'post') {
                //parse form
                var form = new formidable.IncomingForm();
                form.parse(req, function(err, fields, files) {
                        fields_str = JSON.stringify(fields);
                        //show sent values on server console
                        //console.log(fields_str);
                        io.sockets.emit("message_to_client", fields_str);
                });
        }
res.end();
return;
})

server.listen(5002);
