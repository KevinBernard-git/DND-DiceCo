import asyncio
from math import floor
from random import randrange

total = 0
gain = 0
lose = 0
stale = 0
ad_gold = 30
turn_count = 0
hardcore = False
game_active = True


def rolld6():
    d6 = randrange(1, 6)
    d6_bonus = d6 * 5
    print("D6 Bonus Roll: " + str(d6))
    return d6_bonus


def rolld8():
    d8_1 = randrange(1, 8)
    d8_2 = randrange(1, 8)
    d8_bonus = (d8_1 + d8_2) * 5
    print("2 D8 Bonus Roll: " + str(d8_1) + ", " + str(d8_2))
    return d8_bonus


def rolld10():
    d10_1 = randrange(1, 10)
    d10_2 = randrange(1, 10)
    d10_3 = randrange(1, 10)
    d10_bonus = (d10_1 + d10_2 + d10_3) * 5
    print("3 D10 Bonus Roll: " + str(d10_1) + ", " + str(d10_2) + ", " + str(d10_3))
    return d10_bonus


async def rollthedice(ads_gold):
    tg = 0
    roll = randrange(11, 110)
    print("=====Turn " + str(turn_count) + "=====")
    print("You Rolled a " + str(roll))
    if ads_gold > 0:
        print(str(ads_gold) + " spent on ads!")
        print("Total roll : " + str(roll + ads_gold))
    match roll:
        case r if 1 <= r < 21:
            tg += -90
        case r if 21 <= r < 31:
            tg += -60
        case r if 31 <= r < 41:
            tg += -30
        case r if 41 <= r < 61:
            tg += 0
        case r if 61 <= r < 81:
            tg += rolld6()
        case r if 81 <= r < 91:
            tg += rolld8()
        case r if 91 <= r < 110:
            tg += rolld10()
        case _:
            print(total)
    print("Gold this turn: " + str(tg))
    await set_stats(tg)
    return tg


def show_stats():
    win_prct = (float(gain) / float(turn_count))
    lose_prct = (float(lose) / float(turn_count))
    stale_prct = (float(stale) / float(turn_count))
    print("\n=====STATS=====")
    print("After " + str(turn_count) + " turns, you GAINED " + str(gain) + " times and " + "LOST " + str(
        lose) + " times")
    print(str(stale) + " turns were STALEMATE")
    print("Win Percentage: " + floored_percentage(win_prct, 2))
    print("Lose Percentage: " + floored_percentage(lose_prct, 2))
    print("Stalemate Percentage: " + floored_percentage(stale_prct, 2))


def floored_percentage(val, digits):
    val *= 10 ** (digits + 2)
    return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)


async def set_stats(gold):
    global lose, gain, stale
    if gold < 0:
        lose += 1
    elif gold > 0:
        gain += 1
    else:
        stale += 1
    return None


def set_settings():
    global ad_gold, total, gain, lose, stale, hardcore
    print("=====SETTINGS=====")
    ad_gold = int(input("Enter Starting Advertising Gold\n"))
    total = int(input("Enter Starting Gold\n"))
    reply = str(input("Hardcore Mode? "+' (y/n): \n')).lower().strip()
    if reply == 'y':
        hardcore = True
    else:
        hardcore = False


def reset():
    global total, ad_gold, turn_count, gain, lose, stale, hardcore
    print("Game Reset!\n")
    total = 0
    ad_gold = 30
    turn_count = 0
    gain = 0
    lose = 0
    stale = 0
    hardcore = False


async def game_engine():
    global game_active, turn_count, ad_gold, total, gain, lose, stale
    while game_active:
        gold_this_turn = 0
        cmd = input("What would you like to do... \n")
        match cmd:
            case "play" | "p" | "":
                turn_count += 1
                gold_this_turn += await rollthedice(0)
            case num if num.isdigit():
                for i in range(int(cmd)):
                    turn_count += 1
                    total += await rollthedice(0)
                    print("Total Gold: " + str(total) + "\n")
                show_stats()
            case "advertise" | "ad" | "a":
                while True:
                    try:
                        ad_pur = int(input("How much would you like to spend on Ads?\n"))
                        if ad_pur <= ad_gold:
                            ad_gold -= ad_pur
                            turn_count += 1
                            gold_this_turn += await rollthedice(ad_pur)
                        else:
                            print("Not enough ad gold!\nAd Gold: " + str(ad_gold))
                        break
                    except ValueError:
                        print("That's not a number...\n")
            case "reset" | "new" | "r":
                reset()
            case "settings" | "set":
                set_settings()
            case "stats" | "s":
                show_stats()
            case "help" | "h":
                print("\n\n=====List of Commands=====")
                print("Play one round\n  'play' or 'p' or enter")
                print("Play a round with advertising\n  'advertise' or 'ad' or 'a'")
                print("Show Stats for current game\n   'stats' or 's'")
                print("Settings | Set ad gold, starting gold, hardcore mode!?\n   'settings' or 'set'")
                print("Reset game\n   'reset' or 'new' or 'r'")
                print("Help Menu\n   'help' or 'h'")
                print("Quit game\n   'quit or 'q'\n")
            case "quit" | "q":
                print("Cya!")
                game_active = False
                break
        total += gold_this_turn
        print("Total Gold: " + str(total) + "\n")
        if hardcore and total <= 0:
            print("You have been FIRED!!! \n")
            reset()

print("\n\nWelcome to Dice Co.")
print("As a new unpaid intern you'll probably want some training...\n")
print("Just type what you would like to do.")
print("Type 'play' to roll the dice once or type any number to roll that many times.")
print("You can also type 'help' for a list of commands.")
print("Good Luck!\n\n")

asyncio.run(game_engine())
