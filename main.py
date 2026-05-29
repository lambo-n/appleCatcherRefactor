# Apple Catcher - module-level (no classes), following the quickstart.py layout.
import pygame
import random
import os
from apple import Apple

# pygame setup
pygame.init()

# All layout below is authored in a fixed "base" coordinate space and scaled to
# the live window size, so the game scales with the window.
baseW = 500
baseH = 500
width = 600
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Apple Catcher")
clock = pygame.time.Clock()
running = True


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

# game state
basketx = 191
baskety = 220
applelist = []
score = 0
lives = 3
difficulty = 3
gameState = "menu"
previousState = "menu"
alps = 100
speed = 9
baseSpeed = 9
boosterList = []
speedBoostTimer = 0
boostAmount = 5
boostLength = 150
boosterSpawnCooldown = 0
trailPoints = []
trailMaxLength = 30
save = False
saveLevel = 1
showCords = True

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

orangeOwned = False
orangeEquipped = False
orangeBoughtFlashMax = 45
orangeBoughtFlashFrames = 0

pearOwned = False
pearEquipped = False
pearBoughtFlashMax = 45
pearBoughtFlashFrames = 0

trailOwned = False
trailEquipped = False
trailBoughtFlashMax = 45
trailBoughtFlashFrames = 0


# ----------------------------------------------------------------------
# Scaling (base space -> live window space)
# ----------------------------------------------------------------------

def fx():
    """Horizontal scale factor."""
    return width / baseW


def fy():
    """Vertical scale factor."""
    return height / baseH


def fs():
    """Uniform scale factor for fonts and circles (avoids distortion)."""
    return min(fx(), fy())


def on_resize(w, h):
    global width, height, screen
    width = max(w, 1)
    height = max(h, 1)
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)


def mouse_base():
    """Mouse position converted from window space back into base space."""
    mx, my = pygame.mouse.get_pos()
    return mx / fx(), my / fy()


# ----------------------------------------------------------------------
# Drawing primitives
# ----------------------------------------------------------------------

def blit(img, x, y, w, h):
    if img is None:
        return
    scaled = pygame.transform.scale(img, (int(w * fx()), int(h * fy())))
    screen.blit(scaled, (int(x * fx()), int(y * fy())))


def text(msg, x, y, size, color):
    font = pygame.font.Font(None, max(1, int(size * fs())))
    surf = font.render(str(msg), True, color)
    # y is baseline in Processing; subtract ascent to convert to top-left
    screen.blit(surf, (int(x * fx()), int(y * fy()) - font.get_ascent()))


def rect(color, x, y, w, h):
    pygame.draw.rect(
        screen, color,
        (int(x * fx()), int(y * fy()), int(w * fx()), int(h * fy())),
    )


def text_centered(msg, rx, ry, rw, rh, size, color):
    font = pygame.font.Font(None, max(1, int(size * fs())))
    surf = font.render(str(msg), True, color)
    text_rect = surf.get_rect(center=(
        int((rx + rw / 2) * fx()), int((ry + rh / 2) * fy()),
    ))
    screen.blit(surf, text_rect)


def ellipse(color, cx, cy, w, h):
    pygame.draw.ellipse(
        screen, color,
        (int((cx - w / 2) * fx()), int((cy - h / 2) * fy()),
         int(w * fx()), int(h * fy())),
    )


# ----------------------------------------------------------------------
# Game helpers
# ----------------------------------------------------------------------

def current_basket_img():
    if pearEquipped:
        return pear
    if orangeEquipped:
        return orange
    return basket


def create_booster():
    return {"x": random.randint(30, 470), "y": -20, "size": 40, "fallSpeed": 4}


def draw_booster(booster):
    ellipse((255, 230, 0), booster["x"], booster["y"], booster["size"], booster["size"])
    text("S", booster["x"] - 5, booster["y"] + 6, 25, (0, 120, 255))


def draw_trail():
    w = max(1, int(10 * fx()))
    h = max(1, int(10 * fy()))
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((237, 9, 9, 70))
    for (x, y) in trailPoints:
        screen.blit(surf, (int(x * fx() - w / 2), int(y * fy() - h / 2)))


def show_score():
    text("Score: " + str(score), 41, 38, 25, (255, 255, 255))


def show_lives():
    hx = 330
    for _ in range(lives):
        blit(heart, hx, 425, 70, 50)
        hx += 50


