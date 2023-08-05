import json
import os

class Animal:
    def __init__(self, name='lion', turns=20, interactions={
        'poke': ['it roars and bites your hand off', 10],
        'look': ['its yellow fur glistens gracefully in the sun', 1],
        'yell': ['it glances over at you and yawns, bearing its four large canines', 2],
        'look around': ['surrounding you are beautiful African plains', 1],
        'pet': ['its large mane feels good through your fingers', 3]
        }, letter_match=8) -> None:
        self.name = name
        self.turns = turns
        self.interactions = interactions
        self.letter_match = letter_match

def import_file(fpath):
    '''
    takes input file as string that contains details about interactions and rules so user can create their own game
    '''
    ## Example Usage: import_file('../../example.json')
    if fpath == None:
        print("No file path provided. Using default values.")
        print("Example Usage: import_file('../../example.json')")
        return Animal()
    if not fpath.endswith('.json'):
        print("File must be a .json file.")
        return Animal()
    if os.path.isfile(fpath):
        f = open(fpath)
        try:
            imported_animal = json.load(f)
        except:
            print("Invalid file format. Please try again.")
            return None
        try:
            animal = Animal()
            try: 
                if len(imported_animal['name']) > 0:
                    animal.name = imported_animal['name']
                else:
                    print("Invalid name. Using default name.")
            except: print("Error: name not found. Using default name.")
            try: 
                if imported_animal['turns'] > 0:
                    animal.turns = imported_animal['turns']
                else:
                    print("Invalid number of turns. Using default number of turns.")
            except: print("Error: turns not found. Using default turns.")
            try: 
                if len(imported_animal['interactions']) > 0:
                    animal.interactions = imported_animal['interactions']
                else:
                    print("Invalid number of interactions. Using default interactions.")
            except: print("Error: interactions not found. Using default interactions.")
            try: 
                if imported_animal['letter_match'] > 0:
                    animal.letter_match = imported_animal['letter_match']
                else:
                    print("Invalid number of letter_match. Using default letter_match.")
            except: print("Error: letter_match not found. Using default letter_match.")
            print("End of import")
            f.close()
            return animal
        except:
            print("Error: " + "An exception occurred, return default animal.")
            f.close()
            return Animal()
    else:
        print("File not found or Path is incorrect, return default animal.")
        return Animal()

def interact(action:str, animal:Animal):
    '''
    takes action as string and prints result of action.
	accesses a dictionary of lists where lists store result of action and turn/healthpoint loss.
    '''
    act_arr = animal.interactions.get(action)
    animal.turns = animal.turns - act_arr[1]
    return act_arr[0]

def letter_match(letter, animal:Animal):
    '''
    takes a letter as input and returns whether or not letter is in animal name.
    returns array of indices where letter matches.
    '''
    animal.turns = animal.turns - animal.letter_match
    matches = []
    for i in range(len(animal.name)):
        if (letter == animal.name[i]):
            matches.append(i+1)
    animal.turns -= 1
    return matches


def handle_letter_match(animal:Animal, guesses:list):
    '''
    handling user interaction w/ letter match
    '''
    print("Guesses made: ", guesses)
    inp = input("Guess a letter: ").lower().strip()
    if (len(inp)>1):
        print("Input only 1 letter!")
        return False
    elif (inp in guesses):
        print("Already guessed this letter. Pick another.")
        return False
    else:
        guesses.append(inp)
        letter_arr = letter_match(inp, animal)

        if(len(letter_arr) == 0):
            print('No letter matches!')
        else:
            print('Matches at these positions: '+stringify(letter_arr))
        
        return True



def guess(guess_name, animal:Animal):
    '''
    takes name of animal as string and returns true or false
    '''
    if(guess_name == animal.name.lower().strip()):
        return True
    else:
        animal.turns = animal.turns - 1
        return False   

def handle_guess(animal:Animal):
    '''
    handling user interaction when guessing
    '''
    inp = input("Guess the animal: ").lower().strip()
    return guess(inp, animal)

def stringify(keys):
    output = ''
    for key in keys:
        output += '\n\t'+str(key)
    return output
