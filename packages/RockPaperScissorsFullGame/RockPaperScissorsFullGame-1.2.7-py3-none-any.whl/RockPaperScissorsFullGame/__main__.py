# import RockPaperScissorsFullGame.RPS as RPS
# import RockPaperScissorsFullGame.ML as ML
import RPS
import ML

def main():
    # arr = [{1 : {'player': 'Paper', 'computer': 'Rock'}}, {2 : {'player': 'Scissors', 'computer': 'Paper'}}, {3 : {'player': 'Rock', 'computer': 'Scissors'}}, {4 : {'player': 'Paper', 'computer': 'Paper'}}]
    # for kvp in arr :
    #     ML.rpsStorage.update(kvp)
    ML.printRps()
    #print welcome banner
    print("""    
      __        __   __         __   ___  __     __   __   __          __        __   ___  __     __   __     __   __   __   __   __  
|  | |__  |    /  ` /  \  |\/| |__    |  /  \   |__) /  \ /  ` |__/   |__)  /\  |__) |__  |__)   /__` /  ` | /__` /__` /  \ |__) /__` 
|/\| |__  |___ \__, \__/  |  | |__    |  \__/   |  \ \__/ \__, |  \   |    /--\ |    |___ |  \   .__/ \__, | .__/ .__/ \__/ |  \ .__/                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    """)
    
    #first ask user if they want to see ascii art
    asciiVisibility = RPS.setAsciiVisibility()
    
    #Prompting game difficulty
    difficulty = ML.chooseDifficulty()
    if (difficulty.value == 1) :
        print("You chose easy difficulty! Computer will be on random mode.") 
    elif (difficulty.value == 2) :
        print("You chose hard difficulty! Computer will be using history matching.")

    # if user enters difficulty greater than easy, ask user if they want to turn on text-detail mode (to see how computer tracks history)
    # by default, detail mode is set to false
    # showDetails will be passed to the ML.py functions that are responsible for printing out the logic behind the computer move
    showDetails = False
    if (difficulty.value > 1):
        details = input("Do you want to turn on detail mode?\nselect one\n(1) Yes\n(2) No\n")
        if (details == "1" or details.lower() == "yes"): 
            showDetails = True
        elif (details == "2" or details.lower() == "no"):
            showDetails = False
        else:
            print("Invalid input... defaulting detailed mode to false")

    # game
    play = True
    round = 1
    while (play):
        #Initialize computer choice (computerItem) to None during the start of every round.
        computerItem = None

        #Easy mode: randomizes and returns an rps item for the computer choice.
        if (difficulty.value == 1) :
            computerItem = RPS.getComputerItem()

        #Medium mode: calls ML_historyMatching() to make the computer choice.
        elif (difficulty.value == 2) :
            #Current round has to be at least 3 since minimum past rounds checked is 2.
            if round >= 3 :
                #If there is a successful prediction, the computer choice will be chosen to counter the predicted player item.
                # pass showDetails... if true then the func will print out 
                predictedPlayerItem = (ML.ML_callHistoryMatching("computer", showDetails))
                if (predictedPlayerItem  != None) :
                    #only print predicted move if in text-detail mode
                    if(showDetails):
                        print("predicted move: ", predictedPlayerItem) #
                    if (predictedPlayerItem['player'] == 'Scissors') :
                        computerItem = RPS.Item.Rock
                    elif (predictedPlayerItem['player'] == 'Paper') :
                        computerItem = RPS.Item.Scissors
                    elif (predictedPlayerItem['player'] == 'Rock') :
                        computerItem = RPS.Item.Paper
            
            #If there are no successful predictions, the computer choice will default to random.
            if (computerItem == None) :
                computerItem = RPS.getComputerItem()

        #Prompts player input.
        playerInput = input("Enter your item: (rock, paper, scissors) ")

        #Allows the player to end the program with "quit" as the input.
        if(playerInput.lower() == "quit"):
            print("Thank you for playing!\n")
            break

        else:
            #Assigns an rps item corresponding to the user input.
            playerItem = RPS.inputToItem(playerInput)

            #If user input doesn't correspond to any rps item, prompts user input
            #and restarts the program.
            if (playerItem == None):
                print("Invalid Input\n")
                continue

            else:
                playerMove = RPS.getPlayerAsciiArt(playerItem)
                computerMove = RPS.getComputerAsciiArt(computerItem)
                if(not asciiVisibility):
                    print("You choose " + playerItem.name + ". Computer chooses " + computerItem.name + ".")
                else:
                    print("Player Move: " + playerItem.name + playerMove)
                    print("Computer Move: " + computerItem.name + computerMove)
                result = RPS.getOutcome(playerItem,computerItem)
                print("You " + result.name + ".\n")

                #Offering history matching
                # print(ML.ML_callHistoryMatching("player"))

                #Print rpsStorage
                ML.printRps(showDetails)
        
        #Tracking the round
        round += 1


if __name__ == '__main__':
    main()