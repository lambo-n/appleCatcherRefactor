import pygame
import sys
import random
import os
from apple import Apple


class AppleCatcher:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        pygame.display.set_caption("Apple Catcher")
        self.clock = pygame.time.Clock()

        self.alpsimg = self._load_img("pixil-frame-0 (6).png")
        self.pauseimg = self._load_img("pause.png")
        self.heart = self._load_img("heartemoji.png")
        self.resumeimg = self._load_img("resume.png")
        self.basket = self._load_img("download__4_-removebg-preview.png")
        self.orange = self._load_img("ORANGE.png")
        self.pear = self._load_img("PEAR.png")
        self.settings_img = self._load_img("settings.png")
        self.trail_img = self._load_img("trail.png")

        self.basketx = 191
        self.baskety = 220
        self.applelist = []
        self.score = 0
        self.lives = 3
        self.difficulty = 3
        self.gameState = "menu"
        self.previousState = "menu"
        self.alps = 100
        self.speed = 9
        self.baseSpeed = 9
        self.boosterList = []
        self.speedBoostTimer = 0
        self.boostAmount = 5
        self.boostLength = 150
        self.boosterSpawnCooldown = 0
        self.trailPoints = []
        self.trailMaxLength = 30
        self.save = False
        self.saveLevel = 1
        self.showCords = True

        self.bgColors = [
            (21, 39, 237), (219, 98, 22), (56, 217, 75), (245, 232, 93),
            (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255),
            (255, 165, 0), (128, 0, 128), (255, 192, 203), (165, 42, 42),
            (0, 128, 0), (0, 0, 128), (0, 128, 128), (128, 128, 0), (128, 128, 128),
        ]
        self.bgIndex = 0
        self.bgSettings = [
            (30, 30, 30), (219, 98, 22), (56, 217, 75), (245, 232, 93),
            (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255),
            (255, 165, 0), (128, 0, 128), (255, 192, 203), (165, 42, 42),
            (0, 128, 0), (0, 0, 128), (0, 128, 128), (128, 128, 0), (128, 128, 128),
        ]

        self.orangeOwned = False
        self.orangeEquipped = False
        self.orangeBoughtFlashMax = 45
        self.orangeBoughtFlashFrames = 0

        self.pearOwned = False
        self.pearEquipped = False
        self.pearBoughtFlashMax = 45
        self.pearBoughtFlashFrames = 0

        self.trailOwned = False
        self.trailEquipped = False
        self.trailBoughtFlashMax = 45
        self.trailBoughtFlashFrames = 0

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _load_img(self, filename):
        path = os.path.join("assets", filename)
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception:
            return None

    def _blit(self, img, x, y, w, h):
        if img is None:
            return
        scaled = pygame.transform.scale(img, (int(w), int(h)))
        self.screen.blit(scaled, (int(x), int(y)))

    def _text(self, msg, x, y, size, color):
        font = pygame.font.Font(None, size)
        surf = font.render(str(msg), True, color)
        # y is baseline in Processing; subtract ascent to convert to top-left
        self.screen.blit(surf, (int(x), int(y) - font.get_ascent()))

    def _rect(self, color, x, y, w, h):
        pygame.draw.rect(self.screen, color, (int(x), int(y), int(w), int(h)))

    def _text_centered(self, msg, rx, ry, rw, rh, size, color):
        font = pygame.font.Font(None, size)
        surf = font.render(str(msg), True, color)
        text_rect = surf.get_rect(center=(int(rx + rw / 2), int(ry + rh / 2)))
        self.screen.blit(surf, text_rect)

    def _ellipse(self, color, cx, cy, w, h):
        pygame.draw.ellipse(
            self.screen, color,
            (int(cx - w / 2), int(cy - h / 2), int(w), int(h)),
        )

    # ------------------------------------------------------------------
    # Game helpers
    # ------------------------------------------------------------------

    def current_basket_img(self):
        if self.pearEquipped:
            return self.pear
        if self.orangeEquipped:
            return self.orange
        return self.basket

    def create_booster(self):
        return {"x": random.randint(30, 470), "y": -20, "size": 40, "fallSpeed": 4}

    def draw_booster(self, booster):
        self._ellipse((255, 230, 0), booster["x"], booster["y"], booster["size"], booster["size"])
        self._text("S", booster["x"] - 5, booster["y"] + 6, 18, (0, 120, 255))

    def draw_trail(self):
        surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        surf.fill((237, 9, 9, 70))
        for (x, y) in self.trailPoints:
            self.screen.blit(surf, (x - 5, y - 5))

    def show_score(self):
        self._text("Score: " + str(self.score), 41, 38, 25, (255, 255, 255))

    def show_lives(self):
        hx = 330
        for _ in range(self.lives):
            self._blit(self.heart, hx, 425, 70, 50)
            hx += 50

    def start_game(self, level):
        if level == 1:
            self.difficulty = 1
            self.baseSpeed = 9
            self.saveLevel = 1
        elif level == 2:
            self.difficulty = 3
            self.baseSpeed = 9
            self.saveLevel = 2
        elif level == 3:
            self.difficulty = 6
            self.baseSpeed = 11
            self.saveLevel = 3
        self.speed = self.baseSpeed
        self.speedBoostTimer = 0
        self.boosterList = []
        self.applelist = []
        self.score = 0
        self.lives = 3
        self.basketx = 191
        self.baskety = 220
        self.gameState = "play"

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def handle_keydown(self, event):
        k = event.key
        gs = self.gameState

        if gs == "menu":
            if k == pygame.K_1:
                self.start_game(1)
            elif k == pygame.K_2:
                self.start_game(2)
            elif k == pygame.K_3:
                self.start_game(3)
            elif k == pygame.K_BACKQUOTE:
                self.gameState = "shop"
            elif k == pygame.K_s:
                self.gameState = "settings"
            elif k == pygame.K_c:
                self.gameState = "paused"

        elif gs == "shop":
            if k in (pygame.K_t, pygame.K_b):
                self.gameState = "menu"

        elif gs == "settings":
            if k == pygame.K_b:
                self.gameState = "menu"
            elif k == pygame.K_c:
                self.showCords = False
            elif k == pygame.K_g:
                self.bgIndex = (self.bgIndex + 1) % len(self.bgColors)

        elif gs == "paused":
            if k == pygame.K_q:
                self.gameState = "play"
            elif k == pygame.K_b:
                self.gameState = "menu"
            elif k == pygame.K_s:
                self.gameState = "settings"

        elif gs == "play":
            if k == pygame.K_BACKQUOTE:
                self.gameState = "paused"

        elif gs == "gameOver":
            if k == pygame.K_SPACE:
                self.gameState = "menu"

    def handle_mouse_click(self, mx, my):
        gs = self.gameState

        # Pause / resume button (play & paused states)
        if 447 <= mx <= 497 and 10 <= my <= 60:
            if gs == "play":
                self.gameState = "paused"
                return
            if gs == "paused":
                self.gameState = "play"
                return

        # Menu button while paused
        if 320 <= mx <= 420 and 11 <= my <= 61:
            if gs == "paused":
                self.gameState = "menu"
                self.save = True
                return

        # Settings button while paused
        if gs == "paused" and 244 <= mx <= 314 and 10 <= my <= 61:
            self.previousState = "paused"
            self.gameState = "settings"
            return

        if gs == "settings":
            if 411 <= mx <= 498 and 461 <= my <= 500:
                self.gameState = self.previousState
                return
            if 112 <= mx <= 378 and 123 <= my <= 172:
                self.bgIndex = (self.bgIndex + 1) % len(self.bgColors)
                return
            if 110 <= mx <= 382 and 182 <= my <= 231:
                self.showCords = not self.showCords
                return

        if gs == "menu":
            if 75 <= mx <= 175 and 200 <= my <= 250:
                self.start_game(1)
                return
            if 200 <= mx <= 300 and 200 <= my <= 250:
                self.start_game(2)
                return
            if 325 <= mx <= 425 and 200 <= my <= 250:
                self.start_game(3)
                return
            if 200 <= mx <= 300 and 350 <= my <= 400:
                self.gameState = "shop"
                return
            if 0 <= mx <= 50 and 0 <= my <= 50:
                self.previousState = "menu"
                self.gameState = "settings"
                return
            if 51 <= mx <= 148 and 0 <= my <= 50 and self.save:
                self.gameState = "paused"
                return

        if gs == "gameOver":
            if 150 <= mx <= 325 and 300 <= my <= 350:
                self.save = False
                self.applelist = []
                self.boosterList = []
                self.score = 0
                self.lives = 3
                self.gameState = "menu"
                self.speedBoostTimer = 0
                self.speed = self.baseSpeed
                self.basketx = 191
                self.baskety = 220
                self.trailPoints = []
                return

        if gs == "shop":
            if 20 <= mx <= 90 and 433 <= my <= 493:
                self.gameState = "menu"
                return
            if 10 <= mx <= 90 and 150 <= my <= 180:
                if self.orangeBoughtFlashFrames > 0:
                    return
                if not self.orangeOwned:
                    if self.alps >= 6:
                        self.orangeOwned = True
                        self.orangeEquipped = False
                        self.alps -= 6
                        self.orangeBoughtFlashFrames = self.orangeBoughtFlashMax
                    return
                self.orangeEquipped = not self.orangeEquipped
                if self.orangeEquipped:
                    self.pearEquipped = False
                return
            if 121 <= mx <= 199 and 150 <= my <= 180:
                if self.pearBoughtFlashFrames > 0:
                    return
                if not self.pearOwned:
                    if self.alps >= 8:
                        self.pearOwned = True
                        self.alps -= 8
                        self.pearBoughtFlashFrames = self.pearBoughtFlashMax
                    return
                self.pearEquipped = not self.pearEquipped
                if self.pearEquipped:
                    self.orangeEquipped = False
                return
            if 231 <= mx <= 308 and 150 <= my <= 180:
                if self.trailBoughtFlashFrames > 0:
                    return
                if not self.trailOwned:
                    if self.alps >= 9:
                        self.trailOwned = True
                        self.alps -= 9
                        self.trailBoughtFlashFrames = self.trailBoughtFlashMax
                    return
                self.trailEquipped = not self.trailEquipped
                self.trailPoints = []
                return

    # ------------------------------------------------------------------
    # Drawing per state
    # ------------------------------------------------------------------

    def draw_menu(self):
        self._rect((255, 255, 255), 75, 200, 100, 50)
        self._rect((255, 255, 255), 200, 200, 100, 50)
        self._rect((255, 255, 255), 325, 200, 100, 50)
        self._rect((255, 255, 255), 200, 350, 100, 50)
        self._rect((255, 255, 255), 0, 0, 50, 50)
        self._blit(self.settings_img, -10, 0, 70, 50)

        c = (31, 150, 255)
        self._text_centered("Level 1", 75, 200, 100, 50, 20, c)
        self._text_centered("Level 2", 200, 200, 100, 50, 20, c)
        self._text_centered("Level 3", 325, 200, 100, 50, 20, c)
        self._text_centered("Shop", 200, 350, 100, 50, 20, c)

        if self.save:
            self._rect((255, 255, 255), 50, 0, 100, 50)
            self._text_centered("Continue", 50, 0, 100, 25, 17, (31, 150, 25))
            self._text_centered("Level " + str(self.saveLevel), 50, 25, 100, 25, 17, (31, 150, 25))

    def draw_shop(self):
        mx, my = pygame.mouse.get_pos()

        self._blit(self.alpsimg, 330, 387, 200, 200)
        self._text(":", 455, 470, 20, (48, 217, 205))
        self._text(str(self.alps), 465, 472, 20, (48, 217, 205))

        self._rect((255, 255, 255), 0, 0, 500, 50)
        self._text_centered("WELCOME TO THE SHOP", 0, 0, 500, 50, 40, (237, 22, 22))

        self._rect((255, 255, 255), 0, 430, 100, 69)
        self._text_centered("Back To Menu", 0, 430, 100, 69, 14, (237, 22, 22))

        # --- Orange ---
        self._rect((255, 255, 255), 10, 70, 80, 70)
        self._rect((255, 255, 255), 10, 150, 80, 30)
        oh = 10 <= mx <= 90 and 150 <= my <= 180
        if self.orangeBoughtFlashFrames > 0:
            self._text_centered("Bought", 10, 150, 80, 30, 20, (0, 128, 0))
        elif not self.orangeOwned:
            if oh:
                if self.alps >= 6:
                    self._text_centered("Buy", 10, 150, 80, 30, 20, (0, 128, 0))
                else:
                    self._text_centered("Not enough", 10, 150, 80, 30, 13, (232, 46, 53))
            else:
                self._text_centered("6 Alps", 10, 150, 80, 30, 20, (237, 141, 45))
        else:
            if self.orangeEquipped:
                self._text_centered("Unequip", 10, 150, 80, 30, 18, (237, 141, 45))
            else:
                self._text_centered("Equip", 10, 150, 80, 30, 20, (0, 128, 0) if oh else (237, 141, 45))
        self._blit(self.orange, 20, 70, 60, 60)

        # --- Pear ---
        self._rect((255, 255, 255), 120, 70, 80, 70)
        self._rect((255, 255, 255), 120, 150, 80, 30)
        ph = 121 <= mx <= 199 and 150 <= my <= 180
        if self.pearBoughtFlashFrames > 0:
            self._text_centered("Bought", 120, 150, 80, 30, 20, (0, 128, 0))
        elif not self.pearOwned:
            if ph:
                if self.alps >= 8:
                    self._text_centered("Buy", 120, 150, 80, 30, 20, (0, 128, 0))
                else:
                    self._text_centered("Not enough", 120, 150, 80, 30, 13, (232, 46, 53))
            else:
                self._text_centered("8 Alps", 120, 150, 80, 30, 20, (237, 141, 45))
        else:
            if self.pearEquipped:
                self._text_centered("Unequip", 120, 150, 80, 30, 18, (237, 141, 45))
            else:
                self._text_centered("Equip", 120, 150, 80, 30, 20, (0, 128, 0) if ph else (237, 141, 45))
        self._blit(self.pear, 121, 64, 80, 80)

        # --- Trail ---
        self._rect((255, 255, 255), 230, 71, 80, 70)
        self._rect((255, 255, 255), 230, 150, 80, 30)
        th = 231 <= mx <= 308 and 150 <= my <= 180
        if self.trailBoughtFlashFrames > 0:
            self._text_centered("Bought", 230, 150, 80, 30, 20, (0, 128, 0))
        elif not self.trailOwned:
            if th:
                if self.alps >= 9:
                    self._text_centered("Buy", 230, 150, 80, 30, 20, (0, 128, 0))
                else:
                    self._text_centered("Not enough", 230, 150, 80, 30, 13, (232, 46, 53))
            else:
                self._text_centered("9 Alps", 230, 150, 80, 30, 20, (237, 141, 45))
        else:
            if self.trailEquipped:
                self._text_centered("Unequip", 230, 150, 80, 30, 18, (237, 141, 45))
            else:
                self._text_centered("Equip", 230, 150, 80, 30, 20, (0, 128, 0) if th else (237, 141, 45))
        self._blit(self.trail_img, 240, 76, 60, 60)

    def draw_settings(self):
        self.screen.fill(self.bgSettings[self.bgIndex])
        self._text("SETTINGS", 150, 60, 40, (255, 255, 255))

        self._rect((255, 255, 255), 410, 460, 90, 40)
        self._text_centered("Back", 410, 460, 90, 40, 18, (0, 0, 0))

        self._rect((220, 220, 220), 110, 120, 270, 50)
        self._text_centered("Background color", 110, 120, 270, 50, 18, (0, 0, 0))

        self._rect((220, 220, 220), 110, 180, 270, 50)
        label = "Cords:ON" if self.showCords else "Cords:OFF"
        self._text_centered(label, 110, 180, 270, 50, 18, (0, 0, 0))

    def draw_paused(self):
        if self.trailEquipped:
            self.draw_trail()

        self._blit(self.current_basket_img(), self.basketx, self.baskety, 100, 50)
        for apple in self.applelist:
            apple.display(self.screen)
        for booster in self.boosterList:
            self.draw_booster(booster)
        self.show_score()
        self.show_lives()

        self._rect((255, 255, 255), 447, 10, 50, 50)
        self._blit(self.resumeimg, 448, 11, 50, 50)
        self._rect((255, 255, 255), 320, 11, 100, 50)
        self._text_centered("Menu", 320, 11, 100, 50, 20, (0, 0, 0))
        self._rect((255, 255, 255), 254, 11, 50, 50)
        self._blit(self.settings_img, 244, 11, 70, 50)

        if self.speedBoostTimer > 0:
            self._text("BOOST READY", 180, 90, 20, (255, 240, 0))

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))
        self._text("GAME OVER", 20, 250, 75, (80, 240, 31))
        self._text("Final Score: " + str(self.score), 138, 423, 35, (73, 217, 48))
        self._rect((80, 240, 31), 150, 300, 200, 50)
        self._text_centered("MENU", 150, 300, 200, 50, 40, (35, 161, 156))

    def update_and_draw_play(self):
        # Spawn apples
        if random.randint(1, 57) == 8:
            self.applelist.append(Apple(self.difficulty))

        # Spawn boosters
        if self.boosterSpawnCooldown > 0:
            self.boosterSpawnCooldown -= 1
        else:
            if random.randint(1, 220) == 12:
                self.boosterList.append(self.create_booster())
                self.boosterSpawnCooldown = 120

        # Speed boost timer
        if self.speedBoostTimer > 0:
            self.speedBoostTimer -= 1
            self.speed = self.baseSpeed + self.boostAmount
        else:
            self.speed = self.baseSpeed

        # Trail
        if self.trailEquipped:
            self.trailPoints.append((self.basketx + 50, self.baskety + 30))
            if len(self.trailPoints) > self.trailMaxLength:
                self.trailPoints.pop(0)
            self.draw_trail()

        self._blit(self.current_basket_img(), self.basketx, self.baskety, 100, 50)

        # Apples
        for apple in self.applelist[:]:
            apple.move()
            apple.display(self.screen)
            if apple.appley >= 425:
                self.applelist.remove(apple)
                self.lives -= 1
            elif (self.basketx - 49 <= apple.applex <= self.basketx + 100
                  and self.baskety - 49 <= apple.appley <= self.baskety):
                self.applelist.remove(apple)
                self.score += 1
                if self.score % 5 == 0 and self.difficulty == 1:
                    self.alps += 1
                if self.score % 3 == 0 and self.difficulty == 3:
                    self.alps += 1
                if self.score % 2 == 0 and self.difficulty == 6:
                    self.alps += 1

        # Boosters
        for booster in self.boosterList[:]:
            booster["y"] += booster["fallSpeed"]
            self.draw_booster(booster)
            if booster["y"] > 520:
                self.boosterList.remove(booster)
            elif (self.basketx - 20 <= booster["x"] <= self.basketx + 100
                  and self.baskety - 35 <= booster["y"] <= self.baskety + 20):
                self.boosterList.remove(booster)
                self.speedBoostTimer = self.boostLength

        if self.speedBoostTimer > 0:
            self._text("Boost!", 210, 80, 22, (255, 230, 0))

        if self.lives <= 0:
            self.gameState = "gameOver"

        self.show_score()
        self.show_lives()

        self._rect((255, 255, 255), 447, 10, 50, 50)
        self._blit(self.pauseimg, 448, 11, 50, 50)

    # ------------------------------------------------------------------
    # Main frame
    # ------------------------------------------------------------------

    def draw(self):
        mx, my = pygame.mouse.get_pos()

        # Background and common HUD (settings/gameOver override with their own fill)
        if self.gameState not in ("settings", "gameOver"):
            self.screen.fill(self.bgColors[self.bgIndex])
            self._blit(self.alpsimg, 220, -50, 200, 200)
            self._text(":", 345, 36, 20, (48, 217, 205))
            self._text(str(self.alps), 357, 36, 20, (48, 217, 205))

        # Flash timers
        if self.orangeBoughtFlashFrames > 0:
            self.orangeBoughtFlashFrames -= 1
        if self.pearBoughtFlashFrames > 0:
            self.pearBoughtFlashFrames -= 1
        if self.trailBoughtFlashFrames > 0:
            self.trailBoughtFlashFrames -= 1

        if self.gameState == "menu":
            self.draw_menu()
        elif self.gameState == "shop":
            self.draw_shop()
        elif self.gameState == "settings":
            self.draw_settings()
        elif self.gameState == "paused":
            self.draw_paused()
        elif self.gameState == "gameOver":
            self.draw_game_over()
        elif self.gameState == "play":
            self.update_and_draw_play()

        if self.showCords:
            self._text(str(mx) + ", " + str(my), 20, 497, 15, (255, 0, 0))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(*event.pos)

            if self.gameState == "play":
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.basketx >= 0:
                    self.basketx -= self.speed
                if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.basketx <= 400:
                    self.basketx += self.speed
                if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.baskety <= 450:
                    self.baskety += self.speed
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.baskety >= 0:
                    self.baskety -= self.speed

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    AppleCatcher().run()
