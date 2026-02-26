
import random

# OOP Classes
class Player:
    def __init__(self, name):
        self.name = name
        self.dice = [0, 0, 0, 0, 0]
        self.lower = 0
        self.scored = []
        self.total = 0

class YahtzeeGame:
    scores = ["quit","ones","twos","threes","fours","fives","sixes", "3 of a kind", "sm straight", "lg straight", "full house", "4 of a kind", "yahtzee", "chance"]

    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.current_player_idx = 0

    def play(self):
        # Placeholder for main game loop
        pass

    def switch_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def get_current_player(self):
        return self.players[self.current_player_idx]


def roll_hand(player):
    for d in range(5):
        die = random.randint(1,6)
        player.dice[d] = die
    print(*player.dice, sep=", ")


def safe_input(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            break
        except ValueError:
            print("Invalid input! Please enter a whole number. Try again.")
    return value


def reroll_hand(player):
    reroll = safe_input("Reroll how many 0-5? ")
    if (reroll > 0 and reroll < 6):
        for d in range(reroll):
            if (reroll != 5):
                d = safe_input(f"Reroll which {d+1} of {reroll} (1-5)? ")
            die = random.randint(1,6)
            player.dice[d-1] = die
        print(*player.dice, sep=", ")
    elif (reroll > 5):
        print("You had another reroll! We'll assume you meant 0.")
    return reroll


def get_score(player, scores):
    categories = "Score categories are: \n"
    for s in range(1, len(scores), 1):
        categories += str(s) + ":" + scores[s]
        if (s < len(scores) - 1):
            categories += ", "
        else:
            categories += ".\n Score in which category? "
    category = int(input(categories))
    if (category == 0):
        return -2
    elif (in_scored(player, category)):
        return -1
    else:
        return category
        

def addUp(player, value):
    score = 0
    for d in range(5):
        if (player.dice[d] == value):
            score += value
    return score


def addAll(player):
    score = 0
    for d in range(5):
        score += player.dice[d]
    return score


def in_scored(player, category):
    for c in range(len(player.scored)):
        if (player.scored[c] == category):
            print("You already scored that.")
            return True
    return False


def check_yahtzee(player):
    match = player.dice[4]
    for d in range(4):
        if (player.dice[d] != match):
            return False
    return True


def check_dupe(player, count):
    counts = [0,0,0,0,0,0,0]
    toCount = -1
    for d in range(5):
        toCount = player.dice[d]
        counts[toCount] += 1
        if (counts[toCount] == count):
            return True
    return False


def check_full(player):
    counts = [0,0,0,0,0,0,0]
    toCount = -1
    house = 0
    for d in range(5):
        toCount = player.dice[d]
        counts[toCount] += 1
    for d in range(7):
        if (counts[d] == 3):
            house += 2
        elif (counts[d] == 2):
            house += 1
    if (house == 3):
        return True
    else:
        return False


def sort_dice(player):
    for i in range(4):
        minIndex = i
        for j in range(i+1, 5, 1):
            if (player.dice[j] < player.dice[minIndex]):
                minIndex = j
        swap = player.dice[i]
        player.dice[i] = player.dice[minIndex]
        player.dice[minIndex] = swap
        

def count_neighbors(player, needed):
    sort_dice(player)
    jumps = 0
    for i in range(4):
        gap = player.dice[i+1] - player.dice[i]
        if (gap != 1):
            jumps += 1
            if (i == 1 or i == 2):
                jumps = 5
    gap = 5 - needed
    if (jumps > gap):
        return False
    else:
        return True

def lg_straight(player):
    return count_neighbors(player, 5)

def sm_straight(player):
    return count_neighbors(player, 4)

def score_hand(player, h, scores):
    score = 0
    toScore = get_score(player, scores)
    if (toScore == -1):
        toScore = get_score(player, scores)
    if (toScore == -2):
        return False
    else:
        match toScore:
            case 1 | 2 | 3 | 4 | 5 | 6:
                score = addUp(player, toScore)
                player.lower += score
            case 7: # 3 of a kind
                if (check_dupe(player, 3)):
                    score = addAll(player)
            case 8: # sm straight
                if (sm_straight(player)):
                    score = 30
            case 9:  # lg straight
                if (lg_straight(player)):
                    score = 40
            case 10: # full house
                if (check_full(player)):
                    score = 25
            case 11:  # 4 of a kind
                if (check_dupe(player, 4)):
                    score = addAll(player)
            case 12:  # yahtzee
                if (check_yahtzee(player)):
                    score = 50
            case 13:  # chance
                score = addAll(player)
            case _:
                score = -1
        if (score == -1):
            print("Invalid entry. You should have entered an integer 1-13.")
            score_hand(player, h, scores)
        else:
            player.scored.append(toScore)
            if (toScore != 12 and check_yahtzee(player)):
                print("You got a Yahtzee bonus! 100 points added!")
                player.total += 100
            print(f"You scored {score} for {scores[toScore]}")
            player.total += score
            if (h < 13):
                print(f"Your total is {player.total} with {h} of 13 hands played.")
            return True
    

def main():
    print("Welcome to 2-player OOP Yahtzee!\nThere is no scoresheet yet.")
    player_names = []
    for i in range(2):
        name = input(f"Enter name for Player {i+1}: ")
        player_names.append(name)
    game = YahtzeeGame(player_names)
    print("Here is your first of 13 hands.")
    input("Ready?")
    for h in range(1, 14):
        for player in game.players:
            print(f"\n{player.name}'s turn (Hand {h} of 13)")
            roll_hand(player)
            rr = reroll_hand(player)
            if rr > 0:
                rr = reroll_hand(player)
            ok = score_hand(player, h, game.scores)
            if ok == False:
                print("Breaking")
                return
    for player in game.players:
        if player.lower >= 63:
            print(f"{player.name}'s lower score was {player.lower} so you earned 35 extra points!")
            player.total += 35
        print(f"{player.name}'s final score is {player.total} with all hands played.")

if __name__ == "__main__":
    main()
