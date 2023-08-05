# Brainome(tm)

## Project description

Brainome is a **data compiler** that automatically solves supervised machine learning problems with repeatable and reproducible results and creates **standalone python predictors**.

Brainome’s philosophy is that data science should be accessible to all:

* Run on your machine or in your cloud.
* Keep your data local.
* Own your model python code - run it anywhere.
* Single “compiler like” command to convert you data in a model in a single step.
* Automatic data format conversion (text, numbers, etc..).
* No hyper-parameter tuning through measurements.
* Unlimited dimensionality (premium).

Brainome offer unique data insight and helps answer:

* Do I have enough data and the right feature?
* What features are important (attribute ranking)?
* What model type will work best?
* Is my model overfitting?

Brainome’s predictors:

* Run as executable or import as library.
* Are hardware independent.
* Are self contained in a single python file and integrate easily in standard CI/CD flow, Github, etc…

Brainome is free for personal use or evaluation.

Examples:
Measure and build a random forest predictor for titanic
        brainome https://download.brainome.ai/data/public/titanic_train.csv

Build a better predictor by ignoring columns:
        brainome titanic_train.csv -ignorecolumns "PassengerId,Name" -target Survived

Automatically select the important columns by using ranking:
        brainome titanic_train.csv -rank -target Survived

Build a neural network model with effort of 5:
        brainome titanic_train.csv -f NN -e 5 -target Survived

Measure headerless dataset:
        brainome https://download.brainome.ai/data/public/bank.csv -headerless -measureonly

Full documentation can be found at https://www.brainome.ai/documentation