def start_game(level):
    global difficulty, baseSpeed, saveLevel, speed, speedBoostTimer
    global boosterList, applelist, score, lives, basketx, baskety, gameState
    if level == 1:
        difficulty = 1
        baseSpeed = 9
        saveLevel = 1
    elif level == 2:
        difficulty = 3
        baseSpeed = 9
        saveLevel = 2
    elif level == 3:
        difficulty = 6
        baseSpeed = 11
        saveLevel = 3
    speed = baseSpeed
    speedBoostTimer = 0
    boosterList = []
    applelist = []
    score = 0
    lives = 3
    basketx = 191
    baskety = 220
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


def handle_mouse_click(mx, my):
    global gameState, save, previousState, bgIndex, showCords
    global orangeOwned, orangeEquipped, alps, orangeBoughtFlashFrames
    global pearOwned, pearEquipped, pearBoughtFlashFrames
    global trailOwned, trailEquipped, trailPoints
    global applelist, boosterList, score, lives, speedBoostTimer, speed
    global basketx, baskety
    # Incoming coords are in window space; convert to base space so the
    # hit-boxes below stay authored in the fixed 500x500 layout.
    mx = mx / fx()
    my = my / fy()
    gs = gameState

    # Pause / resume button (play & paused states)
    if 447 <= mx <= 497 and 10 <= my <= 60:
        if gs == "play":
            gameState = "paused"
            return
        if gs == "paused":
            gameState = "play"
            return

    # Menu button while paused
    if 320 <= mx <= 420 and 11 <= my <= 61:
        if gs == "paused":
            gameState = "menu"
            save = True
            return

    # Settings button while paused
    if gs == "paused" and 244 <= mx <= 314 and 10 <= my <= 61:
        previousState = "paused"
        gameState = "settings"
        return

    if gs == "settings":
        if 411 <= mx <= 498 and 461 <= my <= 500:
            gameState = previousState
            return
        if 112 <= mx <= 378 and 123 <= my <= 172:
            bgIndex = (bgIndex + 1) % len(bgColors)
            return
        if 110 <= mx <= 382 and 182 <= my <= 231:
            showCords = not showCords
            return

    if gs == "menu":
        if 75 <= mx <= 175 and 200 <= my <= 250:
            start_game(1)
            return
        if 200 <= mx <= 300 and 200 <= my <= 250:
            start_game(2)
            return
        if 325 <= mx <= 425 and 200 <= my <= 250:
            start_game(3)
            return
        if 200 <= mx <= 300 and 350 <= my <= 400:
            gameState = "shop"
            return
        if 0 <= mx <= 50 and 0 <= my <= 50:
            previousState = "menu"
            gameState = "settings"
            return
        if 51 <= mx <= 148 and 0 <= my <= 50 and save:
            gameState = "paused"
            return

    if gs == "gameOver":
        if 150 <= mx <= 325 and 300 <= my <= 350:
            save = False
            applelist = []
            boosterList = []
            score = 0
            lives = 3
            gameState = "menu"
            speedBoostTimer = 0
            speed = baseSpeed
            basketx = 191
            baskety = 220
            trailPoints = []
            return

    if gs == "shop":
        if 20 <= mx <= 90 and 433 <= my <= 493:
            gameState = "menu"
            return
        if 10 <= mx <= 90 and 150 <= my <= 180:
            if orangeBoughtFlashFrames > 0:
                return
            if not orangeOwned:
                if alps >= 6:
                    orangeOwned = True
                    orangeEquipped = False
                    alps -= 6
                    orangeBoughtFlashFrames = orangeBoughtFlashMax
                return
            orangeEquipped = not orangeEquipped
            if orangeEquipped:
                pearEquipped = False
            return
        if 121 <= mx <= 199 and 150 <= my <= 180:
            if pearBoughtFlashFrames > 0:
                return
            if not pearOwned:
                if alps >= 8:
                    pearOwned = True
                    alps -= 8
                    pearBoughtFlashFrames = pearBoughtFlashMax
                return
            pearEquipped = not pearEquipped
            if pearEquipped:
                orangeEquipped = False
            return
        if 231 <= mx <= 308 and 150 <= my <= 180:
            if trailBoughtFlashFrames > 0:
                return
            if not trailOwned:
                if alps >= 9:
                    trailOwned = True
                    alps -= 9
                    trailBoughtFlashFrames = trailBoughtFlashMax
                return
            trailEquipped = not trailEquipped
            trailPoints = []
            return


# ----------------------------------------------------------------------
# Drawing per state
# ----------------------------------------------------------------------

