Play rock paper scissors against a computer!

![RPS workflow](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-6/actions/workflows/tests.yml/badge.svg)

## Features
- Fun to play!
- Easy to install
- 100% Test Coverage
- Beautiful ASCII art
- Two different difficulty levels
- A hard difficulty level that utilizes history matching
- A detailed mode that shows the logic behind the computer move
- Tested using GitHub Actions

## Quickstart with pipenv

Installing Rock Paper Scissors Game is simple with [pipenv](https://pypi.org/project/pipenv/). <br>
```pipenv install RockPaperScissorsFullGame```

Run the package directly from the command line: <br>
```python -m RockPaperScissorsFullGame```


## Quickstart without pipenv

Creates a new virtual environment with the name `.venv`:

```bash
python3 -m venv .venv
```

Activate the virtual environment named `.venv`:

On Mac:

```bash
source .venv/bin/activate
```
On Windows:

```bash
.venv\Scripts\activate.bat
```

Install Rock Paper Scissors Game:
```bash
pip install RockPaperScissorsFullGame
```

This package is developed as a game to be played in the shell.<br>
Run the package directly from the command line: 
```bask
python -m RockPaperScissorsFullGame
```

## How to play
### Choose settings
After running the game, you will be asked if you want the ascii art to be visible.<br>
```
Do you want ascii art to be visible?
select one
(1) Yes
(2) No
```
Enter "1" or "yes" if you want to turn on the ascii art.<br>
Enter "2" or "no" if you want to turn off the ascii art.
<br/><br/>
You will be asked to choose the difficulty level.
```
Enter your preferred difficulty (easy, hard): 
```
Enter "easy" to play the easy mode where computer will randomly choose between rock, paper, and scissors. <br>
Enter "hard" to play the hard mode where computer will use history matching to identify pattern then choose the item.
<br/><br/>
**(Hard mode only)**
You will be asked if you want to turn on the detail mode. With detailed mode on, the terminal will show the outcome of previous rounds and how computer chooses the current item based on previous round.
```
Do you want to turn on detail mode?
select one
(1) Yes
(2) No
```
Enter "1" or "yes" if you want to turn on the detail mode.<br>
Enter "2" or "no" if you want to turn off the detail mode.

### Play the game
Play rock paper scissors by choosing the item. 
```
Enter your item: (rock, paper, scissors)
```
Enter "rock" or "r" if you want to choose rock.<br>
Enter "paper" or "p" if you want to choose paper.<br>
Enter "scissors" or "s" if you want to choose scissors.<br>

The shell will print the result of this round. 
```
You choose Paper. Computer chooses Rock.
You Win.
``` 

### Quit the game
Enter "quit" to quit the game. 

## Contributor
[Benji Luo](https://github.com/BenjiLuo)<br>
[Brian Lin](https://github.com/blin007)<br>
[Robert Chen](https://github.com/RobertChenYF)

## Help building this project
1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo#forking-a-repository) our repository([link](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-6)).
2. Contribute and push any changes to your forked repository. 
3. [Create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) from your forked repository. 
4. We will check the pull request and include any meaningful changes when we update the package. 
## Link to the PyPI page
[https://pypi.org/project/RockPaperScissorsFullGame/](https://pypi.org/project/RockPaperScissorsFullGame/)