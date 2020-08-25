var http = require('http')
    , httpProxy = require('http-proxy');

httpProxy.createServer({
  hostnameOnly: true,
  router: {
    'localhost:8989': '127.0.0.1:8989',
    'localhost:3000' : '127.0.0.1:3000'
  }
}).listen(8930);
