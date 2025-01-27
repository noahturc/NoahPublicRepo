# medium
# finds highest number in a list
def find_highest(lst):
  highest = lst[0]
  for num in lst:
    if num > highest:
      highest = num
  return highest
#print(find_highest([2,4,9,4,8]))



# medium
def fizz_buzz(num):
  if num is not None:
    if (num%3 == 0) and (num%5 == 0):
      print('FizzBuzz')

    elif num%3 == 0:
      print('Fizz')
    elif num%5 == 0:
      print('Buzz')
    else:
      print(str(num))
  else:
    print('None')
#fizz_buzz(3)



# hard
def snakefill(n):
  x = n*n
  snake = 1
  i = 0
  while snake <= x:
    snake *= 2
    i += 1
  return i - 1
#print(snakefill(24))



# medium
# converts normal time to 24 hour clock time
def convertTime(time):
  x = time[-2]
  firstTwoDigits = time[:2]
  lastDigits = time[2:]
  if x.upper() == 'A':
    if firstTwoDigits == '12':
      result = '00' + lastDigits 
    else:
      result = time
  
  elif x.upper() == 'P':
    if firstTwoDigits == '12':
      result = time
    else:
      converted = int(firstTwoDigits) + 12
      result = str(converted) + lastDigits 

  else:
    result = 'You supposed to specify PM or AM bruhhh'
   
  return result[:-2]
#print(convertTime('07:05:45PM'))



# medium
def profit(info):
  #x = info.keys()
  return info['sell_price'] * info['inventory'] - info['cost_price'] * info['inventory']
# print(profit({'cost_price': 2.77, 'sell_price': 7.95, 'inventory': 8500}))



# very hard
def staircase(stairs):
  underscores = []
  hashes = []  
  if stairs < 0:
    stairs = abs(stairs)
    for number in range(stairs + 1):
      hashes.append(number)
    underscores = hashes[:-1]
    underscores = underscores[::-1]
    hashes = hashes[1:]
    for number in underscores:
      print(underscores[number] * '_' + '#' * hashes[number])

  elif stairs > 0:
    for number in range(stairs + 1):      
      hashes.append(number)
    underscores1 = hashes[:-1]
    underscores = underscores1[::-1]
    hashes = hashes[1:]
    for number in underscores1:
      print(underscores[number] * '_' + '#' * hashes[number])

  else:
    print('ZERO')
#staircase(5)
    


# expert
def knightsjump(location):
  positionsLet = ['0', '0', 'a','b','c','d','e','f','g','h', '0', '0']
  positionsNum = ['0', '0', '1','2','3','4','5','6','7','8', '0', '0']
  let = location[0].lower()
  num = location[1]
                          #if knightsjump('d4')
  validLocationsLet1 = [] #c,b
  validLocationsLet2 = [] #e,f
  validLocationsLet1.append(positionsLet[positionsLet.index(let) - 1])
  validLocationsLet1.append(positionsLet[positionsLet.index(let) - 2])
  validLocationsLet2.append(positionsLet[positionsLet.index(let) + 1])
  validLocationsLet2.append(positionsLet[positionsLet.index(let) + 2])

  validLocationsNum1 = [] #2,3
  validLocationsNum2 = [] #6,5
  validLocationsNum1.append(positionsNum[positionsNum.index(num) - 2])
  validLocationsNum1.append(positionsNum[positionsNum.index(num) - 1])
  validLocationsNum2.append(positionsNum[positionsNum.index(num) + 2])
  validLocationsNum2.append(positionsNum[positionsNum.index(num) + 1])

  x = []
  y = []
  z = []
  x = validLocationsLet1[0] + validLocationsNum1[0], validLocationsLet1[0] + validLocationsNum2[0], validLocationsLet2[0] + validLocationsNum1[0], validLocationsLet2[0] +validLocationsNum2[0] 
  y = validLocationsLet1[1] + validLocationsNum1[1], validLocationsLet1[1] + validLocationsNum2[1], validLocationsLet2[1] + validLocationsNum1[1], validLocationsLet2[1] +validLocationsNum2[1] 
  z = x + y

  z_filtered = [i for i in z if '0' not in i]
  z = z_filtered

  print(z)
#knightsjump('D8')



