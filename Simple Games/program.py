import random

import math

lower = int(input('Enter lower bound: '))
higher = int(input('Enter higher bound: '))
numb = random.randint(lower, higher)
amount = round(math.log(higher - lower + 1, 2))
print("\n\tYou've only got ",
      amount,
      " chances to guess the number!\n")

chances = 0

while chances < math.log(higher - lower + 1, 2):
    chances += 1

    guess = int(input('guess a number: '))

    if guess == numb and chances == 1:
        print('Congrats! You guessed correctly in ', chances, 'try')
        break
    elif guess == numb:
        print(print('Congrats! You guessed correctly in ', chances, 'tries'))
        break
    elif guess > numb:
        print('Nope, that number is too high.')
    else:
        print('Nope, that number is too low.')

if amount <= chances:
    print('You have ran out of guesses. the correct number was', numb, 'Better luck next time! ')
