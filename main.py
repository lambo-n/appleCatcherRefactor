# Apple Catcher - pygame-native rewrite.
#
# Everything is drawn to a fixed-size 500x500 "canvas" Surface using native
# pygame calls (pygame.Rect, pygame.draw, pygame.font, Sprite/Group). The
# canvas is then scaled once to the live window, so the game scales cleanly
# without any per-primitive scaling math.
import pygame 
import random
import os
from apple import Apple
from booster import Booster

pygame.init()

CANVAS_SIZE = (500, 500)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
pygame.display.set_caption("Apple Catcher")
canvas = pygame.Surface(CANVAS_SIZE)    
clock = pygame.time.Clock()
running = True


# ----------------------------------------------------------------------
# Asset loading
# ----------------------------------------------------------------------

def load_img(filename):
    path = os.path.join("assets", filename)
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception:
        return None


alpsimg = load_img("pixil-frame-0 (6).png")
pauseimg = load_img("pause.png")
heart = load_img("heartemoji.png")
resumeimg = load_img("resume.png")
basket = load_img("download__4_-removebg-preview.png")
orange = load_img("ORANGE.png")
pear = load_img("PEAR.png")
settings_img = load_img("settings.png")
trail_img = load_img("trail.png")


# ----------------------------------------------------------------------
# Native drawing helpers (cached fonts + cached scaled images)
# ----------------------------------------------------------------------

_font_cache = {}
_scaled_cache = {}


def get_font(size):
    font = _font_cache.get(size)
    if font is None:
        font = pygame.font.Font(None, size)
        _font_cache[size] = font
    return font


def draw_img(img, x, y, w, h):
    """Blit an image scaled to (w, h) at (x, y). Scaled results are cached."""
    if img is None:
        return
    key = (id(img), w, h)
    scaled = _scaled_cache.get(key)
    if scaled is None:
        scaled = pygame.transform.scale(img, (w, h))
        _scaled_cache[key] = scaled
    canvas.blit(scaled, (x, y))


def draw_text(msg, x, y, size, color, anchor="topleft"):
    surf = get_font(size).render(str(msg), True, color)
    canvas.blit(surf, surf.get_rect(**{anchor: (x, y)}))


def draw_text_centered(msg, rect, size, color):
    surf = get_font(size).render(str(msg), True, color)
    canvas.blit(surf, surf.get_rect(center=rect.center))

def display_time_left():
    global timeLeft
    draw_text("Time Left: " + str(timeLeft), 20, 25, 15, (255, 0, 0), anchor="midtop")


# ----------------------------------------------------------------------
# Layout: button hitboxes as pygame.Rect (canvas space)
# ----------------------------------------------------------------------

BTN_PAUSE = pygame.Rect(447, 10, 50, 50)
BTN_MENU_PAUSED = pygame.Rect(320, 11, 100, 50)
BTN_SETTINGS_PAUSED = pygame.Rect(254, 11, 50, 50)

BTN_LEVEL1 = pygame.Rect(75, 200, 100, 50)
BTN_LEVEL2 = pygame.Rect(200, 200, 100, 50)
BTN_LEVEL3 = pygame.Rect(325, 200, 100, 50)
BTN_SHOP = pygame.Rect(200, 350, 100, 50)
BTN_SETTINGS_MENU = pygame.Rect(0, 0, 50, 50)
BTN_CONTINUE = pygame.Rect(50, 0, 100, 50)
BTN_1v1 = pygame.Rect(200,280,100,50)
BTN_SETTINGS_BACK = pygame.Rect(410, 460, 90, 40)
BTN_BG_COLOR = pygame.Rect(110, 120, 270, 50)
BTN_CORDS = pygame.Rect(110, 180, 270, 50)

BTN_GAMEOVER_MENU = pygame.Rect(150, 300, 200, 50)