# hard
# Create a function to check if a candidate is qualified in an imaginary coding interview of an imaginary tech startup.
# You will be given a list of time taken by a candidate to solve a particular question and the total time taken by the candidate to complete the interview.
def interview(times, sumlst):
  try:
    if (times[0] <= 5 and times[1] <= 5) and (times[2] <= 10 and times[3] <= 10) and (times[4] <= 15 and times[5] <= 15) and (times[6] <= 20 and times[7] <= 20) and (sumlst <= 120):
      print('Qualified')

    else:
      print('Disqualified') 
  except IndexError:
    print('Disqualified')
#interview([5, 5, 10, 10, 15, 15, 20, 20], 120)
    


# hard
def encode_morse(message):
  char_to_dots = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', ' ': ' ', '0': '-----',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '&': '.-...', "'": '.----.', '@': '.--.-.', ')': '-.--.-', '(': '-.--.',
    ':': '---...', ',': '--..--', '=': '-...-', '!': '-.-.--', '.': '.-.-.-',
    '-': '-....-', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.'}
  
  splitMessage = [character for character in message]
  result = []
  for character in splitMessage:
    character = char_to_dots[character.upper()]
    result.append(character)
  result = ' '.join(result)
  print(result)
#encode_morse('help me')
  


# expert
def minesweeper(ThreeDimensionalArray):
  
  for iteration1, array in enumerate(ThreeDimensionalArray):
    for iteration2, number in enumerate(range(len(array))):
          
      if array[number] == 1:
        array[number] = 9
          
  for iteration1, array in enumerate(ThreeDimensionalArray):
      for iteration2, number in enumerate(range(len(array))):

        topLeft = [0, 0]
        topRight = [0, len(array) - 1]
        bottomLeft = [len(ThreeDimensionalArray) - 1, 0]
        bottomRight = [len(ThreeDimensionalArray) - 1, len(array) - 1]
    
        if array[number] == 0:
          if [iteration1, iteration2] == topLeft:
            x = 'TopLeft'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[0][1], ThreeDimensionalArray[1][0], ThreeDimensionalArray[1][1]]
            array[number] = surroundingNumbers.count(9)

          elif [iteration1, iteration2] == topRight:
            x = 'TopRight'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[0][len(array)-2], ThreeDimensionalArray[1][len(array)-2], ThreeDimensionalArray[1][len(array)-1]]              
            array[number] = surroundingNumbers.count(9)

          elif [iteration1, iteration2] == bottomLeft:
            x = 'Bottomleft'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[len(ThreeDimensionalArray) - 1][1], ThreeDimensionalArray[len(ThreeDimensionalArray) - 2][0], ThreeDimensionalArray[len(ThreeDimensionalArray) - 2][1]]
            array[number] = surroundingNumbers.count(9)

          elif [iteration1, iteration2] == bottomRight:
            x = 'BottomRight'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[len(ThreeDimensionalArray) - 1][len(array) - 2], ThreeDimensionalArray[len(ThreeDimensionalArray) - 2][len(array) - 1], ThreeDimensionalArray[len(ThreeDimensionalArray) - 2][len(array) - 2]]
            array[number] = surroundingNumbers.count(9)         

          elif iteration1 == 0:
            x = 'TopRow'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[0][iteration2 - 1], ThreeDimensionalArray[0][iteration2 + 1], ThreeDimensionalArray[1][iteration2 - 1], ThreeDimensionalArray[1][iteration2], ThreeDimensionalArray[1][iteration2 + 1]]
            array[number] = surroundingNumbers.count(9)

          elif iteration2 == 0:
            x = 'LeftColumn'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[iteration1][1], ThreeDimensionalArray[iteration1 - 1][0], ThreeDimensionalArray[iteration1 - 1][1], ThreeDimensionalArray[iteration1 + 1][0], ThreeDimensionalArray[iteration1 + 1][1]]
            array[number] = surroundingNumbers.count(9)

          elif iteration2 == len(array) - 1:
            x = 'RightColumn'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[iteration1][len(array) - 2], ThreeDimensionalArray[iteration1 - 1][len(array) - 2], ThreeDimensionalArray[iteration1 - 1][len(array) - 1], ThreeDimensionalArray[iteration1 + 1][len(array) - 2], ThreeDimensionalArray[iteration1 + 1][len(array) - 1]]
            array[number] = surroundingNumbers.count(9)

          elif iteration1 == len(ThreeDimensionalArray) - 1:
            x = 'BottomRow'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[len(ThreeDimensionalArray) - 1][iteration2 - 1], ThreeDimensionalArray[len(ThreeDimensionalArray) - 1][iteration2 + 1], ThreeDimensionalArray[len(ThreeDimensionalArray) - 2][iteration2 - 1], ThreeDimensionalArray[len(ThreeDimensionalArray) - 2][iteration2], ThreeDimensionalArray[len(ThreeDimensionalArray) - 2][iteration2 + 1]]
            array[number] = surroundingNumbers.count(9)

          else:
            x = 'MiddleNumbers'
            surroundingNumbers = []
            surroundingNumbers = [ThreeDimensionalArray[iteration1 - 1][iteration2 - 1], ThreeDimensionalArray[iteration1 - 1][iteration2], ThreeDimensionalArray[iteration1 - 1][iteration2 + 1], ThreeDimensionalArray[iteration1 + 1][iteration2 - 1], ThreeDimensionalArray[iteration1 + 1][iteration2], ThreeDimensionalArray[iteration1 + 1][iteration2 + 1], ThreeDimensionalArray[iteration1][iteration2 - 1], ThreeDimensionalArray[iteration1][iteration2 + 1]]
            array[number] = surroundingNumbers.count(9)

  
      print(ThreeDimensionalArray[iteration1])
