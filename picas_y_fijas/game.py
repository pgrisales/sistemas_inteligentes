import random
from model import solve

# Returns list of digits of a number
def getDigits(num):
    return [int(i) for i in str(num)]
  
# No duplicate digits 
def noDuplicates(num):
    num_li = getDigits(num)
    if len(num_li) == len(set(num_li)):
        return True
    else:
        return False
  
# Generates a 4 digit number with no repeated digits    
def generateNum():
    while True:
        num = random.randint(1000,9999)
        if noDuplicates(num):
            return num
  
# Returns No picas y fijas
def numOfBullsCows(num,guess):
    bull_cow = [0,0]
    num_li = getDigits(num)
    guess_li = getDigits(guess)
      
    for i,j in zip(num_li,guess_li):
        if j in num_li:
            # common digit exact match (fijas)
            if j == i:
                bull_cow[0] += 1
            # common digit match but in wrong position (picas)
            else:
                bull_cow[1] += 1
                  
    return bull_cow
      
def start():
  num = generateNum()
  tries = 0
  win = False   
  bull_cow = [0,0]

  print()
  print(num)
  print()

  while not win:
    tries += 1
    guess = solve(bull_cow[1], bull_cow[0])
      
    bull_cow = numOfBullsCows(num,guess)
    print(f"{bull_cow[0]} bulls, {bull_cow[1]} cows\n")
    print('Number of tries: ', tries)

    if bull_cow[0] == 4:
      print(num)
      print("\nYou guessed right!")
      print("Number of tries: ", tries)
      win = True
      break

