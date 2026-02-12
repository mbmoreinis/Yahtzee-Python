import random
dice = [0,0,0,0,0]
lower = 0
scores = ["quit","ones","twos","threes","fours","fives","sixes", "3 of a kind", "sm straight", "lg straight", "full house", "4 of a kind", "yahtzee", "chance", "yahtzee bonus"]
scored = list()
total = 0;    

# Rolls 5 die into array dice
def roll_hand():
    for d in range(5):
        die = random.randint(1,6)
        dice[d]=die
    print(*dice,sep=", ")

# Rerolls up to specified 5 die in array dice 
def reroll_hand():
    reroll = int(input("Reroll how many 0-5? "))
    if (reroll > 0):
        for d in range(reroll):
            if (reroll != 5):
                d = int(input(f"Reroll which {d+1} of {reroll} (1-5)? "))
            die = random.randint(1,6)
            dice[d-1]=die
        print(*dice,sep=", ")
    return reroll

# Gets category to score hand by
def get_score():
    categories = "Score categories are: \n"
    for s in range(1,len(scores),1):
        categories += str(s)+":"+scores[s]
        if (s < len(scores)-1):
            categories += ", "
        else:
            categories += ".\n Score in which category? "
    category = int(input(categories))
    if (category == 0):
        return -2
    elif (in_scored(category)==True):
        return -1
    else:
        return category
        
def addUp(value):
    score = 0
    for d in range(5):
        if (dice[d] == value):
            score += value
    return score

def addAll():
    score = 0
    for d in range(5):
        score += dice[d]
    return score

def in_scored(category):
    for c in range (len(scored)):
        if (scored[c]==category):
            print("You already scored that.")
            return True
    return False
        
def score_hand(h):
    global total, lower
    toScore = get_score()
    if (toScore == -1):
        toScore = get_score()
    if (toScore == -2):
        return False
    else:
        match toScore:
            case 1 | 2 | 3 | 4 | 5 | 6:
                score = addUp(toScore)
                lower+= score
            case 7:
                score = addAll()
            case 8:
                score = 30
            case 9:
                score = 40
            case 10:
                score = 25
            case 11:
                score = addAll()
            case 12:
                score = 50
            case 13:
                score = addAll()
            case 14:
                score = 100
                h-= 1
            case _:
                score = -1
        if (score == -1):
            print("Invalid entry. You should have entered an integer 1-13.")
            score_hand(h)
        else:
            scored.append(toScore)
            print(f"You scored {score} for {scores[toScore]}")
            total += score
            print(f"Your total is {total} with {h} of 13 hands played.")
            return True
    
def play_game():
    global total
    for h in range(len(scores)-1):
        if (h>0):
            roll_hand()
            rr = reroll_hand()
            if (rr > 0):
                rr = reroll_hand()
            ok = score_hand(h)
            if (ok == False):
                print("Breaking")
                break
    if (lower >= 63):
        print(f"Your lower score was {lower} so you earned 35 extra points!")
        total += 35
    print(f"Your final score is {total} with all hands played.")
    
#main
play_game()
            
                





