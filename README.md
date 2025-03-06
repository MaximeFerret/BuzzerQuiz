# BuzzerQuiz
## Description
BuzzerQuiz est une application de type quiz interactive avec buzzer , basée sur le framework Flask et déployée sur Kubernetes. Elle permet aux utilisateurs de participer à des quiz en temps réel, de voir leurs scores et de gérer .

## Fonctionnalités principales
- Gestion des questions de quiz et des réponses.
- Interface simple et responsive.
- Création d'un compte 
- Suppression d'un quiz
- Creation d'un quiz 
- Edition d'un quiz 
- Gestion des sessions des utilisateurs 
## Installation et configuration
### 1. Cloner le dépôt
- Clonez le dépôt Git contenant le code de l'application sur votre machine locale :  git clone https://github.com/MaximeFerret/BuzzerQuiz.git
### 2.Installer les requirements.txt
- pip install -r requirements.txt
### 3.Créer un fichier .env a la racine du projet et ajouter le code suivant 
- SECRET_KEY=VotreCléSecrèteIci
  SQLALCHEMY_DATABASE_URI=sqlite:///buzzerquiz.db
  ADMIN_SECRET_CODE=VotreCodeSecretAdmin

### 3.Lancer l'application localement 
- il suffit de lancer le fichier main.py

## Déploiement sur Kubernetes
 ### 1. Appliquer la configuration Kubernetes
- kubectl apply -f kubernetes/configmap.yaml
- kubectl apply -f kubernetes/deployment.yaml
- kubectl apply -f kubernetes/service.yaml
 ### 2. Accéder à l'application
- kubectl port-forward svc/buzzer-application 9000:80 #Car on arrive pas a récupérer le IP externe de loadBalancer


