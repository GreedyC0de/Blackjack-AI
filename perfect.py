from blackjack import Game
from functools import lru_cache
from collections import Counter
from graph import plot,graph_money
import sys

sys.setrecursionlimit(3000)

def deck_len(deck):
    len = sum(deck.values())
    return len

def simulate_card(total,card,soft_aces):
    if card == 0:
        total += 11
        soft_aces += 1
    else:
        total += card

    while total > 21 and soft_aces > 0:
        total -= 10
        soft_aces -= 1
    return total,soft_aces

@lru_cache(None)
def dealer_play(dealer_tot,player_tot,deck_count,dealer_soft):
    deck = Counter(dict(deck_count))

    if dealer_tot > 21: #return win if dealer busted
        return 1.0
    
    if dealer_tot >= 17: #return w/l by comparring totals
        if dealer_tot > player_tot:
            return -1.0
        elif dealer_tot < player_tot:
            return 1.0
        else:
            return 0.0
        
    ev = 0.0
    total_cards = deck_len(deck)

    if total_cards == 0:
        if dealer_tot > 21:
            return 1.0
        if dealer_tot < player_tot:
            return 1.0
        if dealer_tot > player_tot:
            return -1.0
        return 0

    for card,count in deck.items(): #iterate through values in deck and how many
        
        if count == 0: #skip if none
            continue

        p = count/total_cards #calc probablility of case occuring
        deck[card] -= 1 #simulate dealing of card

        new_total,soft_aces = simulate_card(dealer_tot,card,dealer_soft) #add card to total
        ev += p * dealer_play(new_total,player_tot,tuple(sorted(deck.items())),soft_aces) #calc w/l of branches of new state and add to ev

        deck[card] += 1 #add back the card for future recursions when backtracking

    return ev

@lru_cache(None)
def ev_stand(player_total,dealer_upcard,deck_count,dealer_soft):
    deck = Counter(dict(deck_count))
    ev = 0.0
    total_cards = deck_len(deck)

    for card,count in deck.items():
        if count == 0:
            continue

        p = count/total_cards
        deck[card] -= 1
        
        dealer_total,soft_aces = simulate_card(dealer_upcard,card,dealer_soft)
        ev += p * dealer_play(dealer_total,player_total,tuple(sorted(deck.items())),soft_aces)

        deck[card] += 1

    return ev

@lru_cache(None)
def ev_hit(player_tot,dealer_upcard,deck_count,player_soft,dealer_soft):
    if player_tot > 21:
        return -1.0
    
    deck = Counter(dict(deck_count))
    ev = 0.0
    total_cards = deck_len(deck)

    for card,count in deck.items():
        if count == 0:
            continue

        p = count/total_cards
        deck[card] -= 1

        new_tot,soft_aces = simulate_card(player_tot,card,player_soft)

        if new_tot > 21:
            ev += p * (-1.0)
        else:
            ev += p * max(
                        ev_hit(new_tot,dealer_upcard,tuple(sorted(deck.items())),soft_aces,dealer_soft),
                        ev_stand(new_tot,dealer_upcard,tuple(sorted(deck.items())),dealer_soft))
        
        deck[card] += 1
    
    return ev

def best_move(player_tot,dealer_upcard,deck,player_soft,dealer_soft):
    stand_ev = ev_stand(player_tot,dealer_upcard,tuple(sorted(deck.items())),dealer_soft)
    hit_ev = ev_hit(player_tot,dealer_upcard,tuple(sorted(deck.items())),player_soft,dealer_soft)

    return 'h' if hit_ev > stand_ev else 's',stand_ev,hit_ev

def card_val(card):
    if card == 0:
        return 11
    return card