BTN_SHOP_BACK = pygame.Rect(0, 430, 100, 69)
SHOP_ORANGE = pygame.Rect(10, 150, 80, 30)
SHOP_PEAR = pygame.Rect(120, 150, 80, 30)
SHOP_TRAIL = pygame.Rect(230, 150, 80, 30)


# ----------------------------------------------------------------------
# Game state
# ----------------------------------------------------------------------

basket_rect = pygame.Rect(191, 220, 100, 50)

player1_pos = pygame.Vector2(100, 400)
player2_pos = pygame.Vector2(400, 400)

apples = pygame.sprite.Group()
boosters = pygame.sprite.Group()
score = 0   
p1_score = 0
p2_score = 0
lives = 3
difficulty = 3
gameState = "menu"
previousState = "menu"
alps = 100
speed = 9
baseSpeed = 9
speedBoostTimer = 0
boostAmount = 5
boostLength = 150
boosterSpawnCooldown = 0
trailPoints = []
trailMaxLength = 30
save = False
saveLevel = 1
showCords = True
timerEvent = pygame.USEREVENT + 1
pygame.time.set_timer(timerEvent, 9000)
timeLeft = 90

bgColors = [
    (21, 39, 237), (219, 98, 22), (56, 217, 75), (245, 232, 93),
    (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255),
    (255, 165, 0), (128, 0, 128), (255, 192, 203), (165, 42, 42),
    (0, 128, 0), (0, 0, 128), (0, 128, 128), (128, 128, 0), (128, 128, 128),
]
bgIndex = 0
bgSettings = [
    (30, 30, 30), (219, 98, 22), (56, 217, 75), (245, 232, 93),
    (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255),
    (255, 165, 0), (128, 0, 128), (255, 192, 203), (165, 42, 42),
    (0, 128, 0), (0, 0, 128), (0, 128, 128), (128, 128, 0), (128, 128, 128),
]

orangeOwned = orangeEquipped = False
pearOwned = pearEquipped = False
trailOwned = trailEquipped = False
orangeBoughtFlashFrames = pearBoughtFlashFrames = trailBoughtFlashFrames = 0
BOUGHT_FLASH_MAX = 45

# Faint red trail stamp, built once.
trail_stamp = pygame.Surface((10, 10), pygame.SRCALPHA)
trail_stamp.fill((237, 9, 9, 70))


# ----------------------------------------------------------------------
# Game helpers
# ----------------------------------------------------------------------

def current_basket_img():
    if pearEquipped:
        return pear
    if orangeEquipped:
        return orange
    return basket


def to_canvas(pos):
    """Map a window-space point into canvas space."""
    mx, my = pos
    w, h = screen.get_size()
    return mx * CANVAS_SIZE[0] / w, my * CANVAS_SIZE[1] / h


def mouse_canvas():
    """Current mouse position mapped from window space into canvas space."""
    return to_canvas(pygame.mouse.get_pos())


def draw_trail():
    for (x, y) in trailPoints:
        canvas.blit(trail_stamp, trail_stamp.get_rect(center=(x, y)))


def show_score():
    draw_text("Score: " + str(score), 41, 25, 25, WHITE)


def show_lives():
    for i in range(lives):
        draw_img(heart, 330 + i * 50, 425, 70, 50)


def start_game(level):
    global difficulty, baseSpeed, saveLevel, speed, speedBoostTimer, gameState
    global score, lives, alps, save, timeLeft
    if level == 1:
        difficulty, baseSpeed, saveLevel = 1, 9, 1
    elif level == 2:
        difficulty, baseSpeed, saveLevel = 3, 9, 2
    elif level == 3:
        difficulty, baseSpeed, saveLevel = 6, 11, 3
    speed = baseSpeed
    speedBoostTimer = 0
    boosters.empty()
    apples.empty()
    score = 0
    lives = 3
    basket_rect.topleft = (191, 220)
    gameState = "play"


