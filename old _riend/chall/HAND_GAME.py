import random

FLAG = "expX{7ru3_m4st3r_0f_h4nd_cr1ck3t}"
VALID_RUNS = [1, 2, 3, 4, 5, 6]

def toss():
    print("\nToss Time! Choose Head or Tail (H/T):")
    player_call = input("> ").strip().lower()
    toss_result = random.choice(['h', 't'])

    if player_call == toss_result:
        print("You won the toss!")
        choice = input("Choose to Bat or Bowl (bat/bowl): ").strip().lower()
        return 'player', choice
    else:
        print("Computer won the toss!")
        comp_choice = random.choice(['bat', 'bowl'])
        print("Computer chooses to", comp_choice)
        return 'computer', comp_choice

# Aggressive & unpredictable computer batting
def insane_computer_batting():
    # Skews towards high scoring (4s & 6s)
    return random.choices([1, 2, 3, 4, 5, 6], weights=[1, 1, 1, 3, 2, 4])[0]

# Very smart and hard-to-beat bowling (matches your habits)
def insane_computer_bowling(player_history):
    if len(player_history) < 3:
        return random.randint(1, 6)
    likely = max(set(player_history[-3:]), key=player_history[-3:].count)
    # 50% chance to bowl exactly what you're likely to choose
    return likely if random.random() < 0.5 else random.randint(1, 6)

def play_innings(batting_side, target=None, player_inputs=None):
    score = 0
    player_history = []

    while True:
        if batting_side == 'player':
            try:
                user_run = int(input("Your turn (1-6): "))
            except ValueError:
                print("Invalid input.")
                continue

            if user_run not in VALID_RUNS:
                print("Choose between 1 to 6.")
                continue

            if user_run in [2, 6]:
                print("You're OUT!")
                return score, False

            comp_bowl = insane_computer_bowling(player_history)
            print(f"Computer bowls: {comp_bowl}")
            player_history.append(user_run)
            player_inputs.append(user_run)

            if user_run == comp_bowl:
                print("You're OUT!")
                break
            else:
                score += user_run
                print("Score:", score)
        else:
            comp_run = insane_computer_batting()
            try:
                user_bowl = int(input("Your bowl (1-6): "))
            except ValueError:
                print("Invalid input.")
                continue

            if user_bowl not in VALID_RUNS:
                print("Choose between 1 to 6.")
                continue

            # 10% chance computer cheats and hits anyway
            if random.random() < 0.1:
                print("Computer plays: [CHEAT HIT] 🎯 6")
                comp_run = 6
            else:
                print(f"Computer plays: {comp_run}")

            if user_bowl == comp_run:
                print("Computer is OUT!")
                break
            else:
                score += comp_run
                print("Computer Score:", score)

        if target and score > target:
            break

    return score, True

def play_game():
    print("\n🏏 Welcome to Hand Cricket (INSANE MODE)")
    toss_winner, choice = toss()

    player_inputs = []

    if toss_winner == 'player':
        player_bats_first = choice == 'bat'
    else:
        player_bats_first = choice != 'bat'

    print(f"\n{'You' if player_bats_first else 'Computer'} will bat first!")

    first_batter = 'player' if player_bats_first else 'computer'
    target_side = 'computer' if player_bats_first else 'player'

    print(f"\n🔁 First Innings: {first_batter.capitalize()} batting")
    first_score, clean_batting = play_innings(first_batter, player_inputs=player_inputs)
    print(f"{first_batter.capitalize()} scored: {first_score}")
    print("\n--- Inning Break ---\n")

    print(f"🔁 Second Innings: {target_side.capitalize()} batting")
    second_score, _ = play_innings(target_side, target=first_score, player_inputs=player_inputs)
    print(f"{target_side.capitalize()} scored: {second_score}")
    print("\n🏁 Match Over!")

    if player_bats_first:
        if first_score > second_score:
            print("🎉 You somehow WON!")
            if clean_batting:
                print("🏆 You avoided using 2 or 6. Respect.")
                print("🎯 FLAG:", FLAG)
        else:
            print("💥 You lost. Try again!")
    else:
        if second_score > first_score:
            print("🎉 You somehow WON!")
            if clean_batting:
                print("🏆 You avoided using 2 or 6. Respect.")
                print("🎯 FLAG:", FLAG)
        else:
            print("💥 You lost. Try again!")

def main_loop():
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != 'y':
            print("\nThanks for surviving INSANE MODE! 🧠💀")
            break

if __name__ == "__main__":
    main_loop()
