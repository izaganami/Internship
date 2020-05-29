var express = require('express'),
  app = express(),
  port =  8989,
  mongoose = require('mongoose'),
  Video = require('./models/model'), //created model loading here
  bodyParser = require('body-parser');
  
// mongoose instance connection url connection
mongoose.Promise = global.Promise;
mongoose.connect( encodeURI('mongodb+srv://admin:admin@cluster0-6maah.mongodb.net/restapi'),
    {useNewUrlParser: true, useUnifiedTopology: true}, () =>
console.log("connected"));


var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));

db.once('open', function (ref) {
    console.log('Connected to mongo server.');
    //trying to get collection names
    console.log(db.collections);
});


app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


var routes = require('./routes/route'); //importing route
routes(app); //register the route


app.listen(port);


console.log('started on: ' + port);

Video.find(function(err, docs) {
    console.log(JSON.stringify(docs));
});

app.use(function(req, res,next) {
  res.header("Access-Control-Allow-Origin","*");
  res.header("Access-Control-Allow-Headers","Origin,X-Requested-With,Content-Type,Accept,Authorization");
  if(req.method==="OPTIONS"){
    res.header("Access-Control-Allow-Methods","PUT,POST,PATCH,DELETE,GET");
    return res.status(200).json({})
  }
  next();
  res.status(404).send({url: req.originalUrl + ' not found'})
});
/*
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://database:M!YnbRNbuUU3a4J@cluster0-mboti.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });
client.connect(err => {
  const collection = client.db("test").collection("devices");
  // perform actions on the collection object
  client.close();
});
 */