# ----------------------------------------------------------------------
# Event handling
# ----------------------------------------------------------------------

def handle_keydown(event):
    global gameState, showCords, bgIndex
    k = event.key

    if gameState == "menu":
        if k == pygame.K_1:
            start_game(1)
        elif k == pygame.K_2:
            start_game(2)
        elif k == pygame.K_3:
            start_game(3)
        elif k == pygame.K_BACKQUOTE:
            gameState = "shop"
        elif k == pygame.K_s:
            gameState = "settings"
        elif k == pygame.K_c:
            gameState = "paused"
    elif gameState == "shop":
        if k in (pygame.K_t, pygame.K_b):
            gameState = "menu"
    elif gameState == "settings":
        if k == pygame.K_b:
            gameState = "menu"
        elif k == pygame.K_c:
            showCords = False
        elif k == pygame.K_g:
            bgIndex = (bgIndex + 1) % len(bgColors)
    elif gameState == "paused":
        if k == pygame.K_q:
            gameState = "play"
        elif k == pygame.K_b:
            gameState = "menu"
        elif k == pygame.K_s:
            gameState = "settings"
    elif gameState == "play":
        if k == pygame.K_BACKQUOTE:
            gameState = "paused"
    elif gameState == "gameOver":
        if k == pygame.K_SPACE:
            gameState = "menu"
    elif gameState =="1v1":
        pass 

def handle_mouse_click(pos):
    global gameState, save, previousState, bgIndex, showCords
    global orangeOwned, orangeEquipped, alps, orangeBoughtFlashFrames
    global pearOwned, pearEquipped, pearBoughtFlashFrames
    global trailOwned, trailEquipped, trailPoints, trailBoughtFlashFrames
    global speedBoostTimer, speed
    p = to_canvas(pos)
    gs = gameState

    if BTN_PAUSE.collidepoint(p):
        if gs == "play":
            gameState = "paused"
            return
        if gs == "paused":
            gameState = "play"
            return

    if gs == "paused":
        if BTN_MENU_PAUSED.collidepoint(p):
            gameState = "menu"
            save = True
            return
        if BTN_SETTINGS_PAUSED.collidepoint(p):
            previousState = "paused"
            gameState = "settings"
            return

    if gs == "settings":
        if BTN_SETTINGS_BACK.collidepoint(p):
            gameState = previousState
            return
        if BTN_BG_COLOR.collidepoint(p):
            bgIndex = (bgIndex + 1) % len(bgColors)
            return
        if BTN_CORDS.collidepoint(p):
            showCords = not showCords
            return

    if gs == "menu":
        if BTN_LEVEL1.collidepoint(p):
            start_game(1)
            return
        if BTN_LEVEL2.collidepoint(p):
            start_game(2)
            return
        if BTN_LEVEL3.collidepoint(p):
            start_game(3)
            return
        if BTN_SHOP.collidepoint(p):
            gameState = "shop"
            return
        if BTN_SETTINGS_MENU.collidepoint(p):
            previousState = "menu"
            gameState = "settings"
            return
        if BTN_1v1.collidepoint(p):
            gameState = "1v1"
            return
            
        
        if save and BTN_CONTINUE.collidepoint(p):
            gameState = "paused"
            return

    if gs == "gameOver":
        if BTN_GAMEOVER_MENU.collidepoint(p):
            save = False
            apples.empty()
            boosters.empty()
            score = 0
            lives = 3
            gameState = "menu"
            speedBoostTimer = 0
            speed = baseSpeed
            basket_rect.topleft = (191, 220)
            trailPoints = []
            return

    if gs == "shop":
        if BTN_SHOP_BACK.collidepoint(p):
            gameState = "menu"
            return
        if SHOP_ORANGE.collidepoint(p):
            if orangeBoughtFlashFrames > 0:
                return
            if not orangeOwned:
                if alps >= 6:
                    orangeOwned = True
                    orangeEquipped = False
                    alps -= 6
                    orangeBoughtFlashFrames = BOUGHT_FLASH_MAX
                return
            orangeEquipped = not orangeEquipped
            if orangeEquipped:
                pearEquipped = False
            return
        if SHOP_PEAR.collidepoint(p):
            if pearBoughtFlashFrames > 0:
                return
            if not pearOwned:
                if alps >= 8:
                    pearOwned = True
                    alps -= 8
                    pearBoughtFlashFrames = BOUGHT_FLASH_MAX
                return
            pearEquipped = not pearEquipped
            if pearEquipped:
                orangeEquipped = False
            return
        if SHOP_TRAIL.collidepoint(p):
            if trailBoughtFlashFrames > 0:
                return
            if not trailOwned:
                if alps >= 9:
                    trailOwned = True
                    alps -= 9
                    trailBoughtFlashFrames = BOUGHT_FLASH_MAX
                return
            trailEquipped = not trailEquipped
            trailPoints = []
            return