'''minesweeper([
  [0, 0, 0],
  [0, 0, 0],
  [0, 1, 0]
])'''



import re
# expert
def is_authentic_skewer(skewer1):
  skewer2 = ''.join(letter for letter in skewer1 if letter.isalnum()) 
  vowels = ['a', 'e', 'i', 'o', 'u']
  consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
  alphabet = vowels + consonants
  
  #makes sure dashes are consistent
  pattern = '|'.join(map(re.escape, alphabet))  # Constructing a pattern to match any letter in the list
  result = re.split(pattern, skewer1[1:])  # Splitting the string using the pattern
  result = [part for part in result if part]  # Filtering out empty strings
  itr = 0
  for dashList in result:
    lenResult = len(result)
    if itr == lenResult - 1:
      break
    elif len(dashList) == len(result[itr+1]):
      itr += 1
    else:
      return False

  #makes sure it alternates between consonants and vowels
  rangeSkewer2 = range(len(skewer2))
  evens = []
  odds = []
  
  for number in rangeSkewer2:
    evens.append(number)
  evens = evens[1:]
  for number in evens:
    if number % 2 == 0:
      evens.remove(number)      
  for number in evens:
    if skewer2[number].lower() not in vowels:
      return False
    
  for number in rangeSkewer2:
    odds.append(number)
  for number in odds[1:]:
    if number % 2 == 1:
      odds.remove(number)          
  for number in odds:
    if skewer2[number].lower() not in consonants:
      return False
  
  #makes sure it doesn't start or end with a vowel
  if (skewer2[0].lower() in vowels) or (skewer2[-1].lower() in vowels):
    return False
  else:
    return True
#print(is_authentic_skewer('r-----a-----b-----b-----t')) 



# very hard
def simplify(fraction):
  fractionSplit = fraction.split('/')
  numerator = int(fractionSplit[0])
  denominator = int(fractionSplit[1])
  
  numeratorList = []
  for number in range(numerator+1):
    numeratorList.append(number)
  numeratorList.reverse()
  denominatorList = []
  for number in range(denominator+1):
    denominatorList.append(number)
  denominatorList.reverse()
  
  for numeratornumber in numeratorList[:-1]:
    dividednum = denominator / numeratornumber
    x = numerator / numeratornumber
    if str(dividednum)[-1] == '0':
      
      if str(x)[-1] == '0':
        topint = int(numerator / numeratornumber)
        bottomint = int(denominator / numeratornumber)
        result = str(topint) + '/' + str(bottomint)
        break     
      else:
        pass

    else:
      result = 'Float'
  if result == fraction:
    result = 'Already in simplest form'
  return result
#print(simplify('49/7'))



# medium
# The use of the len() function is prohibited.
def length(number):
  def real_count(OGList, countList):
    z = int()
    for item in countList:
      z += OGList.count(item)    
    return z

  x = []
  for digit in str(number):
    x.append(digit)

  result = real_count(x, ['0','1','2','3','4','5','6','7','8','9'])
  return result
print("\n", length(200))



# under construction
# expert
def pascalsTriangle(pyramidSize):
  print('''       
           [ 1 ]
        [ 1 ][ 1 ]
     [ 1 ][ 2 ][ 1 ]
   [ 1 ][ 3 ][ 3 ][ 1 ]
[ 1 ][ 4 ][ 6 ][ 4 ][ 1 ]
        ''')

  for size in range(pyramidSize):
    pass
pascalsTriangle(3)