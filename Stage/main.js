var express = require('express'),
  app = express(),
  port =  8989,
  mongoose = require('mongoose'),
  Video = require('./models/model'), //created model loading here
  bodyParser = require('body-parser');

const { exec } = require("child_process");
const path = require('path');
const router = require('express').Router();
const url = require('url');
var process = require('process');
const fs = require('fs');




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

function f(url){


        var serverPath = path.resolve(process.cwd() + '/../AI/fine-tunning-deeplearning-master');
        console.log(serverPath)

        exec("python "+serverPath+"/predict.py "+"--model "+serverPath+"/output/activity.model --label-bin "+serverPath+"/output/lb.pickle --input "+url+" --output "+serverPath+"/output/results.mp4 --size 128 --proba 10.00", (error, stdout, stderr) =>
        {
            if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
});
}




app.use(function(req, res,next) {
  //res.header("Access-Control-Allow-Origin","*");
  res.header("Access-Control-Allow-Headers","Origin,X-Requested-With,Content-Type,Accept,Authorization");
  if(req.method==="OPTIONS"){
    res.header("Access-Control-Allow-Methods","PUT,POST,PATCH,DELETE,GET");
    return res.status(200).json({})
  }
  next();
  //res.status(404).send({url: req.originalUrl + ' not found'})
});


app.get('*', function(req, res){
    var current_url = new URL(req.protocol + '://' + "localhost:8989/" + req.originalUrl+".mp4");
    const search_params = current_url.searchParams;
    const path_video = search_params.get('url');
    try
        {
            //if (fs.existsSync(path_video))
            //{
                var not_private = path_video.includes("/");
                if(not_private)
                {
                    f(path_video);
                    return res.send('Received a GET HTTP method with public path='+path_video);
                }
                else
                    {
                        var path_priv_video="file:///workspace/private/videos/"+path_video;
                        return res.send('Received a GET HTTP method with private path='+path_priv_video);
                    }

            //}
           // else
                //{
                   // return res.send('Received a GET HTTP method with a wrong path');
              //  }

        }
    catch(err)
        {
            console.log(err);
            return res.send('Received a GET HTTP method with an error: '+err);
        }


});

app.post('*', (req, res) => {
  return res.send('Received a POST HTTP method');
});

app.put('/', (req, res) => {
  return res.send('Received a PUT HTTP method');
});

app.delete('/', (req, res) => {
  return res.send('Received a DELETE HTTP method');
});

app.listen(process.env.PORT, () =>
  console.log(`listening on port ${port}!`),
);

/*
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://database:M!YnbRNbuUU3a4J@cluster0-mboti.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });
client.connect(err => {
  const collection = client.db("test").collection("devices");
  // perform actions on the collection object
  client.close();
});
&& cd AI\fine-tunning-deeolearning-master && python predict.py
 */


