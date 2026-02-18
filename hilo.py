from blackjack import Game
from graph import plot,graph_money

g = Game()

         # 2,  3,  4,  5,  6,  7,  8,  9, 10,  A
chart = [['h','h','s','s','s','h','h','h','h','h'], #12
         ['s','s','s','s','s','h','h','h','h','h']] #13,14,15,16

results = ['Wins','Losses','Pushes']
vals = [0,0,0]
profit = 0
count = 0
money_over_time = []

for i in range(1000):
    g.setup()
    result,hand,dealer = False,g.hand_tot,g.dealer_tot
    action = None
    #calc count:
    count = 0
    for card in g.deck:
        val = g.deck[card][1]
        if val == 10 or val == 0:
            count -= 1
        elif val > 1 and val < 7:
            count += 1
    
    if count <= 0:
        bet = 10
    elif count == 1:
        bet = 20
    elif count == 2:
        bet = 40
    elif count == 3:
        bet = 60
    elif bet >= 4:
        bet = 100
    profit -= bet
    
    while result == False:
        try:
            if hand == 12:
                action = chart[0][dealer-2]
            elif 12 < hand < 17:
                action = chart[1][dealer-2]
            elif hand >= 17:
                action = 's'
            else:
                action = 'h'
        except Exception as error:
            pass

        result,hand,dealer,payout = g.play_game(action,bet=bet)

    if result == 'l':
        vals[1] += 1
    elif result == 'w':
        vals[0] += 1
    else:
        vals[2] += 1

    profit += payout
    money_over_time.append(profit)
    #print(f'PAYOUT: {payout}; WIN/LOSE: {result}')
    #print(f'BET: {bet}; COUNT: {count}; PROFIT: {profit}')
    print(f'Game: {i+1}')
print(vals)
plot(results,vals)
print(profit)
graph_money(money_over_time)
print(money_over_time)