# Multihoming
Lien vers l'application : https://multihoming.herokuapp.com/

# Description du projet
## Présentation rapide du modèle

L'objectif de l'application est de modéliser les résultats de l'article *The importance of consumer multihoming (joint purchases) for market performance: Mergers and entry in media markets*. L'article porte donc sur l'étude du multihoming des consommateurs. Le multihoming des consommateurs modélise une situation dans laquelle un consommateur achète un même bien équivalent chez deux entreprises différentes, par exemple en souscrivant à la fois à un abonnement Netflix et à un abonnement Disney +. Le modèle se base sur le modèle de Salop, lui-même étant une extension du modèle d'Hotelling, représentant une plage sur laquelle sont présents deux vendeurs de glaces, et dont les consommateurs sont répartis tout le long de cette plage. Hotelling se pose donc la question de savoir où est ce que les deux vendeurs vont se positionner, sachant que les consommateurs subissent un coût de transport pour se rendre chez un marchand et donc ils privilégierons le marchand le plus proche. Salop va chercher à combler la principale faiblesse de ce modèle, à savoir les effets de bord dûs au fait que le modèle soit basé sur un segment. Salop va donc mettre en place un nouveau modèle basé, non plus sur un segment, mais sur un cercle, dont les consommateurs sont répartis tout autour de celui-ci. Voici donc le modèle de ville circulaire, qui nous servira de base pour ce modèle de homing. 

La différenciation des préférences des consommateurs se modélise par le paramètre $\theta$, plus celui-ci est faible et plus les consommateurs auront une préférence forte pour un bien, et donc seront des singlehomers. A l'inverse, un $\theta$ élevé rendra les consommateurs moins dépendant à l'un des deux biens, ils seront donc des multihomers. 


## Présentation de l'application.

L'application permet à un utilisateur d'obtenir la répartition des consommateurs dans chaque groupe (singlehomer et multihomer) en fonction d'un $\theta$ et d'un prix spécifiés par l'utilisateur. Le panel étudié est restreint à une configuration de marché dans laquelle il n'y a que 3 entreprises, le nombre de consommateurs affichés dans chaque groupe ne représente que la demande pour l'entreprise 1. C'est-à-dire que si l'application vous affiche qu'il y a 5 multihomers et 4 singlehomers, il ne s'agit que de consommateurs étant singlehomers de l'entreprise 1 (ils ne consomme que chez elle) ou alors multihomers de l'entreprise 1 (ils consomment au moins le bien de l'entreprise 1). Sur le cercle, est représenté le modèle, les trois entreprises distribuées symétriquement autour de celui-ci, ainsi que les consommateurs indifférents entre singlehomer et multihomer. Ces consommateurs représentent une limite au delà de laquelle les consommateurs basculeront d'une classe à l'autre (multihomer devient singlehomer ou inversement). Les positions de ces consommateurs indifférents sont amenées à être modifiées par les paramètres de prix ou de $\theta$.


## Etat d'avancement du projet

Actuellement, l'application représente correctement l'emplacement des firmes et des consommateurs indifférents entre singlehomer et multihomer. Elle affiche également le nombre de consommateurs singlehomers et multihomers de l'entreprise 1. 
Il est actuellement à l'étude l'implémentation de contraintes afin que les positions des consommateurs indifférents respectent les problématiques du modèle. Une première version est actuellement appliquée sur l'application mais elle est bugguée. Il s'agit du principal objectif à atteindre pour permettre une potentielle autre amélioration, puisque comme vous le verrez, le nombre de singlehomers et de multihomers en souffre. 

Une fois cette problématique résolue, il pourrait être intéressant de permettre à l'utilisateur de modifier les prix des autres entreprises, permettre d'ajouter une entreprise sur le marché ou effectuer une fusion. 

