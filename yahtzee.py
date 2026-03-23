# from microbit import *
dice = [0,0,0,0,0]
lower = 0
scores = ["quit","ones","twos","threes","fours","fives","sixes", "3 of a kind", "sm straight", "lg straight", "full house", "4 of a kind", "yahtzee", "chance"]
scored = [0]
total = 0;
die = -1;
roll_over = False

# Create an array (list) containing the 6 die faces
die_faces = [
    images.create_image("""
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        """),
    images.create_image("""
        . . . . .
        . . . . .
        . . # . .
        . . . . .
        . . . . .
        """),
    images.create_image("""
        # . . . .
        . . . . .
        . . . . .
        . . . . .
        . . . . #
        """),
    images.create_image("""
        # . . . .
        . . . . .
        . . # . .
        . . . . .
        . . . . #
        """),
    images.create_image("""
        # . . . #
        . . . . .
        . . . . .
        . . . . .
        # . . . #
        """),
    images.create_image("""
        # . . . #
        . . . . .
        . . # . .
        . . . . .
        # . . . #
        """),
    images.create_image("""
        # . . . #
        . . . . .
        # . . . #
        . . . . .
        # . . . #
        """)
]
# Trigger the roll when the Micro:bit is shaken
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def on_gesture_shake():
    global die
    die = die + 1
    if roll_over == False:
        roll = randint(1, 6)
        die_faces[roll].show_image(0)
        roll_hand(die, roll)

def roll_hand(die,roll):
    global dice, die, roll_over
    dice[die] = roll
    if die == 5:
        roll_over = True
        msg = "H:"
        for d in range(5):
            msg += dice[d]
        basic.show_string(msg)
        reroll_hand()


# Rolls 5 die into array dice
# def roll_hand_old():
#     msg = "H:"
#     for d in range(5):
#         die = randint(1, 6)
#         dice[d] = die
#         msg += die
#     basic.show_string(msg)



# Scroll Micro is needed because one cannot capture current displayed character,
# so we need to break strings up into lists. First below is the microbits version.
def scroll_micro(msg):
    pressed = False;
    slist = []
    msgl = 0
    for char in msg:
        slist.append(char)
        msgl += 1
    c = 0
    while (c < msgl and pressed is False):
        basic.show_string(slist[c])
        if input.button_is_pressed(Button.A):
            pressed = True
            basic.clear_screen()
            basic.show_string(slist[c])
            return int(slist[c])
            basic.pause(10)
        basic.pause(100) # pause to prevent the loop from running too fast
        c+= 1
    return 1

# Rerolls up to specified 5 die in array dice
def reroll_hand():
    reroll = int(scroll_micro("RR? 0.1.2.3.4.5...0.1.2.3.4.5"))
    if (reroll == 5):
        for d in range(reroll):
            die = randint(1, 6)
            dice[d] = die
            msg = ", ".join(str(x) for x in dice)
            basic.show_string(msg)
    elif (reroll == 0):
        basic.show_string("No rerolls")
    else:
        for d in range(reroll):
            which = int(scroll_micro("RW? 1.2.3.4.5.6..1.2.3.4.5.6"))
            die = randint(1, 6)
            dice[which] = die
        msg = ", ".join(str(x) for x in dice)
        basic.show_string(msg)

# Gets category to score hand by
def get_score():
    categories = "Score categories are: \n"
    for s in range(1,len(scores),1):
        categories += str(s)+":"+scores[s]
        if (s < len(scores)-1):
            categories += ", "
        else:
            categories += ".\n Score in which category? "
    category = int(scroll_micro(categories))
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
        if (scored[c] == category):
            msg = "You already scored that."
            basic.show_string(msg)
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
        if toScore > 0 and toScore < 7:
            score = addUp(toScore)
            lower+= score
        elif toScore == 7:
            if (check_dupe(3)):
                score = addAll()
        elif toScore == 8:
            if (sm_straight()):
                score = 30
        elif toScore == 9:
            if (lg_straight()):
                score = 40
        elif toScore == 10:
            if (check_full()):
                score = 25
        elif toScore == 11:
            if (check_dupe(4)):
                score = addAll()
        elif toScore == 12:
            if (check_yahtzee()):
                score = 50
        elif toScore == 13:
            score = addAll()
        else:
            score = -1
        if (score == -1):
            msg="Invalid entry. You should have entered an integer 1-13."
            basic.show_string(msg)
            score_hand(h)
            return False
        else:
            scored.append(toScore) # add current to scored categories
            if (toScore != 12 and check_yahtzee()):
                msg="You got a Yahtzee bonus! 100 points added!"
                basic.show_string(msg)
                total += 100
            msg = "You scored " + str(score) + " for " + str(scores[toScore])
            basic.show_string(msg)
            total += score
            if (h < 13):
                msg= "Your total is "+ str(total) + " with "+ str(h) + " of 13 hands played"
                basic.show_string(msg)
            return True

def play_game():
    global total
    for h in range(len(scores)):
        if (h>0):
            roll_hand(0,0)
            rr = reroll_hand()
            if (rr > 0):
                rr = reroll_hand()
            ok = score_hand(h)
            if (ok == False):
                basic.show_string("Breaking")
                break
    if (lower >= 63):
        msg="Your lower score was "+ str(lower) + "so you earned 35 extra points!"
        basic.show_string(msg)
        total += 35
    msg="Your final score is " + str(total) + " with all hands played."
    basic.show_string(msg)
    
#main
if input.button_is_pressed(Button.B):
    play_game()
