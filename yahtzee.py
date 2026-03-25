# LOGIC: B changes mode (initial B starts)
# LOGIC: A selects displayed character
# LOGIC: Shake rolls dice

# NOTE: Extra reroll granted

dice = [0,0,0,0,0]
scores = ["-","1","2","3","4","5","6","3K","SS","LS","FH","4K","YZ","CH"]
scored = [0]
total = 0;
lower = 0
reroll = 0
die = -1;
rerolls = 2
roll_over = True
hands = 13
hand = 0

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
        """),
    images.create_image("""
        . . . . .
        . . . . #
        . . . # . 
        # . # . . 
        . # . . .
        """),
    images.create_image("""
        . . . . #
        . . . # .
        # . # . .
        . # . . .
        . . . . .
        """),
    images.create_image("""
        # . . . #
        . # . # .
        . . # . .
        . # . # .
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

# Add roll to hand until 5 are rolled
def roll_hand(die,roll):
    global dice,die,roll_over,rerolls,hands
    dice[die] = roll
    if die == 5:
        roll_over = True
        show_hand()

def show_hand():
    global dice, rerolls
    msg = "H:"
    for d in range(1,6):
        msg += dice[d]
    msg += "R:" + rerolls
    if rerolls > 0:
        # Reroll hand with B button if there are rerolls
        input.on_button_pressed(Button.B,reroll_hand)
    elif rerolls <= 0:
        # Score hand if there are no rerolls left
        input.on_button_pressed(Button.B,score_hand)
    basic.show_string(msg)

# Scroll Micro is needed because one cannot capture current displayed character,
# so we need to break strings up into lists. First below is the microbits version.
def scroll_micro(msg):
    pressed = False;
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
    pressed = False;
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

# Rerolls up to specified 5 die in array dice
def reroll_hand():
    global roll_over,reroll,rerolls
    reroll = int(scroll_micro("RR? 012345 012345"))
    if (reroll == 5 and rerolls > 0):
        roll_over = False
        rerolls = rerolls - 1 
        basic.show_string("R5!")
    elif (reroll == 0):
        roll_over = True
        basic.show_string("B!")
        input.on_button_pressed(Button.B,score_hand)
    else:
        for d in range(reroll):
            which = int(scroll_micro("RW? 12345 12345"))
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
    hexvals = "W? 123456789ABCD 123456789ABCD"
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
    msg = scorecat + " OK? YN YN"
    ok = scroll_micro_str(str(msg))
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
    global dice
    score = 0
    for d in range(5):
        if (dice[d] == value):
            score += value
    if score > 0:
        die_faces[8].show_image(0)
    else: 
        die_faces[9].show_image(0)
    return score

def addAll():
    global dice
    score = 0
    for d in range(5):
        score += dice[d]
    if score > 0:
        die_faces[8].show_image(0)
    else:
        die_faces[9].show_image(0)
    return score

def in_scored(category):
    global dice
    for c in range (len(scored)):
        if (scored[c] == category):
            msg = "2X!"
            basic.show_string(msg)
            die_faces[8].show_image(0)
            return True
    die_faces[9].show_image(0)
    return False

def check_yahtzee():
    global dice
    match = dice[4]
    for d in range(4):
        if (dice[d] != match):
            die_faces[9].show_image(0)
            return False
    die_faces[8].show_image(0)
    return True

def check_dupe(count):
    global dice
    counts = [0,0,0,0,0,0,0]
    toCount = -1
    for d in range(5):
        toCount = dice[d]
        counts[toCount] += 1
        if (counts[toCount] == count):
            die_faces[8].show_image(0)
            return True
    die_faces[9].show_image(0)
    return False

def check_full():
    global dice
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
        die_faces[8].show_image(0)
        return True
    else:
        die_faces[9].show_image(0)
        return False

def sort_dice():
    global dice
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
    global dice
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
        die_faces[9].show_image(0)
        return False
    else:
        die_faces[8].show_image(0)
        return True
    
def lg_straight():
    return count_neighbors(5)

def sm_straight():
    return count_neighbors(4)
        
def score_hand():
    global dice, total, lower, hands, hand, rerolls
    rerolls = 2
    hand = hand+1
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
                msg="YZ!+100!!"
                basic.show_string(msg)
                total += 100
            msg = "P: " + str(score)+ "  "
            basic.show_string(msg)
            msg = "    C:" + str(scores[toScore])
            total += score
            msg= "TS: "+ str(total)+ "  " 
            basic.show_string(msg)
            msg = "H: "+ str(hand)
            if hand == 13:
                if (lower >= 63):
                        msg="YLS= "+ str(lower) + "so +35!   "
                        basic.show_string(msg)
                        total += 35
                msg="FS: " + str(total)
                basic.show_string(msg)
                input.on_button_pressed(Button.B,end_game)
                return False
            return True
def end_game():
    global total
    basic.show_string("Total: "+total+ "... Game Over!")
    input.on_button_pressed(Button.B,play_game)

    return True

def play_game():
    music.play(music.tone_playable(Note.C, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)
    global total, die, dice, roll_over
    die = 0
    dice = [0,0,0,0,0]
    roll_over = False
    basic.show_string("SH!")