# ----------------------------------------------------------------------
# Drawing per state
# ----------------------------------------------------------------------

def draw_menu():
    for r in (BTN_LEVEL1, BTN_LEVEL2, BTN_LEVEL3, BTN_SHOP, BTN_SETTINGS_MENU,BTN_1v1):
        pygame.draw.rect(canvas, WHITE, r)
    draw_img(settings_img, -10, 0, 70, 50)

    c = (31, 150, 255)
    draw_text_centered("Level 1", BTN_LEVEL1, 20, c)
    draw_text_centered("Level 2", BTN_LEVEL2, 20, c)
    draw_text_centered("Level 3", BTN_LEVEL3, 20, c)
    draw_text_centered("Shop", BTN_SHOP, 20, c)
    draw_text_centered("1v1",BTN_1v1,20,c)
    if save:
        pygame.draw.rect(canvas, WHITE, BTN_CONTINUE)
        draw_text_centered("Continue", pygame.Rect(50, 0, 100, 25), 17, (31, 150, 25))
        draw_text_centered("Level " + str(saveLevel),
                           pygame.Rect(50, 25, 100, 25), 17, (31, 150, 25))


def _draw_shop_item(item_rect, icon_rect, owned, equipped, flash, cost, hovered):
    pygame.draw.rect(canvas, WHITE, icon_rect)
    pygame.draw.rect(canvas, WHITE, item_rect)
    if flash > 0:
        draw_text_centered("Bought", item_rect, 20, (0, 128, 0))
    elif not owned:
        if hovered:
            if alps >= cost:
                draw_text_centered("Buy", item_rect, 20, (0, 128, 0))
            else:
                draw_text_centered("Not enough", item_rect, 13, (232, 46, 53))
        else:
            draw_text_centered(str(cost) + " Alps", item_rect, 20, (237, 141, 45))
    elif equipped:
        draw_text_centered("Unequip", item_rect, 18, (237, 141, 45))
    else:
        draw_text_centered("Equip", item_rect, 20, (0, 128, 0) if hovered else (237, 141, 45))


def draw_shop():
    p = mouse_canvas()

    draw_img(alpsimg, 330, 387, 200, 200)
    draw_text(":", 455, 463, 20, (48, 217, 205))
    draw_text(str(alps), 465, 465, 20, (48, 217, 205))

    pygame.draw.rect(canvas, WHITE, pygame.Rect(0, 0, 500, 50))
    draw_text_centered("WELCOME TO THE SHOP", pygame.Rect(0, 0, 500, 50), 40, (237, 22, 22))

    pygame.draw.rect(canvas, WHITE, BTN_SHOP_BACK)
    draw_text_centered("Back To Menu", BTN_SHOP_BACK, 14, (237, 22, 22))

    _draw_shop_item(SHOP_ORANGE, pygame.Rect(10, 70, 80, 70), orangeOwned,
                    orangeEquipped, orangeBoughtFlashFrames, 6, SHOP_ORANGE.collidepoint(p))
    draw_img(orange, 20, 70, 60, 60)

    _draw_shop_item(SHOP_PEAR, pygame.Rect(120, 70, 80, 70), pearOwned,
                    pearEquipped, pearBoughtFlashFrames, 8, SHOP_PEAR.collidepoint(p))
    draw_img(pear, 121, 64, 80, 80)

    _draw_shop_item(SHOP_TRAIL, pygame.Rect(230, 71, 80, 70), trailOwned,
                    trailEquipped, trailBoughtFlashFrames, 9, SHOP_TRAIL.collidepoint(p))
    draw_img(trail_img, 240, 76, 60, 60)


