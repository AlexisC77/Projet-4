bonjour! Ce document a pour objectif de vous expliquer comment utiliser ce programme de génération de tournois d'échecs!

Tout d'abord, assurer vous que python est installé sur votre appareil dans une version assez récente (supérieure à 3.4) ensuite, allez dans votre terminal et placez vous dans le dossier contenant le script et le fichier requirements.txt, et créer votre environnement virtuel (tapez "python -m venv env" si vous utilisez venv) ensuite, activez cette environnement (tapez "source env/bin/activate" si vous utilisez venv) puis installez les paquets python contenus dans le fichier requirements.txt (tapez "pip install -r requirements.txt")

vous pouvez maintenant éxécuter le programme en tapant "python chess_tournament.py" ou en allez l'éxécuter manuellement directement dans python ou dans votre IDE, ce programme créera des dossiers pour chacunes des catégories du site contenant les images des livres et un fichier .csv contenant les information.


Afin de créer un rapport flake8 avec pour paramètre max-line-length=119, installez d'abord flake8 en tapant "pip install flake8-html" puis placez vous dans le dossier contenant le projet et rentrez: "flake8 --format=html --max-line-length=119 --htmldir=flake-report" dans votre terminal
