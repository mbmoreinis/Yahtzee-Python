# LOGIC: B changes mode (initial B starts)
# LOGIC: A selects displayed character
# LOGIC: Shake rolls dice

dice = [0,0,0,0,0]
lower = 0
reroll = 0
scores = ["0","1","2","3","4","5","6","3K","SS=","LS","FH","4K","YZ","CH"]
scored = [0]
total = 0
die = -1
rerolls = 2
roll_over = True
hands = 13

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
input.on_gesture(Gesture.SHAKE, try_roll)

# First B: Trigger start of game, enable rolls
input.on_button_pressed(Button.B,play_game)

# Attempt to roll a die (roll_over = False)
def try_roll():
    global die, roll_over
    die = die + 1
    if roll_over == False:
        roll = randint(1, 6)
        die_faces[roll].show_image(0)
        roll_hand(die, roll)
    else:
        basic.show_string("A|B")

# Add roll to hand until 5 are rolled
def roll_hand(die,roll):
    global dice, die, roll_over, rerolls, hands
    dice[die] = roll
    if die == 5:
        roll_over = True
        show_hand()
        if rerolls > 0:
            # Reroll hand with B button if there are rerolls
            input.on_button_pressed(Button.B,reroll_hand)
        elif rerolls <= 0:
            # Score hand if there are no rerolls left
            input.on_button_pressed(Button.B,score_hand)

def show_hand():
    msg = "H:"
    for d in range(1,6):
        msg += dice[d]
    basic.show_string(msg)

# Scroll Micro is needed because one cannot capture current displayed character,
# so we need to break strings up into lists. First below is the microbits version.
def scroll_micro(msg):
    pressed = False
    slist = [] #string list from msg
    msgl = 0 # message length
    for char in msg:
        slist.append(char)
        msgl += 1
    c = 0 # current character in string list
    while (c < msgl and pressed is False):
        basic.show_string(slist[c])
        if input.button_is_pressed(Button.A):
            music.play(music.tone_playable(Note.C, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)
            pressed = True
            basic.clear_screen()
            basic.show_string(slist[c])
            return int(slist[c])
            basic.pause(10)
        basic.pause(100) # pause to prevent the loop from running too fast
        c+= 1
    return 1


# Scroll Micro String is needed because one cannot capture current displayed character,
# so we need to break strings up into lists. First below is the microbits version.
def scroll_micro_str(msg):
    pressed = False
    slist = [] #string list from msg
    msgl = 0 # message length
    for char in msg:
        slist.append(char)
        msgl += 1
    c = 0 # current character in string list
    while (c < msgl and pressed is False):
        basic.show_string(slist[c])
        if input.button_is_pressed(Button.A):
            music.play(music.tone_playable(Note.C, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)
            pressed = True
            basic.clear_screen()
            basic.show_string(slist[c])
            return str(slist[c])
            basic.pause(10)
        basic.pause(100) # pause to prevent the loop from running too fast
        c+= 1
    return "*"

# Scroll Micro String is needed because one cannot capture current displayed character,
# so we need to break strings up into lists. First below is the microbits version.
def scroll_micro_list(slist):
    pressed = False
    msgl=0
    for cat in slist:
        msgl += 1
    c = 0 # current element in string list
    while (c < msgl and pressed is False):
        basic.show_string(slist[c])
        if input.button_is_pressed(Button.A):
            music.play(music.tone_playable(Note.C, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)
            pressed = True
            basic.clear_screen()
            basic.show_string(slist[c])
            return str(slist[c])
            basic.pause(10)
        basic.pause(100) # pause to prevent the loop from running too fast
        c+= 1
    return "*"


# Rerolls up to specified 5 die in array dice
def reroll_hand():
    global roll_over, reroll, rerolls
    reroll = int(scroll_micro("R?012345012345"))
    if (reroll == 5 and rerolls > 0):
        roll_over = False
        rerolls = rerolls - 1
        basic.show_string("R:")
    elif (reroll == 0 or roll_over == True):
        roll_over = True
        rerolls = 0
        basic.show_string("-")
        input.on_button_pressed(Button.B,score_hand)
    else:
        roll_over = False
        for d in range(reroll):
            which = int(scroll_micro("W?123456123456"))
            die = randint(1, 6)
            dice[which] = die
        rerolls = rerolls - 1
    show_hand()

# Gets category to score hand by
def get_score():
    categories = "C:"
    for s in range(1,len(scores),1):
        categories += scores[s]
    basic.show_string(categories)
    hexvals = "W?123456789ABCD"
    category = scroll_micro_str(hexvals)
    numcat = 0
    if category == "A":
        numcat = 10
    elif category == "B":
        numcat = 11
    elif category == "C":
        numcat =12
    elif category == "D":
        numcat = 13
    else:
        numcat = int(category)
    scorecat = str(scores[numcat])
    okcat = scorecat + "OK?YN"
    ok = scroll_micro_str(str(okcat))
    if ok == "Y":
        if (numcat == 0):
            return -2
        elif (in_scored(numcat)):
            return -1
        else:
            return numcat
    else:
        get_score()
        return numcat
        
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
            msg = "2X!"
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
    house = 0
    for d in range(5):
        toCount = dice[d]
        counts[toCount] += 1
    for d in range (7):
        if (counts[d] == 3):
            house +=2
        elif (counts[d] == 2):
            house +=1
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
        
def score_hand():
    global total, lower, hands, rerolls
    rerolls = 2
    h = hands
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
            msg="!1-13."
            basic.show_string(msg)
            score_hand()
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
            hands = hands - 1
            return True

def play_game():
    music.play(music.tone_playable(Note.C, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)
    global total, die, dice, roll_over
    die = 0
    dice = [0,0,0,0,0]
    roll_over = False
    basic.show_string("!")
    # for h in range(len(scores)):
            # rr = reroll_hand()
            # if (rr > 0):
            #     rr = reroll_hand()
            # ok = score_hand(h)
            # if (ok == False):
            #     basic.show_string("Breaking")
            #     break
    # if (lower >= 63):
    #     msg="Your lower score was "+ str(lower) + "so you earned 35 extra points!"
    #     basic.show_string(msg)
    #     total += 35
    # msg="Your final score is " + str(total) + " with all hands played."
    # basic.show_string(msg)
    
