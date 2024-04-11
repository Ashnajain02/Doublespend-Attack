import random
import math
import sys

# Wouldnt it be nice for graders to see your explaination of what craziness you are doing???
def satoshi(q,z):
    p = 1 - q
    l = (z * q) / (p)
    probability = 0
    for k in range(z):
        probability += (((l ** k) * math.exp(-l)) / math.factorial(k)) * (1 - (q/p) ** (z - k))
    return 1 - probability

# Remember to comment the what, why and high-level how
# Dont explain basic python language features.  Expect that your reader knows python.  Explain what you are trying to do and how the python code
# gets there!
MAX_LEAD = 35
def monteCarlo(q,z, numTrials=50000):
    winA = 0
    for i in range(numTrials):
       winner = simulate(q, z)
       if winner == 'A': winA += 1
          
    return winA/numTrials

def simulate(q, z):
   #win for attacker: when the attacker ties in the number of blocks as the honest miner
   lenA = 0 
   lenH = 0 

   while True:
      if lenH >= z and lenA >= lenH:
         return "A"
      elif lenH >= z and lenH - lenA >= MAX_LEAD:
         return "B"
      
      random_num = random.uniform(0, 1)
      if random_num <= q:
         lenA += 1
      else:
         lenH += 1
   

def markovChainSum(q,z):
    #so we dont simulate this for a number of trials??
    cache = {}
    return markovChainRecurse(q, z, 0, cache, 0, 0)
   
#instead of using a random number to decide if we found a block or not -> will use a probability
def markovChainRecurse(q, z, A, cache, lenA, lenH):
   #q: attacker power
   #z: embargo interval 
   #A: attackers lead

    if (q**lenA * (1-q)**lenH) < 1/1e60:
       #ATTCKER LOST
       return 0.0

    if lenH >= z and A >= 0: #and lenA >= z
       #since lenH >= z: the embargo period is over
       #therefore lenA also be >= z
       #and A >= 0

       #ATTACKER WINS
       return 1.0 
    

    if (lenA, lenH) in cache:
      return cache[(lenA, lenH)]
    else:
        pWon = q * markovChainRecurse(q, z, A + 1, cache, lenA + 1, lenH)
        pLost = (1 - q) * markovChainRecurse(q, z, A - 1, cache, lenA, lenH + 1)

        cache[(lenA, lenH)] = pWon + pLost
        return cache[(lenA, lenH)]
   
# Testing your work by repeated submission is a giant waste of your time.  Always optimize your time when coding!!!
# Instead, write your own tests!
def Test():
  # Your algorithm might go deep, so you may need to change the recursion limit.
  # At the same time, this might make an infinite recursion hard to find
  sys.setrecursionlimit(5000)
  q=0.3

  for z in range(0,11):
    s = satoshi(q,z)
    mc = monteCarlo(q,z, 10000)
    ms = markovChainSum(q,z)
    print("q:", q, " z:", z, " satoshi: %3.3f" % (s*100), " monte carlo: %3.3f" % (mc*100), " markov sum: %3.3f" % (ms*100))

Test()