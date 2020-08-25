var http = require('http'),
    fs = require('fs'),
    path = require('path');
const PORT = 3000;
var express = require('express');
var app = express();
p=__dirname
console.log(p)
var server = http.createServer(app);


app.use(express.static(__dirname + '/'));
app.get('/cloud.html', function(req, res) {
    fs.readFile(__dirname + '/cloud.html', 'utf8', function(err, text){
        res.send(text);
    });
});
app.get('/wrongpath.html', function(req, res) {
    fs.readFile(__dirname + '/wrong.html', 'utf8', function(err, text){
        res.send(text);
    });
});
app.get('/local.html', function(req, res) {
    fs.readFile(__dirname + '/local.html', 'utf8', function(err, text){
        res.send(text);
    });
});
app.listen(PORT);