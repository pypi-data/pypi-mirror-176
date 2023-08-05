![Python build & test](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-14/actions/workflows/python-package.yml/badge.svg) [![PyPI version](https://badge.fury.io/py/dailydose.svg)](https://badge.fury.io/py/dailydose)

# Python *`dailydose`* Package

Boredom kills. Here's a package that gives you a daily dose of fun!


## Team Members
* [Sneheel Sarangi](https://github.com/Xarangi)
* [Winston Zhang](https://github.com/Midas0231)
* [Larry Li](https://github.com/86larryli)
* [Paula Seraphim](https://github.com/paulasera)


## Installation

Install the *`dailydose`* module with `pip`.


## Usage

Once installed, *`dailydose`* gives access to the package's 4 special features: today's news in different fields (per Vox Media), random fun facts, and the games of hangman and battleship. The variety of the collection is inspired by the traditional newspaper/magazine experience, in which both information and thought-provoking entertainment is regularly provided. This package is ideal for any program that operates on changing content or stimulating applications. 

*dailydose* supports a command-line interface (CLI). To choose one of the above options, simply call:

```
$ python3 -m dailydose
```

Upon running the package, a main menu is displayed in which your options are listed. Access each feature by entering their corresponding menu number.


## Fun Stuffs To Do

### Fun Facts

- To see a fun fact, press 1 when the main menu is prompted. A random fun fact from [TheFactSite](https://www.thefactsite.com/) will be printed.

- After that, you will be redirected to the main menu.

### Newsfeed

- To see today's news, press 2 when the main menu is prompted. Immediately after, you will be given a list of options to read about: Culture, Politics, Science, World, Technology, Environment, and Business. You also have the option to return to the main menu. 

- Select a field by entering the corresponding listed number. Today's top headlines in the chosen field, as published by Vox Media, as well as a link to read more are printed.

- The content is sourced from their website and therefore changes accordingly.

- Upon receiving the headlines, you will be redirected to the main menu. 

### Hangman Game

- To play the hangman game, press 3 when the main menu is prompted.

- You will then be asked to enter the length of the word you want to guess.

- Upon guessing the correct word or losing the game, you will be redirected to the main menu.

### Battleship Game

- To play the battleship game, press 4 when the main menu is prompted.

- You will then be asked to enter the board dimensions and ship size. You can also choose to use the default settings.

- The game creates a dimension*dimension size board and keeps track of how many turns it takes for you to win! What do you think is the optimal strategy?

- Upon winning or exiting the game, you will be redirected to the main menu.


## Importing the Package

For example usage of the package, see [`example/example.py`](example/example.py).

### 1. `fact.get` -- generate a list of random fun fact objects

```
fact.get(count=1, include_details=True)
```

Parameters

- `count`: how many non-duplicate fun fact objects to return
    - default: 1
    - possible values: [1, 100], inclusive


- `include_details`: whether to return the detailed contents of the facts or only the headings
    - default: True

### 2. `news.get_headlines` -- generate a list of headlines

```
news.get_headlines(subject, titular)
```

Parameters

- `subject`: category name in url slug format on [Vox.com](https://www.vox.com/)
    - possible values: `"culture"`, `"policy-and-politics"`, `"science-and-health"`, `"world"`, `"technology"`, `"energy-and-environment"`, `"business-and-finance"`

- `titular`: a user-friendly display name for the category name
    - possible values: any `str`

### 3. `hang.hangman` -- start an interactive hangman game

```
hang.hangman(num_letter=number_of_letters)
```

Parameters

- `num_letter`: the length of word you want to guess
    - possible values: a string make up of numbers, the length of word acceptable is in between [`"4"`, `"10"`], inclusive

### 4. `battleship.main` -- start an interactive battleship game

```
battleship.main(ship_size="4", dimension="10")
```

Parameters

- `dimension`: the size of the board (dimension * dimension)
    - default: `"10"`
    - possible values: a string make up of numbers, the board dimension acceptable is in between [`"1"`, `"10"`], inclusive

- `ship_size`: the size of the hidden battleship
    - default: `"4"`
    - possible values: a string make up of numbers, the ship size acceptable is in between [`"1"`, `dimension`], inclusive

## Contribute

### Source Code

Clone the package source code from [GitHub repository](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-14).

### Setup Virtual Environment

1. Create a `pipenv`-managed virtual environment and install all required dependencies by running the following command in the main project directory where the `Pipfile` is:

```
pipenv install
```

2. Activate the virtual environment: 

```
pipenv shell
```

3. Then you can test and modify the package!

### Test the Package

1. Run the tests from the main project directory:

```
python3 -m pytest
```

### Build the Package

1. Delete the autogenerated `dist` directory if it exists.

2. Delete the autogenerated `src/*.egg-info` directory if it exists.

3. Build the package by running the following command in the main project directory:

```
python3 -m build
```
