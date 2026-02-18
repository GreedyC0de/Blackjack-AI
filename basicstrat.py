from blackjack import Game
from graph import plot

g = Game()

         # 2,  3,  4,  5,  6,  7,  8,  9, 10,  A
chart = [['h','h','s','s','s','h','h','h','h','h'], #12
         ['s','s','s','s','s','h','h','h','h','h']] #13,14,15,16

results = ['Wins','Losses','Pushes']
vals = [0,0,0]

for i in range(1000):
    g.setup()
    result,hand,dealer = False,g.hand_tot,g.dealer_tot
    action = None
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

        result,hand,dealer = g.play_game(action)

    if result == 'l':
        vals[1] += 1
    elif result == 'w':
        vals[0] += 1
    else:
        vals[2] += 1
    print(f'Game: {i+1}')

print(vals)
plot(results,vals)