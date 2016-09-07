#!/usr/bin/env python3
# encoding: utf-8
import re, random

docstring = "data/robin.txt"
with open(docstring) as robin:
    master_list = robin.read().splitlines()

used = set()

def getWords(word, word_set):
    matches = []
    search_space = " ".join(list(word_set)) # unused words converted to string
    for i in range(4): # create regexes to find words differing by one letter
        srcstr = r'{0}\w{1}'.format(word[0:i], word[i+1:4])
        found = re.findall(srcstr, search_space)
        if len(found) > 0: # only append actual results
            matches.append(found)
    if len(matches) > 0: # flatten and return list of lists
        matches = [match for ml in matches for match in ml]
        return matches
    return None # in case no matches found

def addWord(word):
    toADD = input("\tAre you sure this is a real word? (y/n) ")
    toADD = toADD.lower()
    if toADD[0] == "y":
        master_list.append(word)
        print("That word will be added to my memory for the next game.")

def testMove(move, currWord, solutions, word_set):
    if len(move) != 4:
        if move == "protest":
            master_list.remove(currWord)
            raise Exception("\tThat word will be removed from my memory.")
        else:
            raise Exception("\tThat is not 4 letters long.")
    elif move in used:
        raise Exception("\tThat word has already been used.")
    elif move not in word_set:
        raise Exception("\tI am not familiar with this word.")
    elif move not in solutions:
        raise Exception("\tThat is not a valid answer.")

def Main():
    currWord = '' # placeholder
    used.clear() # need to clear for repeated games
    unused = set(master_list)

    while True: # loop for a single game
        solutions = getWords(currWord, unused) if currWord != '' else master_list
        if len(used) % 2 == 0: # computer's turn
            if solutions != None: # select move from available
                currWord = random.choice(solutions)
            else:
                print("The computer has run out of words after {0} moves. You win!".format(len(used)))
                return True # humanwin = true
            print("CPU move:\t{0}".format(currWord))

        else: # human's turn
            if solutions != None: # if moves available
                while True: # exception handling loop, exits on valid move
                    move = input("Your move: ").lower() # ask for word
                    try: # accept only if it passes tests
                        testMove(move, currWord, solutions, unused)
                        currWord = move
                        break
                    except Exception as e:
                        print(e, "({0})".format(currWord))
                        e = str(e)
                        if e == "\tI am not familiar with this word.":
                            addWord(move)
            else:
                print("There are no words left after {0} moves. You lose.".format(len(used)))
                return False # humanwin = false
        used.add(currWord) # add to used words set
        unused.remove(currWord) # keep unused list current
        print("")

def displayResults(results):
    if results["games"] > 1:
        print("""
You played {0} game(s).
Of those you won {1} and lost {2}.""".format(results["games"], results["wins"],
    results["losses"]))

    if results["forfeit"] > 0:
        print("You forfeit {0} game(s)".format(results["forfeit"]))

    print("\nThanks for playing! Come again some time.")

def writeMaster(ml):
    ml = sorted(list(set(ml)))
    with open(docstring, "w") as robin:
        for word in ml:
            robin.write("{0}\n".format(word))

if __name__ == '__main__':
    # Instructions
    print("""
Do you think you have what it takes to beat the computer? The game
is simple: the computer chooses a word at random, with turns alternating
thereafter. Make a move by changing the word into another valid four-letter
word by changing one letter. Each word may only be used once. The game
continues until there are no valid words left. The loser is the player that
has no more valid moves. Press Ctrl-C to quit at any time.
        """)

    results = {"games" : 0, "wins" : 0, "losses" : 0, "forfeit" : 0, "draws" : 0}

    while True: # main game loop
        try:
            humanWin = Main() # play a game, return result
            if humanWin: # increment W-L record
                results["wins"] += 1
            else:
                results["losses"] += 1

        except KeyboardInterrupt:
            results["forfeit"] += 1

        results["games"] += 1 # increment games played always
        print("")
        playAgain = input("Do you want to play again? (y/n) ").lower()
        if playAgain[0] != "y": # Start another game if the player wishes
            displayResults(results)
            writeMaster(master_list)
            break # exit program and display results if not

# TODO: add ability to handle ultra rare but theoretically possible draw
# scenario, update instructions, prevent instalosses, add ability to protest,
# add words even after last move (game is over)