def draw_settings():
    canvas.fill(bgSettings[bgIndex])
    draw_text("SETTINGS", 173, 60, 40, WHITE)

    pygame.draw.rect(canvas, WHITE, BTN_SETTINGS_BACK)
    draw_text_centered("Back", BTN_SETTINGS_BACK, 18, (0, 0, 0))

    pygame.draw.rect(canvas, (220, 220, 220), BTN_BG_COLOR)
    draw_text_centered("Background color", BTN_BG_COLOR, 18, (0, 0, 0))

    pygame.draw.rect(canvas, (220, 220, 220), BTN_CORDS)
    draw_text_centered("Cords:ON" if showCords else "Cords:OFF", BTN_CORDS, 18, (0, 0, 0))


def draw_basket_and_entities():
    if trailEquipped:
        draw_trail()
    draw_img(current_basket_img(), basket_rect.x, basket_rect.y, 100, 50)
    apples.draw(canvas)
    boosters.draw(canvas)
    show_score()
    show_lives()


def draw_paused():
    draw_basket_and_entities()

    pygame.draw.rect(canvas, WHITE, BTN_PAUSE)
    draw_img(resumeimg, 448, 11, 50, 50)
    pygame.draw.rect(canvas, WHITE, BTN_MENU_PAUSED)
    draw_text_centered("Menu", BTN_MENU_PAUSED, 20, (0, 0, 0))
    pygame.draw.rect(canvas, WHITE, BTN_SETTINGS_PAUSED)
    draw_img(settings_img, 244, 11, 70, 50)

    if speedBoostTimer > 0:
        draw_text("BOOST READY", 180, 80, 20, (255, 240, 0))


def draw_game_over():
    canvas.fill((0, 0, 0))
    draw_text("GAME OVER", 55, 190, 90, (80, 240, 31))
    draw_text("Final Score: " + str(score), 163, 395, 35, (73, 217, 48))
    pygame.draw.rect(canvas, (80, 240, 31), BTN_GAMEOVER_MENU)
    draw_text_centered("MENU", BTN_GAMEOVER_MENU, 40, (35, 161, 156))