def prebet_ev(deck):
    total_cards = sum(deck.values())
    ev = 0.0

    for c1 in deck:
        if deck[c1] == 0:
            continue
        p1 = deck[c1]
        deck[c1] -= 1

        for c2 in deck:
            if c2 > c1:
                continue
            mult = 2 if c1 != c2 else 1

            if deck[c2] == 0:
                continue
            p2 = deck[c2]
            deck[c2] -= 1

            if c1 == c2:
                p_player = (p1/total_cards) * ((p1-1)/(total_cards-1))
            else:
                p_player = (p1/total_cards) * (p2/(total_cards-1))

            for dealer_card in deck:
                if deck[dealer_card] == 0:
                    continue
                p3 = deck[dealer_card]
                deck[dealer_card] -= 1

                p_dealer = p3/(total_cards-2)

                player_soft = 0
                player_total = 0
                player_total,player_soft = simulate_card(player_total,c1,player_soft)
                player_total,player_soft = simulate_card(player_total,c2,player_soft)

                dealer_soft = 0
                dealer_total = 0
                dealer_total,dealer_soft = simulate_card(dealer_total,dealer_card,dealer_soft)

                deal_ev = optimal_ev(player_total,dealer_total,tuple(sorted(deck.items())),player_soft,dealer_soft)
                prob = mult * p_player * p_dealer
                ev += prob * deal_ev

                deck[dealer_card] += 1
            deck[c2] += 1
        deck[c1] += 1
    return ev

@lru_cache(None)
def optimal_ev(player_total,dealer_upc,deck_f,player_soft,dealer_soft):
    if player_total > 21:
        return -1.0
    
    s_ev = ev_stand(player_total,dealer_upc,deck_f,dealer_soft)
    h_ev = ev_hit(player_total,dealer_upc,deck_f,player_soft,dealer_soft)
    return max(s_ev,h_ev)

g = Game()

results = ['Wins','Losses','Pushes']
vals = [0,0,0]
profit = 1000
money_over_time = []

for i in range(250):
    bbb = Counter({2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 0:0})
    for card in g.deck:
        val = g.default_deck[card][1]
        bbb[val] += 1
    #'''
    ev = prebet_ev(bbb)    
    base_bet = 100
    max_bet = 1000
    bet = base_bet + (max_bet-base_bet) * ev / 0.1
    bet = int(round(max(base_bet,min(max_bet,bet))))
    #'''
    #bet=1
    g.setup(bet)

    player_tot = 0
    player_soft = 0

    for card in g.hand:
        val = g.default_deck[card][1]
        player_tot,player_soft = simulate_card(player_tot,val,player_soft)

    dealer_upcard = g.default_deck[g.dealer_hand[0]][1]
    dealer_soft = 1 if dealer_upcard == 0 else 0
    dealer_tot = 11 if dealer_upcard == 0 else dealer_upcard
    '''
    hilo = 0
    for card in g.deck:
        val = g.deck[card][1]
        if val == 10 or val == 0:
            hilo -= 1
        elif val > 1 and val < 7:
            hilo += 1
    
    if hilo <= 0:
        bet = 10
    elif hilo == 1:
        bet = 20
    elif hilo == 2:
        bet = 40
    elif hilo == 3:
        bet = 60
    elif hilo >= 4:
        bet = 100
    '''
    profit -= bet
    
    stood = False
    result = False
    while result == False:
        count = Counter({2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 0:0})
        
        for card in g.deck:
            val = g.default_deck[card][1]
            count[val] += 1
        
        if not stood:
            action,stand_ev,hit_ev = best_move(player_tot,dealer_upcard,count,player_soft,dealer_soft)
            if action == 's' and player_tot <= 11:
                action = 'h'
            if action == 's':
                stood = True
       
        result,player_tot,dealer_tot,payout = g.play_game(action,bet=bet,stand_ev=stand_ev,hit_ev=hit_ev)
        if action == 's':
            new_card = g.hand[-1]
            val = g.default_deck[new_card][1]
            player_tot,player_soft = simulate_card(player_tot,val,player_soft)

        player_soft = 0
        for card in g.hand:
            val = g.default_deck[card][1]
            if val == 0:
                player_soft += 1

    if result == 'l':
        vals[1] += 1
    elif result == 'w':
        vals[0] += 1
    else:
        vals[2] += 1
    profit += payout
    money_over_time.append(profit)
    print(f'Game: {i+1}')

print(results)
print(vals)
plot(results,vals)
print(profit)
graph_money(money_over_time,len(money_over_time))
print(money_over_time)