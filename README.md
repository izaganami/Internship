# Internship

###updates:

--- On peut interrompre le processus à n'importe quelle époque et les poids seront enregistrés sous le fichier best_model.pickle  


--- Avec la bonne installation de CUDA et cudnn l'entrainement se lance en GPU


--- Le fichier Reload_Train permet de reprendre l'entrainement d;un model sans devoir commencer à 0, le code correspondant esr dans le fichier scritp-to-train et le parametre associé est 'ReloadModel'

---vo02:
1. Le script tout en un est redirigé vers le fichier finetuning 
2. Le fichier predict.py permet maintenant de visualiser le pourcentage des deux premieres configurations
3. Cette visualisation est sous forme de boutton qui permet de corriger les erreurs de l'algo a chaque click pour semi-automatisation de la tache
         
![capture du resultat](https://github.com/izaganami/Internship/blob/master/1905.PNG "Capture")
         
 Prochaine etape:
      Sauvegarde des résultats sous format json au fur de la visualisation et la validation.

---v03:
1. L'entrée text est possible avec un champ dédié et un button 
2. Pour chaque changement de configuration une fonction est lancée permettant de mettre à jour le fichier json
3. Le fichier json est généré à la fin du code sous la forme:

```json
"183": {"start": "00:00:16.76", "end": "00:00:16.85", "label": "AS02"}
```

---v04:
1. l'input est testé s'il appartient au groupe des labels ou pas.
2. Pour chaque lancement de test sur un nouvelle video on genere des figures pour toutes 100frames pour visualiser les probabilités de chaque configuration.

 Prochaine etape:
      Une deuxieme validation avant l'écriture sur le fichier json qui se base sur un seuil de probabilités à faire entrer manuellement ou avec une valeur par défaut.
