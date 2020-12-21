var service_port_ws = 5004;

var formidable = require('formidable');
var http = require('http');

const https = require('https');
const fs = require('fs');


const options = {
  key: fs.readFileSync('/certs/server.key'),
  cert: fs.readFileSync('/certs/server.crt')
};




//set up the websocket server
var app = https.createServer(options).listen(service_port_ws);
var io = require('socket.io')(app);

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