def update_and_draw_play():
    global speed, speedBoostTimer, boosterSpawnCooldown, score, lives, alps, gameState,timeLeft

    if random.randint(1, 57) == 8:
        apples.add(Apple(difficulty))

    if boosterSpawnCooldown > 0:
        boosterSpawnCooldown -= 1
    elif random.randint(1, 220) == 12:
        boosters.add(Booster())
        boosterSpawnCooldown = 120

    if speedBoostTimer > 0:
        speedBoostTimer -= 1
        speed = baseSpeed + boostAmount
    else:
        speed = baseSpeed

    if trailEquipped:
        trailPoints.append((basket_rect.x + 50, basket_rect.y + 30))
        if len(trailPoints) > trailMaxLength:
            trailPoints.pop(0)
        draw_trail()

    player1_pos = pygame.Vector2(0, 500)
    
    print(player1_pos) # (0, 500)
    
    # x variable
    print(player1_pos.x) # 0
    print(player1_pos.y) # 500
    
    print(basket_rect) # (191, 220)

    draw_img(current_basket_img(), basket_rect.x, basket_rect.y, 100, 50)

    # Apples: a loose catch box around the basket; missed if they fall past 425.
    catch_box = pygame.Rect(basket_rect.x - 49, basket_rect.y - 49, 149, 49)
    apples.update()
    for apple in list(apples):
        if apple.rect.top >= 425:
            apple.kill()
            lives -= 1
        elif catch_box.collidepoint(apple.rect.topleft):
            apple.kill()
            score += 1
            if (difficulty == 1 and score % 5 == 0) or \
               (difficulty == 3 and score % 3 == 0) or \
               (difficulty == 6 and score % 2 == 0):
                alps += 1
    apples.draw(canvas)

    # Boosters.
    boost_box = pygame.Rect(basket_rect.x - 20, basket_rect.y - 35, 120, 55)
    boosters.update()
    for booster in list(boosters):
        if booster.rect.centery > 520:
            booster.kill()
        elif boost_box.collidepoint(booster.rect.center):
            booster.kill()
            speedBoostTimer = boostLength
    boosters.draw(canvas)

    if speedBoostTimer > 0:
        draw_text("Boost!", 227, 65, 22, (255, 230, 0))

    if lives <= 0:
        gameState = "gameOver"

    show_score()
    show_lives()

    pygame.draw.rect(canvas, WHITE, BTN_PAUSE)
    draw_img(pauseimg, 448, 11, 50, 50)


def draw_1v1():
    canvas.fill("black")    
    
    player1_rect = pygame.Rect(player1_pos.x, player1_pos.y, 50, 50)
    player2_rect = pygame.Rect(player2_pos.x, player2_pos.y, 50, 50)
    
    draw_text("Player 1 score: " + str(p1_score), 20, 20, 20, (255, 0, 0))
    draw_text("Player 2 score: " + str(p2_score), 350, 20, 20, (255, 0, 0))
    


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((max(event.w, 1), max(event.h, 1)),
                                             pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_mouse_click(event.pos)

        elif event.type == timerEvent:
            if timeLeft > 0 and gameState == "1v1":
                timeLeft -= 1
                display_time_left()
            elif timeLeft <= 0 and gameState == "1v1":
                gameState = "gameOver"


    if gameState == "play":
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and basket_rect.x >= 0:
            basket_rect.x -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and basket_rect.x <= 400:
            basket_rect.x += speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and basket_rect.y <= 450:
            basket_rect.y += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and basket_rect.y >= 0:
            basket_rect.y -= speed
            
    

    if gameState not in ("settings", "gameOver"):
        canvas.fill(bgColors[bgIndex])
        draw_img(alpsimg, 220, -50, 200, 200)
        draw_text(":", 345, 27, 20, (48, 217, 205))
        draw_text(str(alps), 357, 27, 20, (48, 217, 205))

    if orangeBoughtFlashFrames > 0:
        orangeBoughtFlashFrames -= 1
    if pearBoughtFlashFrames > 0:
        pearBoughtFlashFrames -= 1
    if trailBoughtFlashFrames > 0:
        trailBoughtFlashFrames -= 1

    if gameState == "menu":
        draw_menu()
    elif gameState == "shop":
        draw_shop()
    elif gameState == "settings":
        draw_settings()
    elif gameState == "paused":
        draw_paused()
    elif gameState == "gameOver":
        draw_game_over()
    elif gameState == "play":
        update_and_draw_play()
    elif gameState == "1v1":
        draw_1v1()

    if showCords:
        mx, my = mouse_canvas()
        draw_text(str(int(mx)) + ", " + str(int(my)), 20, 497, 15, (255, 0, 0),
                  anchor="bottomleft")

    # Scale the fixed canvas up to the live window and present.
    # smoothscale anti-aliases the upscale so text/edges aren't pixelated.
    pygame.transform.smoothscale(canvas, screen.get_size(), screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
