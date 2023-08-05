from examplepackageTeam12p3 import guess_game as game


def main():
  animal = game.Animal()
  turns = animal.turns
  actions = animal.interactions.keys()
  guesses = []

  print('Welcome to our guessing game! Interact with the animal to receive clues on what it is and make your best guess!')

  while(turns > 0):
    print('\nYour number of turns left: '+str(turns))
    print('Your available actions: '+game.stringify(actions)+'\n\tguess letter\n\tguess')
    guess = handle_input(actions, animal, guesses)

    if(guess):
      print('Congrats! You win!')
      break

    turns = animal.turns

    if(turns <= 0):
      print('Your game has ended! Better luck next time!')

def handle_input(actions, animal, guesses):
  while(True):
    inp = input('What will you do?: ').lower().strip()

    if(inp == 'guess letter'):
      while(True):
          if(game.handle_letter_match(animal, guesses)):
              return False
    elif(inp == 'guess'):
        if(game.handle_guess(animal)):
          return True
        else:
          print('Wrong, try again!')
          return False

    if(inp in actions):
      print(game.interact(inp, animal))
      interactions = animal.interactions
      del interactions[inp]
      return False
    else:
      print('Can\'t do that, sorry!')
      print('Your available actions: '+game.stringify(actions)+'\n\tguess letter\n\tguess')

if __name__ == '__main__':
  main()

