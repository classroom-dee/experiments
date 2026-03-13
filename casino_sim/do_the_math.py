import random

N_CUSTOMERS = 1_000
EDGE_RATE = 0.05  # THIS MAKES A HUGE DIFF AND DRIFT
BET_UNIT_FIXED = 1.0
PER_CUSTOMER_WALLET = 1_000
CASINO_RESERVE = 1_000_000

casino_reserve_active = CASINO_RESERVE
total_customer_won_cnt = 0
games_cnt = 0
broken_customers = 0
for _ in range(N_CUSTOMERS):
    curr_customer_budget = PER_CUSTOMER_WALLET
    while curr_customer_budget > 0 and casino_reserve_active > 0:
        roll = random.choice([True, False])

        casino_reserve_active += (
            -BET_UNIT_FIXED if roll else BET_UNIT_FIXED * (1 + EDGE_RATE)
        )
        curr_customer_budget += (
            BET_UNIT_FIXED if roll else -BET_UNIT_FIXED * (1 + EDGE_RATE)
        )
        total_customer_won_cnt += 1 if roll else 0
        games_cnt += 1
    if casino_reserve_active <= 0:
        print("Casino is broke! LOL That never happens!")
        break  # can't go to a broke casino, now can we?
    broken_customers += 1

print('---"Fiscal session" statistics---')
print(f"total times rolled: {games_cnt}")
print(f"customer won count: {total_customer_won_cnt} out of {games_cnt} rolls")
print(f"customer win rate: {total_customer_won_cnt / games_cnt * 100}%")
print(f"customers went broke: {broken_customers}")
print(f"casino reserve: ${casino_reserve_active}")
print(f"casino earning: ${casino_reserve_active - CASINO_RESERVE}")
