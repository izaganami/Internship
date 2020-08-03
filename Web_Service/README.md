# Internship

Pour le moment on a l'application qui est connectée à un service sur cloud (MongoDB Atlas) pour tester si le Restful
 Webservice  fonctionne comme on veut. Du coup on accede grace à l'identifiant de l'objet en methode GET et apres on peut 
 lancer le script sur la video en question.
 
 Ci-dessous il'y a l'output du code, l'outil Postman qui permet de tester des service REST, le coté cloud et local(Compass) de 
 MongoDB.
 
![Lien en methode GET](https://github.com/izaganami/Internship/blob/master/Stage/screens/link.PNG  "Lien en methode GET")

![MongoDB et Compass](https://github.com/izaganami/Internship/blob/master/Stage/screens/localandcloud.PNG  "MongoDB et Compass")

![Postman et la sortie du code](https://github.com/izaganami/Internship/blob/master/Stage/screens/restfulapp.PNG  "Postman et la sortie du code")

---
To test the application, first thing first is running the server on the virtual machine using:
```
npm start
```
After receiving the "connected" message, we can open any browser and run these examples:
1.For a public video located in the virtual machine:
```
http://localhost:8989/page?url=C:/Users/youne/Desktop/example_clips/p207lise
```


2.For a private video located in the virtual machine:(Only the name is required and the algortihm will verify if it exists or not)
```
http://localhost:8989/page?url=p207lise
```
The complete path for this last request will be : 
```
file:///workspace/private/videos/p207lise
```
And the algorithm makes sure the extension is added afterwards.
