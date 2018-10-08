var service_port_ws = 5004;

//https://www.npmjs.com/package/formidable
var formidable = require('formidable'),
    http = require('http'),
    util = require('util');

//set up the websocket server
var app = http.createServer().listen(service_port_ws);
var io = require('socket.io').listen(app);

http.createServer(function(req, res) {
        //set api endpoint name and method
        if (req.url == '/readevent' && req.method.toLowerCase() == 'post') {
                //parse form
                var form = new formidable.IncomingForm();
                form.parse(req, function(err, fields, files) {
                        //show sent values on server console
                        fields_str=JSON.stringify(fields);
                        console.log(fields_str);
                        send_msg(fields_str);
                         res.end();
                        //show sent values into browser
                        //res.writeHead(200, {'content-type': 'text/plain'});
                        //res.write('received post:\n\n');
                        //res.end(util.inspect({fields: fields}));
                });
                return;
        }


//function to send message
function send_msg(datareceived){
//      console.log("data sent:" + datareceived.toString());
        //console.log(util.inspect(datareceived, false, null));
        //prepare message
        //var msg = datareceived.toString();
        var msg = datareceived;
        //only send message if its correct (see examples above)
        //if(msg.indexOf("window")==0){
                //io.sockets.emit("message_to_client",{targetWindow: msg});
                io.sockets.emit("message_to_client",msg);
        //}
}

}).listen(5002);

