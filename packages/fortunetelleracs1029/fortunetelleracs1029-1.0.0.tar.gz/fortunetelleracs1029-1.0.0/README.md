[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9088627&assignment_repo_type=AssignmentRepo)

![build badge](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-16/actions/workflows/build.yaml/badge.svg)

# Python Fortune Teller Package

[Andrei Stoica](https://github.com/andreicstoica)
[Brandon Chen](https://github.com/b-chen00)
[Charlie Xiang](https://github.com/xiang-charlie)
[Sanjaya Bhatta](https://github.com/itSanjaya)

[Package Page on PyPi](https://pypi.org/project/fortunetelleracs1029/1.0.0/)

## Description
Fortuneteller gives you a fortune for various aspect of your life in order to get you along on your way. If you need general life advice or guidance, a quote will be given if you are looking to learn or detach. If you are stuck on a computer science project or assignment, this package will help you estimate when it will be completed by and even attempt to help you debug by giving a random common error. An inspirational fortune could also be given as a quote from a famous figure. For a lighter mood, a funnier/light-hearted fortune could be given as well.

## Functions and their Args
### getLiveAdvice(type, seed=None)
Returns a line of life advice, either focused on learning (learning) or detaching (detach) depending on the argument passed in with an optional seed argument.

#### Args:
* type: The type of life advice to be returned taken as either the String "learning" or "detach".
* seed: An optional seed to generate the same random result which is taken as a String or Integer.

#### Returns:
* A String representing the learning or detach advice.

### getCSFortune(question, debug, seed=None)
Receives a question in the form of a String with a boolean value on whether it is for debugging purposes. An optional seed argument could be given to generate the same random result. Outputs a fortune on whether you will succeed in doing anything computer science related or not. If debugging, a random potential error is given or nothing at all if it is beyond fixing.

#### Args:
* question: A computer science related question that the user wants to be answer taken as a String.
* debug: A boolean indicating whether the question is for debugging purposes in which a potential error is returned to assist in debugging.
* seed: An optional seed to generate the same random result which is taken as a String or Integer.

#### Returns:
* A String representing a solution to common computer science problems or an estimation of when your task will be completed if at all.

### getInspiration(name)
Receives either a famous person's name or an empty string, and returns a random inspirational quote by the specified person. If the string is empty, returns a random inspirational quote by a random person.

#### Args:
* name: A name of a famous person whose quote will be returned and taken as a String.

#### Returns:
* A String representing a quote by a specific or random famous person. If empty, a random quote will be given. If the requested famous person isn't in our data then an appropriate message is returned.

### funny(name)
Receives the name of a person and return a funny quote if the person is one of the 6 preset.

#### Args:
* name: A name of a person whose quote will be returned and taken as a String.

#### Returns:
* A String representing a funny quote said by a specific or random famous person. If empty, a random quote will be given. If the requested famous person isn't in our data then an appropriate message is returned.

## How to Import and Use
* Create a virtual environment using `python -m venv venv` and enter the virtual environment using `source venv/bin/activate` or `source venv/Scripts/activate`.
* Install requirements using `python install -r requirements.txt`.
* Use `pip install fortunetelleracs1029==1.0.0`in the command line to create a pipenv-managed virtual environment and install the latest version of this package.
* Activate the virtual environment using `pipenv shell`.
* Create a Python program and import this package using `from fortunetelleracs1029 import fortuneteller`.
* Call the functions using `fortuneteller.{{function name}}`.
* Run your Python program using `python3 my_program_filename.py`.
* Type `exit` to exit the virtual environment.

### Example:
```
from fortunetelleracs1029 import fortuneteller

fortuneteller.getLifeAdvice("learning")
fortuneteller.getLifeAdvice("detach")
fortuneteller.getLifeAdvice("learning", "super cool seed")
fortuneteller.getLifeAdvice("detach", 12345)

fortuneteller.getCSFortune("Will I finish this project?", False)
fortuneteller.getCSFortune("Why is my code not compiling?", True)
fortuneteller.getCSFortune("Will I finish this project?", False, "super cool seed two")
fortuneteller.getCSFortune("Why is my code not compiling?", True, 123456)

fortuneteller.getInspiration("Lemony Snicket")
fortuneteller.getInspiration("Amelia Earhart")
fortuneteller.getInspiration("")
fortuneteller.getInspiration("A person who does not exist")

fortuneteller.funny("Steven Wright")
fortuneteller.funny("Oscar Wilde")
fortuneteller.funny("")
fortuneteller.funny("A person who does not exist")

```

## How to Contribute, Build and Test
* Clone the project using `git clone https://github.com/software-students-fall2022/python-package-exercise-project-3-team-16.git`.
* Create a virtual environment using `python -m venv venv` and enter the virtual environment using `source venv/bin/activate` or `source venv/Scripts/activate`.
* Enter the project directory using `cd python-package-exercise-project-3-team-16`.
* Install requirements using `python install -r requirements.txt`.
* Use `pip install fortunetelleracs1029==1.0.0`in the command line to create a pipenv-managed virtual environment and install the latest version of this package.
* Activate the virtual environment using `pipenv shell`.
* Edit the file `test_fortuneteller.py` to create or build upon test cases.
* Build the project by running `python -m build`.
* Run the tests from the main project directory using `python3 -m pytest`.
* Type `exit` to exit the virtual environment.

### Example Test:
```
def test_getCSFortune_seed(self):
    """
    Make sure that the text returned by the getCSFortune() function is the same when given the same seed.
    """
    actual = fortuneteller.getCSFortune("question", True, "super secret seed")
    for i in range(100):
        assert actual == fortuneteller.getCSFortune("question", True, "super secret seed")

    actual = fortuneteller.getCSFortune("question", False, "super secret seed")
    for i in range(100):
        assert actual == fortuneteller.getCSFortune("question", False, "super secret seed")
```
