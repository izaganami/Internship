## Analyse semi-automatique de vidéos de séances d’activités d’apprentissage
Ce dépôt rassemble le code développé durant notre projet recherche.

### Préparation des données
Le dossier `data_preparation` rassemble des scripts python utiles à la mise en forme de la donnée pour l'apprentissage des divers réseaux de neurones ainsi que de petits utilitaires pour analyser les données d'entraînement. Plus de détails dans le dossier en question.

### modèle CNN et fine-tuning
Le dossier `CNN_model_fine_tuning` rassemble les scripts d'entraînement d'un réseau de neurones convolutifs avec pour base le réseau ResNet50.
Plus d'informations dans le dossier correspondant.
### modèle LSTM
Le dossier `LSTM_model` rassemble les scripts d'entraînement d'un réseau de neurones récursif qui prend en entrée les features du CNN entraîné.
Plus d'informations dans le dossier correspondant.

### Lancer un entrainement
Utilisez le script `train_all-in-one.py`
