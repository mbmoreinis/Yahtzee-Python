import random
dice = [0,0,0,0,0]
lower = 0
scores = ["quit","ones","twos","threes","fours","fives","sixes", "3 of a kind", "sm straight", "lg straight", "full house", "4 of a kind", "yahtzee", "chance"]
scored = []
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
    if (reroll > 0 and reroll < 6):
        for d in range(reroll):
            if (reroll != 5):
                d = int(input(f"Reroll which {d+1} of {reroll} (1-5)? "))
            die = random.randint(1,6)
            dice[d-1]=die
        print(*dice,sep=", ")
    elif (reroll > 5):
        print("You had another reroll! We'll assume you meant 0.")
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
    elif (in_scored(category)):
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

def check_yahtzee():
    match = dice[4]
    for d in range(4):
        if (dice[d] != match):
            return False
    return True

def check_dupe(count):
    counts = [0,0,0,0,0,0,0]
    toCount = -1
    for d in range(5):
        toCount = dice[d]
        counts[toCount] += 1
        if (counts[toCount] == count):
            return True
    return False

def check_full():
    counts = [0,0,0,0,0,0,0]
    toCount = -1
    house = 0;
    for d in range(5):
        toCount = dice[d]
        counts[toCount] += 1
    for d in range (7):
        if (counts[d] == 3):
            house +=2;
        elif (counts[d] == 2):
            house +=1;
    if (house == 3):
        return True
    else:
        return False

def sort_dice():
    n = 6
    swap = -1
    for i in range (4):
        minIndex = i
        for j in range (i+1,5,1):
            if (dice[j] < dice[minIndex]):
                minIndex = j
        swap = dice[i]
        dice[i]=dice[minIndex]
        dice[minIndex] = swap
        
def count_neighbors(needed):
    sort_dice()
    jumps = 0
    for i in range (4):
        gap = dice[i+1]-dice[i]
        if (gap != 1):
            jumps += 1
            if (i == 1 or i == 2):
                jumps = 5
    gap = 5-needed
    if (jumps > gap):
        return False
    else:
        return True
    
def lg_straight():
    return count_neighbors(5)

def sm_straight():
    return count_neighbors(4)
        
def score_hand(h):
    global total, lower
    score = 0
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
            case 7: # 3 of a kind
                if (check_dupe(3)):
                    score = addAll()
            case 8: # sm straight
                if (sm_straight()):
                    score = 30
            case 9:  # lg straight
                if (lg_straight()):
                    score = 40
            case 10: # full house
                if (check_full()):
                    score = 25
            case 11:  # 4 of a kind
                if (check_dupe(4)):
                    score = addAll()
            case 12:  # yahtzee
                if (check_yahtzee()):
                    score = 50
            case 13:  # chance
                score = addAll()
            case _: # bad entry
                score = -1
        if (score == -1):
            print("Invalid entry. You should have entered an integer 1-13.")
            score_hand(h)
        else:
            scored.append(toScore) # add current to scored categories
            if (toScore != 12 and check_yahtzee()): 
                print("You got a Yahtzee bonus! 100 points added!")
                total += 100
            print(f"You scored {score} for {scores[toScore]}")
            total += score
            if (h < 13):
                print(f"Your total is {total} with {h} of 13 hands played.")
            return True
    
def play_game():
    global total
    for h in range(len(scores)):
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
