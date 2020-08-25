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
var urlExists = require('url-exists');
var engines = require('consolidate');



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
        var webpath=path.resolve(process.cwd() + '/../Web_Service');
        console.log(serverPath)
        let re = new RegExp("^.*\\/(?=[^/]*$)");
        var sub_str=url.match(re);
        var name = url.replace(sub_str,'');
        name= name.replace(".mp4",'')
        exec("python "+serverPath+"/predict.py "+"--model "+serverPath+"/output/activity.model --label-bin "+serverPath+"/output/lb.pickle --input "+url+" --output "+webpath+"/outputs/"+name+".mp4" +" --size 128 --proba 10.00 --path "+webpath+"/outputs/"+name+".json", (error, stdout, stderr) =>
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

function checkExistsWithTimeout(filePath, timeout) {
    return new Promise(function (resolve, reject) {

        var timer = setTimeout(function () {
            watcher.close();
            reject(new Error('File did not exists and was not created during the timeout.'));
        }, timeout);

        fs.access(filePath, fs.constants.R_OK, function (err) {
            if (!err) {
                clearTimeout(timer);
                watcher.close();
                resolve();
            }
        });

        var dir = path.dirname(filePath);
        var basename = path.basename(filePath);
        var watcher = fs.watch(dir, function (eventType, filename) {
            if (eventType === 'rename' && filename === basename) {
                clearTimeout(timer);
                watcher.close();
                resolve();
            }
        });
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


app.get('/page', function(req, res){
    var current_url = new URL(req.protocol + '://' + "localhost:8989/" + req.originalUrl+".mp4");
    const search_params = current_url.searchParams;
    const path_video = search_params.get('url');

    //get name of video
    let re = new RegExp("^.*\\/(?=[^/]*$)");
    var sub_string=path_video.match(re);
    var name_string = path_video.replace(sub_string,'');
    name_string= name_string.replace(".mp4",'');
    module.exports = { name_string: name_string };

    var test=true;
    try
        {
            urlExists(path_video, function(err, exists) {
            console.log(exists);
            test=exists;
            });
            if (fs.existsSync(path_video))
            {
                var not_private = path_video.includes("/");
                if(not_private)
                {
                    f(path_video);
                    res.redirect('http://localhost:8989/local.html?name='+name_string);
                    //return res.send('Received a GET HTTP method with public path='+path_video);
                }
                else
                    {
                        var path_priv_video="file:///workspace/private/videos/"+path_video;
                        f(path_priv_video);
                        res.redirect('http://localhost:8989/local.html?name='+name_string);
                        //return res.send('Received a GET HTTP method with private path='+path_priv_video);
                    }

            }
            else if(test===true)
            {
                f(path_video);
                /*checkExistsWithTimeout('outputs/small.json',46969).then((result) => {
                    res.redirect("http://localhost:8989/downloadFile/small.json");
                    console.log("Success", result);
                    }).catch((error) => {
                    console.log("Error", error);
                });*/
                try {
                    res.redirect('http://localhost:8989/cloud.html?name='+name_string);
                }
                catch (e) {

                    res.redirect('https://9196b81e795e.ngrok.io/cloud.html?name='+name_string);
                }

                //return res.send('Received a GET HTTP method with cloud/public path='+path_video);
            }
            else
                {
                    res.redirect('http://localhost:8989/wrongpath.html');
                   //return res.send('Received a GET HTTP method with a wrong path');
                }

        }
    catch(err)
        {
            console.log(err);
            return res.send('Received a GET HTTP method with an error: '+err);
        }



});


app.use(express.static(__dirname + '/'));
app.get('/downloadFile/*', (req, res) => {
    var name=req.originalUrl.split('/')[2];
    console.log(name)

    checkExistsWithTimeout('outputs/'+name,46969).then((result) => {
        res.download('outputs/'+name, (err) => {
            if (err)
            {
                console.log(err);
            }});
                console.log("Success", result);
            }).catch((error) => {
                console.log("Error", error);
            });

        });



/*app.get('/cloud.html', function(req,res) {
    app.use(express.static('assets'));
    data= fs.readFile('./cloud.html',   function (err, data) {
    res.setHeader('Content-Type', 'text/html');
    res.send(data);
})});*/

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

//deleting index.js

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


