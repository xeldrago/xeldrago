import pygame
import random
import math

pygame.init()

# Window setup
WIDTH, HEIGHT = 1000, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casino Royale - Full Card Game")
FONT = pygame.font.SysFont("comicsans", 20)
BIG_FONT = pygame.font.SysFont("comicsans", 36)
clock = pygame.time.Clock()

# Constants
CARD_WIDTH, CARD_HEIGHT = 60, 90
SUITS = ['hearts', 'diamonds', 'spades', 'clubs']
# Colors for suits (red for hearts and diamonds, black for spades and clubs)
SUIT_COLORS = {
    'hearts': (255, 0, 0),
    'diamonds': (255, 0, 0),
    'spades': (0, 0, 0),
    'clubs': (0, 0, 0)
}
COLORS = [(255, 0, 0), (0, 255, 50), (0, 0, 255), (255, 255, 0)]
CENTER = (WIDTH//2, HEIGHT//2)
PLAYER_POSITIONS = {
    0: (CENTER[0] - CARD_WIDTH//2, HEIGHT - 140),      # South
    1: (CENTER[0] - CARD_WIDTH//2, 60),                # North
    2: (60, CENTER[1] - CARD_HEIGHT//2),               # West
    3: (WIDTH - 120, CENTER[1] - CARD_HEIGHT//2),      # East
}

# Card creation
def create_deck():
    return [(val, suit) for val in range(1, 14) for suit in SUITS]

def draw_heart(surface, x, y, size, color):
    pygame.draw.circle(surface, color, (x - size//3, y), size//3)
    pygame.draw.circle(surface, color, (x + size//3, y), size//3)
    points = [(x - size//2, y), (x + size//2, y), (x, y + size)]
    pygame.draw.polygon(surface, color, points)

def draw_diamond(surface, x, y, size, color):
    points = [(x, y - size), (x + size, y), (x, y + size), (x - size, y)]
    pygame.draw.polygon(surface, color, points)

def draw_spade(surface, x, y, size, color):
    pygame.draw.circle(surface, color, (x - size//3, y), size//3)
    pygame.draw.circle(surface, color, (x + size//3, y), size//3)
    points = [(x - size//2, y), (x + size//2, y), (x, y - size)]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.rect(surface, color, (x - 4, y, 8, size//2))

def draw_club(surface, x, y, size, color):
    pygame.draw.circle(surface, color, (x, y - size//3), size//3)
    pygame.draw.circle(surface, color, (x - size//3, y + size//4), size//3)
    pygame.draw.circle(surface, color, (x + size//3, y + size//4), size//3)
    pygame.draw.rect(surface, color, (x - 4, y, 8, size//2))

def draw_suit(surface, suit, center_x, center_y, size, color):
    if suit == 'hearts':
        draw_heart(surface, center_x, center_y, size, color)
    elif suit == 'diamonds':
        draw_diamond(surface, center_x, center_y, size, color)
    elif suit == 'spades':
        draw_spade(surface, center_x, center_y, size, color)
    elif suit == 'clubs':
        draw_club(surface, center_x, center_y, size, color)

def get_card_display(value):
    """Map card values to display rank"""
    ranks = {1: "A", 11: "J", 12: "Q", 13: "K"}
    return ranks.get(value, str(value))

class Player:
    def __init__(self, name, is_bot=True):
        self.name = name
        self.is_bot = is_bot
        self.chips = 100
        self.cards = []

    def draw_cards(self, deck):
        self.cards = [deck.pop(), deck.pop()]

players = [Player(f"Player {i+1}", True) for i in range(4)]
deck = create_deck()
random.shuffle(deck)
winner = ""
show_rules = True

def draw_card(surface, val, suit, x, y):
    pygame.draw.rect(surface, (255, 255, 255), (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=8)
    pygame.draw.rect(surface, (0, 0, 0), (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=8)
    
    # Display rank text top-left
    value_text = FONT.render(get_card_display(val), True, SUIT_COLORS[suit])
    surface.blit(value_text, (x + 5, y + 5))
    
    # Display suit shape center
    draw_suit(surface, suit, x + CARD_WIDTH//2, y + CARD_HEIGHT//2, 15, SUIT_COLORS[suit])
    
    # Display rank text bottom-right (rotated)
    value_text_rot = pygame.transform.rotate(value_text, 180)
    surface.blit(value_text_rot, (x + CARD_WIDTH - 20, y + CARD_HEIGHT - 25))

def draw_screen():
    SCREEN.fill((10, 90, 20))  # Table green
    title = BIG_FONT.render("♠ Casino Royale ♣", True, (255, 255, 255))
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 10))

    for i, p in enumerate(players):
        pos = PLAYER_POSITIONS[i]
        x, y = pos
        name = FONT.render(f"{p.name} ({'Bot' if p.is_bot else 'Human'})", True, COLORS[i])
        SCREEN.blit(name, (x, y - 20 if i != 0 else y + CARD_HEIGHT + 5))
        for j, card in enumerate(p.cards):
            draw_card(SCREEN, card[0], card[1], x + j * (CARD_WIDTH + 10), y)

        # Display chips below cards
        chips_text = FONT.render(f"Chips: {p.chips}", True, (255, 255, 255))
        SCREEN.blit(chips_text, (x, y + CARD_HEIGHT + 25))

    if winner:
        result = BIG_FONT.render(winner, True, (255, 255, 255))
        SCREEN.blit(result, (CENTER[0] - result.get_width()//2, HEIGHT//2 - 30))

    if show_rules:
        rules = [
            "RULES: Highest sum of 2 cards wins the round.",
            "Tie: Chips are split.",
            "Each player starts with 100 chips.",
            "Press [1-4] to toggle Bot/Human.",
            "Press [SPACE] to start round.",
            "Press [R] to reset game."
        ]
        for i, line in enumerate(rules):
            text = FONT.render(line, True, (255, 255, 255))
            SCREEN.blit(text, (30, 580 + i * 25))

    pygame.display.update()

def play_round():
    global winner, deck
    if len(deck) < 8:
        deck = create_deck()
        random.shuffle(deck)
    for p in players:
        p.draw_cards(deck)

    max_score = max(sum(card[0] for card in p.cards) for p in players)
    winners = [p for p in players if sum(card[0] for card in p.cards) == max_score]
    pot = 10 * len(players)
    for p in players:
        p.chips -= 10
    for p in winners:
        p.chips += pot // len(winners)

    if len(winners) == 1:
        winner = f"{winners[0].name} wins this round!"
    else:
        winner = "It's a tie!"

def reset_game():
    global winner, deck
    winner = ""
    deck = create_deck()
    random.shuffle(deck)
    for p in players:
        p.chips = 100
        p.cards = []

# Main loop
running = True
while running:
    clock.tick(60)
    draw_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play_round()
            elif event.key == pygame.K_r:
                reset_game()
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                idx = event.key - pygame.K_1
                players[idx].is_bot = not players[idx].is_bot

pygame.quit()