def draw_menu():
    rect((255, 255, 255), 75, 200, 100, 50)
    rect((255, 255, 255), 200, 200, 100, 50)
    rect((255, 255, 255), 325, 200, 100, 50)
    rect((255, 255, 255), 200, 350, 100, 50)
    rect((255, 255, 255), 0, 0, 50, 50)
    blit(settings_img, -10, 0, 70, 50)

    c = (31, 150, 255)
    text_centered("Level 1", 75, 200, 100, 50, 20, c)
    text_centered("Level 2", 200, 200, 100, 50, 20, c)
    text_centered("Level 3", 325, 200, 100, 50, 20, c)
    text_centered("Shop", 200, 350, 100, 50, 20, c)

    if save:
        rect((255, 255, 255), 50, 0, 100, 50)
        text_centered("Continue", 50, 0, 100, 25, 17, (31, 150, 25))
        text_centered("Level " + str(saveLevel), 50, 25, 100, 25, 17, (31, 150, 25))


def draw_shop():
    mx, my = mouse_base()

    blit(alpsimg, 330, 387, 200, 200)
    text(":", 455, 470, 20, (48, 217, 205))
    text(str(alps), 465, 472, 20, (48, 217, 205))

    rect((255, 255, 255), 0, 0, 500, 50)
    text_centered("WELCOME TO THE SHOP", 0, 0, 500, 50, 40, (237, 22, 22))

    rect((255, 255, 255), 0, 430, 100, 69)
    text_centered("Back To Menu", 0, 430, 100, 69, 14, (237, 22, 22))

    # --- Orange ---
    rect((255, 255, 255), 10, 70, 80, 70)
    rect((255, 255, 255), 10, 150, 80, 30)
    oh = 10 <= mx <= 90 and 150 <= my <= 180
    if orangeBoughtFlashFrames > 0:
        text_centered("Bought", 10, 150, 80, 30, 20, (0, 128, 0))
    elif not orangeOwned:
        if oh:
            if alps >= 6:
                text_centered("Buy", 10, 150, 80, 30, 20, (0, 128, 0))
            else:
                text_centered("Not enough", 10, 150, 80, 30, 13, (232, 46, 53))
        else:
            text_centered("6 Alps", 10, 150, 80, 30, 20, (237, 141, 45))
    else:
        if orangeEquipped:
            text_centered("Unequip", 10, 150, 80, 30, 18, (237, 141, 45))
        else:
            text_centered("Equip", 10, 150, 80, 30, 20, (0, 128, 0) if oh else (237, 141, 45))
    blit(orange, 20, 70, 60, 60)

    # --- Pear ---
    rect((255, 255, 255), 120, 70, 80, 70)
    rect((255, 255, 255), 120, 150, 80, 30)
    ph = 121 <= mx <= 199 and 150 <= my <= 180
    if pearBoughtFlashFrames > 0:
        text_centered("Bought", 120, 150, 80, 30, 20, (0, 128, 0))
    elif not pearOwned:
        if ph:
            if alps >= 8:
                text_centered("Buy", 120, 150, 80, 30, 20, (0, 128, 0))
            else:
                text_centered("Not enough", 120, 150, 80, 30, 13, (232, 46, 53))
        else:
            text_centered("8 Alps", 120, 150, 80, 30, 20, (237, 141, 45))
    else:
        if pearEquipped:
            text_centered("Unequip", 120, 150, 80, 30, 18, (237, 141, 45))
        else:
            text_centered("Equip", 120, 150, 80, 30, 20, (0, 128, 0) if ph else (237, 141, 45))
    blit(pear, 121, 64, 80, 80)

    # --- Trail ---
    rect((255, 255, 255), 230, 71, 80, 70)
    rect((255, 255, 255), 230, 150, 80, 30)
    th = 231 <= mx <= 308 and 150 <= my <= 180
    if trailBoughtFlashFrames > 0:
        text_centered("Bought", 230, 150, 80, 30, 20, (0, 128, 0))
    elif not trailOwned:
        if th:
            if alps >= 9:
                text_centered("Buy", 230, 150, 80, 30, 20, (0, 128, 0))
            else:
                text_centered("Not enough", 230, 150, 80, 30, 13, (232, 46, 53))
        else:
            text_centered("9 Alps", 230, 150, 80, 30, 20, (237, 141, 45))
    else:
        if trailEquipped:
            text_centered("Unequip", 230, 150, 80, 30, 18, (237, 141, 45))
        else:
            text_centered("Equip", 230, 150, 80, 30, 20, (0, 128, 0) if th else (237, 141, 45))
    blit(trail_img, 240, 76, 60, 60)


def draw_settings():
    screen.fill(bgSettings[bgIndex])
    text("SETTINGS", 150, 60, 40, (255, 255, 255))

    rect((255, 255, 255), 410, 460, 90, 40)
    text_centered("Back", 410, 460, 90, 40, 18, (0, 0, 0))

    rect((220, 220, 220), 110, 120, 270, 50)
    text_centered("Background color", 110, 120, 270, 50, 18, (0, 0, 0))

    rect((220, 220, 220), 110, 180, 270, 50)
    label = "Cords:ON" if showCords else "Cords:OFF"
    text_centered(label, 110, 180, 270, 50, 18, (0, 0, 0))


