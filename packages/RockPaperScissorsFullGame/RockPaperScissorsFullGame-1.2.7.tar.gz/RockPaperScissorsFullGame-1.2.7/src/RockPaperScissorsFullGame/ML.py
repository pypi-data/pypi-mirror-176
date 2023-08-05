#Machine Learning functions for higher difficulties
import RPS
# import RockPaperScissorsFullGame.RPS as RPS
from enum import Enum

#Stores the results of each round in a dictionary: 
#{round : {"player" : playerchoice, "computer" :computerchoice}}.
rpsStorage = {}

#Arrays track the rounds for which the outcome occurs.
winsArr = []
lossesArr = []
tiesArr = []

#Variables track the number of rounds and outcomes.
round = 1
wins = 0
losses = 0
ties = 0

#Difficulties
class difficulty(Enum):
    Easy = 1
    Hard = 2

#Prompt the user for choice of difficulty and returns difficulty 
#if the difficulty begins with the input.
def chooseDifficulty() :
    playerInput = input("Enter your preferred difficulty (easy, hard): ")
    if ("easy").startswith(playerInput.lower()): 
        return difficulty.Easy
    elif ("hard").startswith(playerInput.lower()): 
        return difficulty.Hard
    else:
        return None

#Stores the outcome of a round and players' choices (player and computer)
#in the rpsStorage dictionary. Tracks wins, losses, and ties.
def storeOutcome(outcome, playerChoice, computerChoice) :
    global round 
    global wins 
    global losses 
    global ties 

    if (outcome == "Win") :
        kvp = {round : storeChoices(playerChoice, computerChoice)}
        rpsStorage.update(kvp)
        winsArr.append(round)
        round += 1
        wins += 1
        return kvp
    elif (outcome == "Lose") :
        kvp = {round : storeChoices(playerChoice, computerChoice)}
        rpsStorage.update(kvp)
        lossesArr.append(round)
        round += 1
        losses += 1
        return kvp
    elif (outcome == "Tie") :
        kvp = {round : storeChoices(playerChoice, computerChoice)}
        rpsStorage.update(kvp)
        tiesArr.append(round)
        round += 1
        ties += 1
        return kvp
    else :
        return None

#Auxiliary function: Creates the choices dictionary for rpsStorage.
def storeChoices(playerChoice, computerChoice) :
    return {"player" : playerChoice, "computer" : computerChoice}

#Prints the current outcomes in rpsStorage 
# showDetails defaults to true so that it does not impact unit tests
def printRps(showDetails=True) :
    #If there aren't any values in RPS storage (shouldn't ever be the case), prints 0.
    # only print if in text-detail mode
    if(showDetails):
        if len(rpsStorage) == 0:
            print(0)
        else :
            tracker = 1

            print("\nOutcomes of the previous rounds: ")

            #Printing the round and the value in the rpsStorage for the outcome of each round.
            for kvp in rpsStorage.values() :
                print(tracker, " : ", kvp)
                tracker += 1

            print("")

#Iterates through rpsStorage to check if the outcomes from a previous number
#of rounds before the current one has been repeated before. Returns the next
#expected outcome after the repeated interval of outcomes if there is a repeated
#segment. If there isn't a repeated segment, the previous number of rounds checked
#is decremented and checked again. This repetition occurs until number of rounds
#is lower than 2 (not really a segment).
# showDetails defaults to true so that it does not impact unit tests
def ML_historyMatching (numRounds, showDetails=True) :
    #Fetching the values in rpsStorage dictionary.
    resultsArr = list(rpsStorage.values())

    while numRounds != 1 :
        fractResultsArr = []

        #Iterates through the last n rounds and stores their key-value pairs into fractResultsArr[]. 
        for index in range(len(resultsArr) - numRounds, len(resultsArr), 1) :
            fractResultsArr.append(resultsArr[index])

        #Using the auxiliary function find_subarray(), a segment of key-value pairs in the larger resultsArr[] 
        #containing the key-value pairs of the smaller fractResultsArr[] will be found. An index will be returned
        #that will serve as the starting index for the segment of key-value pairs in resultsArr[] that match the 
        #ones in fractResultsArr[].
        startIndex = find_subarray(resultsArr, fractResultsArr)
        
        # only print if in text-detail mode
        if(showDetails):
            print("this is the fract results arr: ", fractResultsArr) #
            print("this is the start index: ", startIndex) #

        #If there are no segments of key-value pairs in the larger resultsArr[] which match the ones in
        #the smaller fractResultsArr[], the number of past rounds checked will be decremented. This loop continues
        #until past rounds equals 1. 
        if startIndex == None :
            numRounds -= 1
            continue

        #Returns the expected move the player will play after the matched segment. Checks if the expected move is in
        #the bounds of the resultsArr (numRounds can't encompass the entire array AND the matching segment cannot be last n 
        #rounds).  
        elif not (startIndex + numRounds >= len(resultsArr)):
            return resultsArr[startIndex + numRounds]

        numRounds -= 1
    return None

#Auxiliary function to call ML_historyMatching and prompt the user for num rounds input.
def ML_callHistoryMatching(caller, showDetails=True) :
    global round

    #Prompts player input if the caller is the player
    if ("player").startswith(caller.lower()) :
        playerInput = input("Would you like to check the history (yes or no)?\n")

        #If the player's response is yes, prompts for how many past rounds to check.
        if ("yes").startswith(playerInput.lower()) :
            playerInput = int(input("How many rounds?\n"))

            #Checks if the player wants to check an appropriate number of past rounds (makes sure the current round is more than the number of past rounds).
            if (playerInput >= 2 and round > playerInput) :
                return ML_historyMatching(playerInput, showDetails)
            else :
                return ValueError
        
        #Additional output if user doesn't want to do history matching.
        elif ("no").startswith(playerInput.lower()) :
            print("Next time!")
    
    #If the caller is the computer, automatically sets the numRounds to 1 less than the total rounds in the game.
    elif ("computer").startswith(caller.lower()) :
        if (round >= 3) :
            return ML_historyMatching(round-2, showDetails)
    
    return None
      
#Checks if the first array contains the second array.
def find_subarray(first_arr, second_arr):
    first = 0
    second = 0

    first_len = len(first_arr)
    second_len = len(second_arr)

    while first < first_len and second < second_len:
        #From the beginning of each array, every element is matched to check
        #for an equality. In this case, we only want to match the player's past moves
        #to find a pattern so only the key-value pair for the player is checked (hence [0]).
        if (first_arr[first])['player'] == (second_arr[second])['player']:
            first += 1
            second += 1

            #If the second array is completed (has every element equal
            #to an element in the first array in the same order), 
            #second array is contained within the first array.
            if second == second_len:
                return first - second_len

        else:
            #If the second array's element doesn't match the first array's 
            #element, it has to be reset. Likewise, if the second array is
            #reset, the first array has to be checked again from the next 
            #element after the first element which matched the second array's 
            #first element.
            first = first - second + 1
            second = 0

    return None


        
    




    
    
    

