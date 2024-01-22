# Spécifications techniques
## Introduction
Ce document détaille les spécifications techniques du projet, y compris les choix d'architecture, les choix technologiques, les choix de sécurité, les choix de déploiement et les choix de développement.


## Choix d'architecture

- Architecture en micro-services
- Un back-end pour la gestion des utilisateurs et des données, l'api et la generation des pages html 
- trois micro-services en python
- Un broker de message pour la communication entre les micro-services
- Une base de données pour les données des utilisateurs et des données de l'application (ex: les analyses) 

### Architecture en micro-services
L'architecture en micro-services est une architecture logicielle qui consiste à découper une application en un ensemble de services indépendants, qui communiquent entre eux au moyen de messages. Chaque service est déployé indépendamment des autres et communique avec les autres services au moyen de messages. Cette architecture permet de découpler les services et de les déployer indépendamment les uns des autres. Elle permet également de développer les services dans des langages différents.
Des services peuvent être ajoutés ou supprimés sans impacter les autres services. Cette architecture permet également de développer les services dans des langages différents.

### Un back-end pour la gestion des utilisateurs et des données, l'api et la generation des pages html
Le back-end est un service qui gère les utilisateurs, les données et l'api. Il est développé en python avec le framework Django. Il est composé de plusieurs parties:
- Un service pour la gestion des utilisateurs
- Un service pour la gestion des analyses
- Une api public pour une utilisation par des applications tierces
- Une api privée pour une utilisation par les micro-services
- Un service pour la génération des pages html

### Trois micro-services en python
Le premier micro-service `ms-metadata` est en charge de l'analyse des méta-données des emails.
Il effectue les tests suivants:
- Vérification de la réputation de l'adresse IP de l'expéditeur
- Vérification de la réputation du nom de domaine de l'expéditeur
- Vérification l'authenticité de l'expéditeur (SPF, DKIM, DMARC)

Le second micro-service `ms-content` est en charge de l'analyse du contenu des emails.
Il effectue les tests suivants:
- Vérification de la présence de liens malveillants
- Vérification de la présence de nombreuses fautes d'orthographe
- Recherche de mots clés dans le contenu de l'email
- Présence de typo-squatting dans les domaines des liens et des adresses email
- Présence de caractères suspects 

Le troisième micro-service `ms-attachments` est en charge de l'analyse des pièces jointes des emails.
Il effectue les tests suivants:
- Vérification du type de fichier
- Vérification du hash du fichier



## Choix technologiques
### Langages et Frameworks
- Django pour le back-end
- Python pour les micro-services
- HTML, CSS, Javascript pour le front-end
- SQL pour la base de données
- Markdown pour la documentation
- Minio pour le stockage des fichiers
- RabbitMQ pour le broker de message

Nous avons choisi django pour le back-end car c'est un framework qui est très bien documenté et qui est très utilisé. Ce framework facilite la mise en place rapide d'un back-end complet avec une base de données et une API. La génération de pages HTML est également simplifiée, tout comme la gestion de l'authentification des utilisateurs. Django offre également la possibilité de créer une API efficacement grâce à Django Rest Framework.

En ce qui concerne les micro-services, notre choix s'est porté sur Python en raison de notre familiarité avec le langage et de sa popularité. Il permet de développer rapidement des micro-services. De plus le back-end est développé en python avec Django, ce qui permet de développer les micro-services plus rapidement bien que les micro-services puissent être développés dans un autre langage.

Nous avons choisi HTML, CSS et Javascript pour le front-end car nous n'avons actuellement pas besoin de fonctionnalités avancées.
En ce qui concerne le stockage des fichiers, Minio a été choisi en tant que service de stockage d'objets en raison de sa capacité à stocker des fichiers de manière distribuée tout en offrant un accès via une API. Cette solution s'intègre parfaitement à notre déploiement sur Kubernetes, faisant de Minio un choix idéal pour le stockage de fichiers dans cet environnement.
Nous avons choisi RabbitMQ pour le broker de message car c'est un broker de message très utilisé et qui est très bien documenté. Il permet de communiquer entre les micro-services de manière asynchrone.


### Infrastructure
- Docker pour la conteneurisation
- Kubernetes pour l'orchestration des conteneurs



## Choix de sécurité
Les choix de sécurité sont détaillés dans le [plan de sécurisation](plan_securisation.md).

## Choix de déploiement

## Choix de développement
### Diagrammes