def draw_paused():
    if trailEquipped:
        draw_trail()

    blit(current_basket_img(), basketx, baskety, 100, 50)
    for apple in applelist:
        apple.display(screen, fx(), fy())
    for booster in boosterList:
        draw_booster(booster)
    show_score()
    show_lives()

    rect((255, 255, 255), 447, 10, 50, 50)
    blit(resumeimg, 448, 11, 50, 50)
    rect((255, 255, 255), 320, 11, 100, 50)
    text_centered("Menu", 320, 11, 100, 50, 20, (0, 0, 0))
    rect((255, 255, 255), 254, 11, 50, 50)
    blit(settings_img, 244, 11, 70, 50)

    if speedBoostTimer > 0:
        text("BOOST READY", 180, 90, 20, (255, 240, 0))


def draw_game_over():
    screen.fill((0, 0, 0))
    text("GAME OVER", 55, 250, 90, (80, 240, 31))
    text("Final Score: " + str(score), 138, 423, 35, (73, 217, 48))
    rect((80, 240, 31), 150, 300, 200, 50)
    text_centered("MENU", 150, 300, 200, 50, 40, (35, 161, 156))


def update_and_draw_play():
    global speed, speedBoostTimer, boosterSpawnCooldown, score, lives, alps, gameState
    # Spawn apples
    if random.randint(1, 57) == 8:
        applelist.append(Apple(difficulty))

    # Spawn boosters
    if boosterSpawnCooldown > 0:
        boosterSpawnCooldown -= 1
    else:
        if random.randint(1, 220) == 12:
            boosterList.append(create_booster())
            boosterSpawnCooldown = 120

    # Speed boost timer
    if speedBoostTimer > 0:
        speedBoostTimer -= 1
        speed = baseSpeed + boostAmount
    else:
        speed = baseSpeed

    # Trail
    if trailEquipped:
        trailPoints.append((basketx + 50, baskety + 30))
        if len(trailPoints) > trailMaxLength:
            trailPoints.pop(0)
        draw_trail()

    blit(current_basket_img(), basketx, baskety, 100, 50)

    # Apples
    for apple in applelist[:]:
        apple.move()
        apple.display(screen, fx(), fy())
        if apple.appley >= 425:
            applelist.remove(apple)
            lives -= 1
        elif (basketx - 49 <= apple.applex <= basketx + 100
              and baskety - 49 <= apple.appley <= baskety):
            applelist.remove(apple)
            score += 1
            if score % 5 == 0 and difficulty == 1:
                alps += 1
            if score % 3 == 0 and difficulty == 3:
                alps += 1
            if score % 2 == 0 and difficulty == 6:
                alps += 1

    # Boosters
    for booster in boosterList[:]:
        booster["y"] += booster["fallSpeed"]
        draw_booster(booster)
        if booster["y"] > 520:
            boosterList.remove(booster)
        elif (basketx - 20 <= booster["x"] <= basketx + 100
              and baskety - 35 <= booster["y"] <= baskety + 20):
            boosterList.remove(booster)
            speedBoostTimer = boostLength

    if speedBoostTimer > 0:
        text("Boost!", 210, 80, 22, (255, 230, 0))

    if lives <= 0:
        gameState = "gameOver"

    show_score()
    show_lives()

    rect((255, 255, 255), 447, 10, 50, 50)
    blit(pauseimg, 448, 11, 50, 50)


# ----------------------------------------------------------------------
# Main frame
# ----------------------------------------------------------------------

def draw():
    global orangeBoughtFlashFrames, pearBoughtFlashFrames, trailBoughtFlashFrames
    mx, my = mouse_base()

    # Background and common HUD (settings/gameOver override with their own fill)
    if gameState not in ("settings", "gameOver"):
        screen.fill(bgColors[bgIndex])
        blit(alpsimg, 220, -50, 200, 200)
        text(":", 345, 36, 20, (48, 217, 205))
        text(str(alps), 357, 36, 20, (48, 217, 205))

    # Flash timers
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

    if showCords:
        text(str(int(mx)) + ", " + str(int(my)), 20, 497, 15, (255, 0, 0))


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            on_resize(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_mouse_click(*event.pos)

    if gameState == "play":
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and basketx >= 0:
            basketx -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and basketx <= 400:
            basketx += speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and baskety <= 450:
            baskety += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and baskety >= 0:
            baskety -= speed

    draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(60)

pygame.quit()
