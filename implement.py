
# Interactive Nash Equilibrium Analyzer
# Stage 2 - Terminal Based Implementation

print("=" * 55)
print("       NASH EQUILIBRIUM ANALYZER")
print("=" * 55)

# Get player names
player_a = input("\nEnter Player A name: ").strip() or "Player A"
player_b = input("Enter Player B name: ").strip() or "Player B"

# Get strategies
print("\n--- Enter Strategies ---")

a_strategies = [
    input(f"{player_a}, enter Strategy 1: ").strip() or "A1",
    input(f"{player_a}, enter Strategy 2: ").strip() or "A2"
]

b_strategies = [
    input(f"{player_b}, enter Strategy 1: ").strip() or "B1",
    input(f"{player_b}, enter Strategy 2: ").strip() or "B2"
]

# Input payoff matrix
# Each cell contains (Player A payoff, Player B payoff)

payoffs = []

print("\n--- Enter Payoff Matrix ---")
print("Enter integer payoffs for each strategy combination.")
print("Format: Player A payoff, Player B payoff")

for i in range(2):
    row = []

    for j in range(2):
        print(
            f"\n{a_strategies[i]} vs {b_strategies[j]}"
        )

        while True:
            try:
                a_payoff = int(
                    input(f"{player_a}'s payoff: ")
                )
                b_payoff = int(
                    input(f"{player_b}'s payoff: ")
                )

                row.append((a_payoff, b_payoff))
                break

            except ValueError:
                print("Invalid input. Please enter integer values.")

    payoffs.append(row)


# Display payoff matrix
print("\n" + "=" * 55)
print("PAYOFF MATRIX")
print("=" * 55)

print(f"{'Strategy':<18}{b_strategies[0]:>15}{b_strategies[1]:>15}")

for i in range(2):
    print(
        f"{a_strategies[i]:<18}"
        f"{str(payoffs[i][0]):>15}"
        f"{str(payoffs[i][1]):>15}"
    )


# --------------------------------------------------
# BEST RESPONSE ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 55)
print("BEST RESPONSE ANALYSIS")
print("=" * 55)

# Player A's best response for each strategy of B
best_a = {}

for j in range(2):
    highest = max(payoffs[i][j][0] for i in range(2))

    best_a[j] = [
        i for i in range(2)
        if payoffs[i][j][0] == highest
    ]

    names = [a_strategies[i] for i in best_a[j]]

    print(
        f"When {player_b} chooses {b_strategies[j]}, "
        f"{player_a}'s best response: {', '.join(names)}"
    )


# Player B's best response for each strategy of A
best_b = {}

for i in range(2):
    highest = max(payoffs[i][j][1] for j in range(2))

    best_b[i] = [
        j for j in range(2)
        if payoffs[i][j][1] == highest
    ]

    names = [b_strategies[j] for j in best_b[i]]

    print(
        f"When {player_a} chooses {a_strategies[i]}, "
        f"{player_b}'s best response: {', '.join(names)}"
    )


# --------------------------------------------------
# DOMINANT STRATEGY ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 55)
print("DOMINANT STRATEGY ANALYSIS")
print("=" * 55)


def find_dominant_strategy(player):
    dominant = []

    for strategy in range(2):
        other = 1 - strategy

        if player == "A":
            differences = [
                payoffs[strategy][j][0] - payoffs[other][j][0]
                for j in range(2)
            ]
        else:
            differences = [
                payoffs[i][strategy][1] - payoffs[i][other][1]
                for i in range(2)
            ]

        # Weak dominance: never worse and sometimes better
        if all(d >= 0 for d in differences) and any(
            d > 0 for d in differences
        ):
            dominant.append(strategy)

    return dominant


dominant_a = find_dominant_strategy("A")
dominant_b = find_dominant_strategy("B")

if dominant_a:
    print(
        f"{player_a}: Weakly dominant strategy - "
        + ", ".join(a_strategies[i] for i in dominant_a)
    )
else:
    print(f"{player_a}: No weakly dominant strategy.")

if dominant_b:
    print(
        f"{player_b}: Weakly dominant strategy - "
        + ", ".join(b_strategies[j] for j in dominant_b)
    )
else:
    print(f"{player_b}: No weakly dominant strategy.")


# --------------------------------------------------
# NASH EQUILIBRIUM DETECTION
# --------------------------------------------------

print("\n" + "=" * 55)
print("NASH EQUILIBRIUM ANALYSIS")
print("=" * 55)

equilibria = []

for i in range(2):
    for j in range(2):

        # Both players must be playing best responses
        if i in best_a[j] and j in best_b[i]:
            equilibria.append((i, j))

if equilibria:
    print("Pure Nash Equilibrium found:")

    for i, j in equilibria:
        print(
            f"\nStrategies: ({a_strategies[i]}, {b_strategies[j]})"
        )

        print(
            f"Payoffs: ({payoffs[i][j][0]}, "
            f"{payoffs[i][j][1]})"
        )

        print(
            "Neither player can improve their payoff "
            "by changing strategy alone."
        )
else:
    print("No pure Nash Equilibrium found.")
    print("A mixed-strategy equilibrium may exist.")


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n" + "=" * 55)
print("ANALYSIS SUMMARY")
print("=" * 55)

print(f"Players: {player_a} and {player_b}")
print("Game type: Two-player, 2x2 strategic game")
print(f"Number of pure Nash Equilibria: {len(equilibria)}")

print("\nStage 2 implementation completed!")
