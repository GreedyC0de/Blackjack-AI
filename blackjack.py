import pygame
import random
import time

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,120,0)
SPEED = 60

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920,1080))
        self.hand_pos = [50*2,335*2]
        self.dealer_hand_pos = [50*2,100*2]
        self.deck_pos = (825*2,35*2)
        self.clock = pygame.time.Clock()
        self.card_size = (100*2,140*2)
        self.default_deck = {
            '2_club': (pygame.image.load('cards/2_of_clubs.png'),2),
            '3_club': (pygame.image.load('cards/3_of_clubs.png'),3),
            '4_club': (pygame.image.load('cards/4_of_clubs.png'),4),
            '5_club': (pygame.image.load('cards/5_of_clubs.png'),5),
            '6_club': (pygame.image.load('cards/6_of_clubs.png'),6),
            '7_club': (pygame.image.load('cards/7_of_clubs.png'),7),
            '8_club': (pygame.image.load('cards/8_of_clubs.png'),8),
            '9_club': (pygame.image.load('cards/9_of_clubs.png'),9),
            '10_club': (pygame.image.load('cards/10_of_clubs.png'),10),
            'Jack_club': (pygame.image.load('cards/jack_of_clubs2.png'),10),
            'Queen_club': (pygame.image.load('cards/queen_of_clubs2.png'),10),
            'King_club': (pygame.image.load('cards/king_of_clubs2.png'),10),
            'Ace_club': (pygame.image.load('cards/ace_of_clubs.png'),0),

            '2_spade': (pygame.image.load('cards/2_of_spades.png'),2),
            '3_spade': (pygame.image.load('cards/3_of_spades.png'),3),
            '4_spade': (pygame.image.load('cards/4_of_spades.png'),4),
            '5_spade': (pygame.image.load('cards/5_of_spades.png'),5),
            '6_spade': (pygame.image.load('cards/6_of_spades.png'),6),
            '7_spade': (pygame.image.load('cards/7_of_spades.png'),7),
            '8_spade': (pygame.image.load('cards/8_of_spades.png'),8),
            '9_spade': (pygame.image.load('cards/9_of_spades.png'),9),
            '10_spade': (pygame.image.load('cards/10_of_spades.png'),10),
            'Jack_spade': (pygame.image.load('cards/jack_of_spades2.png'),10),
            'Queen_spade': (pygame.image.load('cards/queen_of_spades2.png'),10),
            'King_spade': (pygame.image.load('cards/king_of_spades2.png'),10),
            'Ace_spade': (pygame.image.load('cards/ace_of_spades2.png'),0),

            '2_heart': (pygame.image.load('cards/2_of_hearts.png'),2),
            '3_heart': (pygame.image.load('cards/3_of_hearts.png'),3),
            '4_heart': (pygame.image.load('cards/4_of_hearts.png'),4),
            '5_heart': (pygame.image.load('cards/5_of_hearts.png'),5),
            '6_heart': (pygame.image.load('cards/6_of_hearts.png'),6),
            '7_heart': (pygame.image.load('cards/7_of_hearts.png'),7),
            '8_heart': (pygame.image.load('cards/8_of_hearts.png'),8),
            '9_heart': (pygame.image.load('cards/9_of_hearts.png'),9),
            '10_heart': (pygame.image.load('cards/10_of_hearts.png'),10),
            'Jack_heart': (pygame.image.load('cards/jack_of_hearts2.png'),10),
            'Queen_heart': (pygame.image.load('cards/queen_of_hearts2.png'),10),
            'King_heart': (pygame.image.load('cards/king_of_hearts2.png'),10),
            'Ace_heart': (pygame.image.load('cards/ace_of_hearts.png'),0),

            '2_diamond': (pygame.image.load('cards/2_of_diamonds.png'),2),
            '3_diamond': (pygame.image.load('cards/3_of_diamonds.png'),3),
            '4_diamond': (pygame.image.load('cards/4_of_diamonds.png'),4),
            '5_diamond': (pygame.image.load('cards/5_of_diamonds.png'),5),
            '6_diamond': (pygame.image.load('cards/6_of_diamonds.png'),6),
            '7_diamond': (pygame.image.load('cards/7_of_diamonds.png'),7),
            '8_diamond': (pygame.image.load('cards/8_of_diamonds.png'),8),
            '9_diamond': (pygame.image.load('cards/9_of_diamonds.png'),9),
            '10_diamond': (pygame.image.load('cards/10_of_diamonds.png'),10),
            'Jack_diamond': (pygame.image.load('cards/jack_of_diamonds2.png'),10),
            'Queen_diamond': (pygame.image.load('cards/queen_of_diamonds2.png'),10),
            'King_diamond': (pygame.image.load('cards/king_of_diamonds2.png'),10),
            'Ace_diamond': (pygame.image.load('cards/ace_of_diamonds.png'),0),

            'Card_back' : (pygame.image.load('cardback.png'),0)
        }
        self.font = pygame.font.Font('pixelfont.ttf',128)
        self.deckImg = pygame.image.load('deck.png')
        self.action = None
        self.hand_tot = 0
        self.dealer_tot = 0
        self.result = None
        self.over = False
        self.deck = self.default_deck.copy()
        del self.deck['Card_back']
        self.bet = 0
        self.stand_ev = 0
        self.hit_ev = 0

    def setup(self,bet):
        self.payout = 0
        self.hand = []
        self.dealer_hand = []
        self.hand_tot = 0
        self.dealer_tot = 0
        self.over = False
        self.bet = bet
        try:
            self.deal()
        except Exception as error:
            if not self.deck:
                self.deck = self.default_deck.copy()
                del self.deck['Card_back']
            self.deal()
        time.sleep(0.3)

    def move_card(self,tx,ty):
        x,y = self.deck_pos[0],self.deck_pos[1]
        dx,dy = abs(tx-x),abs(ty-y)
        for i in range(-1,int(SPEED/3)):
            self.make_ui()
            scaled_card = pygame.transform.scale(self.default_deck['Card_back'][0],self.card_size)
            self.screen.blit(scaled_card,(x,y))
            pygame.display.flip()
            x -= dx/(SPEED/3)
            y += dy/(SPEED/3)
            self.clock.tick(SPEED)

    def play_game(self,action,bet=None,stand_ev=None,hit_ev=None):
        #check for quit
        self.bet = bet
        self.stand_ev = stand_ev
        self.hit_ev = hit_ev
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
        #play until stand
        self.action = action
        if self.action == 'h':
            self.play_step(self.action)
        #play as dealer if stood
        if self.action == 's':
            self.dealer()
        #calculate hands
        self.hand_tot = self.calc_hand(self.hand)
        self.dealer_tot = self.calc_hand(self.dealer_hand)
        #draw ui
        self.make_ui()
        #return lose/win and payout
        if self.over or self.hand_tot > 21:
            time.sleep(1)
            over = self.game_over(bet)
            if self.hand_tot == 21 and len(self.hand) == 2:
                self.payout = bet*2.5
            return over,self.hand_tot,self.dealer_tot, self.payout
        return False,self.hand_tot,self.dealer_tot, None
    
    def game_over(self,bet):
        if self.calc_hand(self.hand) > 21:
            self.payout = 0
            return 'l'
        elif self.dealer_tot > 21 or self.dealer_tot < self.hand_tot:
            self.payout = bet*2
            return 'w'
        elif self.dealer_tot > self.hand_tot:
            self.payout = 0
            return 'l'
        elif self.calc_hand(self.dealer_hand) == self.calc_hand(self.hand):
            self.payout = bet
            return 'p'

    def dealer(self):
        if self.dealer_tot < 17:
            if not self.deck:
                self.deck = self.default_deck.copy()
                del self.deck['Card_back']
            if 'Card_back' in self.dealer_hand:
                self.dealer_hand.pop(-1)
                card = random.choice(list(self.deck.keys()))
                self.dealer_hand.append(card)
                del self.deck[card]
            else:
                self.move_card(self.dealer_hand_pos[0]+(240*len(self.dealer_hand)),self.dealer_hand_pos[1])
                card = random.choice(list(self.deck.keys()))
                self.dealer_hand.append(card)
                del self.deck[card]
        elif self.dealer_tot >= 17:
            self.over = True

    def play_step(self,action):
        try:
            if self.action == 'h':
                self.move_card(self.hand_pos[0]+(240*len(self.hand)),self.hand_pos[1])
                card = random.choice(list(self.deck.keys()))
                self.hand.append(card)
                del self.deck[card]
        except Exception as error:
            self.deck = self.default_deck.copy()
            del self.deck['Card_back']
            self.move_card(self.hand_pos[0]+(240*len(self.hand)),self.hand_pos[1])
            card = random.choice(list(self.deck.keys()))
            self.hand.append(card)
            del self.deck[card]

    def calc_hand(self,hand):
        total = 0
        aces = 0
        for card in hand:
            val = self.default_deck[card][1]
            aces = aces+1 if val == 0 and card != 'Card_back' else aces
            total += val
        for ace in range(aces):
            if total + 11 <= 21:
                total += 11
            else:
                total += 1
        return total

    def deal(self):
        offset = 0
        for i in range(3):
            card = random.choice(list(self.deck.keys()))
            if i<2:
                self.move_card(self.hand_pos[0]+offset,self.hand_pos[1])
                self.hand.append(card)
                del self.deck[card]
            else:
                self.move_card(self.dealer_hand_pos[0],self.dealer_hand_pos[1])
                self.dealer_hand.append(card)
                del self.deck[card]
            offset += 240
        self.move_card(self.dealer_hand_pos[0]+240,self.dealer_hand_pos[1])
        self.dealer_hand.append('Card_back')
        self.hand_tot = self.calc_hand(self.hand)
        self.dealer_tot = self.calc_hand(self.dealer_hand)
        self.make_ui()
    
    def make_ui(self):
        self.screen.fill(GREEN)
        s_ev_txt = self.font.render(f'Stand EV: {round(self.stand_ev,2)}',True,WHITE)
        h_ev_txt = self.font.render(f'Hit EV: {round(self.hit_ev,2)}',True,WHITE)
        bet_txt = self.font.render(f'Bet: {self.bet}',True,WHITE)
        self.screen.blit(bet_txt,(900,70))
        self.screen.blit(s_ev_txt,(900,220))
        self.screen.blit(h_ev_txt,(900,370))
        scaled_deck = pygame.transform.scale(self.deckImg,(200,304))
        self.screen.blit(scaled_deck,self.deck_pos)
        player_txt = self.font.render(f'Player Hand: {self.hand_tot}',True,WHITE)
        dealer_txt = self.font.render(f'Dealer Hand: {self.dealer_tot}',True,WHITE)
        self.screen.blit(player_txt,(35*2,270*2))
        self.screen.blit(dealer_txt,(35*2,35*2))
        offset = 0
        dealer_offset = 0
        for card in self.hand:
            scaled_card = pygame.transform.scale(self.default_deck[card][0], self.card_size)
            self.screen.blit(scaled_card,(self.hand_pos[0]+offset,self.hand_pos[1]))
            offset += 240
        for card in self.dealer_hand:
            scaled_card = pygame.transform.scale(self.default_deck[card][0], self.card_size)
            self.screen.blit(scaled_card,(self.dealer_hand_pos[0]+dealer_offset,self.dealer_hand_pos[1]))
            dealer_offset += 240
        pygame.display.flip()
'''
g = Game()
g.setup()
while True:
    result,hand,dealer = g.play_game('s')
    if result != False:
        print(result)
        time.sleep(0.7)
        pygame.quit()
        quit()
'''