# project_data_storytelling_ynov

Repository hébergeant notre travail effectué lors d'un projet de notre majeure Data Science.

Il se compose de fichiers .ipynb de data cleaning, de fichiers .py pour le code dash et de fichiers .csv et .xls qui étaient nos sources de données.


L'objectif du projet était de produire une solution de Data Storytelling et de la déployer en ligne.

Nous avons choisi comme sujet l'inflation des prix de l'alimentaire, et avons tenter de faire resortir les éléments importants à constater.

La structure du projet est consituté d'un package pages (qui contient un module styles pour le code css, un module gen pour les fonctions génératrices de contenu, et d'un module pour chaque page), d'un fichier requirements.txt qui englobe nos dépendances, d'un fichier master_datastorytelling.yml qui contient le code yaml nécessaire à notre déploiement continu, et d'un fichier app.py qui contient le code de notre application dash, qui exploite le package pages pour fonctionner.
