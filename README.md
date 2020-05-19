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
      Sauvegarde des r2sultat sous format json au fur de la visualisation et la validation.
