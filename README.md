# Projet d'École : Création d'un Langage de Programmation

## Description
Ce projet consiste à créer un langage de programmation en utilisant Yacc en Python. L'objectif est de concevoir un compilateur simple qui peut analyser et exécuter des programmes écrits dans ce nouveau langage.

## Prérequis
- Python 3.x

## Installation
Pour installer les dépendances nécessaires, exécutez la commande suivante :
__windows__ :
```bash
py -m pip install -r requirements.txt
```
__linux__ :
```bash
python3 -m pip install -r requirements.txt
```

## Utilisation
Pour exécuter le compilateur, utilisez la commande suivante :
__windows__ :
```bash
python main.py
```
__linux__ :
```bash
python3 main.py
```

## Tests
Pour exécuter les tests, utilisez la commande suivante :
__windows__ :
```bash
py -m pytest
```
__linux__ :
```bash
python3 -m pytest
```

## Structure du projet
```txt
.
├── main.py
├── lexer.py
├── parser.py
├── evals.py
├── utils.py
├── tests
│   ├── test_.py
│   └── ...
├── examples
│   ├── example1.txt
│   └── ...
├── README.md
└── requirements.txt
```

## Auteurs
- BOURDIN Kerian
- TECHER Mathis