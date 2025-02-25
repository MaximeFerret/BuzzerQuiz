# On part d'un environnement Ubuntu 22.04
FROM ubuntu:22.04
# On installe Python et pip
RUN apt-get update && apt-get install -y python3-pip
# On copie les fichiers de notre projet dans l'environnement

COPY . .
# On installe les dépendances à partir du fichier requirements.txt
RUN pip install -r requirements.txt
# On définit la commande à exécuter pour lancer notre application
ENTRYPOINT ["python", "main.py"]
