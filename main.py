import pygame
import random
import sys
import math
import json
import os
import pyperclip
pygame.init()
info = pygame.display.Info()
SW = info.current_w
SH = info.current_h
screen = pygame.display.set_mode(
    (SW, SH), 
    pygame.FULLSCREEN
)
pygame.display.set_caption(
    "Cyber Jumper"
)
SETTINGS = {
    "joystick_size": 1,
    "animations_on": True
}
game_state = "MENU"
current_lang = "RU"
LANGUAGES = ["RU", "EN"]
BG_EURO = (10, 20, 50)
CARD_EURO = (25, 42, 86)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LGRAY = (180, 190, 220)
CYAN = (0, 246, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 230, 0)
PURPLE = (190, 46, 221)
RED = (255, 30, 70)
GOLD = (255, 215, 0)
SAVE_FILE = "cyber_euro_save.json"

def generate_user_id():
    num = random.randint(100000, 999999)
    return f"ID-{num}"

player_data = {
    "user_id": generate_user_id(),
    "gems": 50,
    "coins": 1000,
    "cases": 2,
    "high_score": 0,
    "current_skin": "Обычный куб",
    "owned_skins": ["Обычный куб"],
    "used_promos": [],
    "custom_promos": {},
    "language": "RU"
}

if os.path.exists(SAVE_FILE):
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            player_data = json.load(f)
            if "language" in player_data:
                current_lang = player_data["language"]
            if "custom_promos" not in player_data:
                player_data["custom_promos"] = {}
    except:
        pass

def save_data():
    player_data["language"] = current_lang
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            player_data, 
            f, 
            ensure_ascii=False, 
            indent=4
        )

LOCALIZATION = {
    "RU": {
        "title": "CYBER JUMPER BRIGHT",
        "id": "Профиль:",
        "gems": "💎 Гемы",
        "coins": "Монеты",
        "cases": "📦 Кейсы",
        "play": "ИГРАТЬ",
        "shop": "КОЛЛЕКЦИЯ ГЕРОЕВ",
        "open_cases": "КЕЙС-ЗОНА",
        "promo": "ПРОМОКОДЫ",
        "sett": "НАСТРОЙКИ",
        "lang_lbl": "ЯЗЫК",
        "joy_size": "ДЖОЙСТИК",
        "anim": "АНИМАЦИИ",
        "on": "ВКЛ",
        "off": "ВЫКЛ",
        "back": "В МЕНЮ",
        "enter_promo": "ВВОД КОДА",
        "promo_tip": "Нажмите Ctrl+V для вставки кодов",
        "invalid_promo": "Неверный код!",
        "used_promo": "Уже активирован!",
        "success_promo": "Код активирован успешно!",
        "admin_title": "⚡ АДМИН ПАНЕЛЬ ⚡",
        "admin_gems": "+5000 ГЕМОВ",
        "admin_cases": "+10 КЕЙСОВ",
        "admin_skins": "ОТКРЫТЬ ВСЕ",
        "admin_exit": "ВЫХОД",
        "shop_title": "МАГАЗИН ПЕРСОНАЖЕЙ",
        "balance": "Баланс",
        "select": "ВЫБРАТЬ",
        "selected": "ВЫБРАН",
        "cases_title": "ОТКРЫТИЕ КЕЙСОВ",
        "your_cases": "Кейсы",
        "case_tip": "Нажмите ОТКРЫТЬ ниже",
        "open_btn": "ОТКРЫТЬ",
        "buy_case": "КУПИТЬ КЕЙС (500)",
        "dropped": "ВЫПАЛО",
        "game_over": "КОНЕЦ ИГРЫ",
        "high_score": "РЕКОРД",
        "earned": "ЗАРАБОТАНО",
        "retry": "ПОВТОР",
        "score_lbl": "ОЧКИ",
        "world_lbl": "МИР"
    },
    "EN": {
        "title": "CYBER JUMPER BRIGHT",
        "id": "Profile:",
        "gems": "💎 Gems",
        "coins": "Coins",
        "cases": "📦 Cases",
        "play": "PLAY",
        "shop": "HEROES",
        "open_cases": "CASE ZONE",
        "promo": "PROMOCODES",
        "sett": "SETTINGS",
        "lang_lbl": "LANGUAGE",
        "joy_size": "JOYSTICK",
        "anim": "ANIMATIONS",
        "on": "ON",
        "off": "OFF",
        "back": "BACK",
        "enter_promo": "ENTER CODE",
        "promo_tip": "Press Ctrl+V to paste text",
        "invalid_promo": "Invalid code!",
        "used_promo": "Already used!",
        "success_promo": "Activated!",
        "admin_title": "⚡ ADMIN PANEL ⚡",
        "admin_gems": "+5000 GEMS",
        "admin_cases": "+10 CASES",
        "admin_skins": "UNLOCK ALL",
        "admin_exit": "EXIT",
        "shop_title": "HERO SHOP",
        "balance": "Balance",
        "select": "SELECT",
        "selected": "SELECTED",
        "cases_title": "LUCKY BOXES",
        "your_cases": "Cases",
        "case_tip": "Press OPEN below",
        "open_btn": "OPEN",
        "buy_case": "BUY BOX (500)",
        "dropped": "DROPPED",
        "game_over": "GAME OVER",
        "high_score": "HIGH SCORE",
        "earned": "EARNED",
        "retry": "RETRY",
        "score_lbl": "SCORE",
        "world_lbl": "WORLD"
    }
}
WORLDS = {
    "CYBER": {
        "bg": BG_EURO, 
        "plat": GREEN, 
        "player": CYAN, 
        "name": "NEON METROPOLIS"
    },
    "HELL": {
        "bg": (50, 10, 20), 
        "plat": YELLOW, 
        "player": RED, 
        "name": "INFERNO CRATER"
    },
    "SPACE": {
        "bg": (15, 10, 40), 
        "plat": PURPLE, 
        "player": GREEN, 
        "name": "ORBIT STATION"
    }
}
current_world = "CYBER"

FONT_MENU = pygame.font.Font(None, int(SW * 0.045))
FONT_TITLE = pygame.font.Font(None, int(SW * 0.032))
FONT_SUB = pygame.font.Font(None, int(SW * 0.020))
FONT_BTN = pygame.font.Font(None, int(SW * 0.015))

GRAVITY = 0.4
JUMP_POWER = -14

SKINS = {
    "Обычный куб":  {"price": 0,    "color": CYAN},
    "Неон":         {"price": 100,  "color": GREEN},
    "Пламя":        {"price": 300,  "color": RED},
    "Аметист":      {"price": 500,  "color": PURPLE},
    "Изумруд":      {"price": 800,  "color": (0, 255, 128)},
    "Золото":       {"price": 1200, "color": YELLOW},
    "Самурай":      {"price": 2000, "color": (200, 0, 0)},
    "Кибер Кошка":  {"price": 2500, "color": (255, 0, 128)},
    "Тень":         {"price": 4000, "color": (30, 35, 60)},
    "АДМИН-КУБ":    {"price": 9999, "color": WHITE}
}

promo_input_text = ""
promo_message = ""
promo_message_color = WHITE
case_animation_timer = 0
case_reward_item = ""
case_is_opening = False
admin_id_input = ""
admin_target_found = False
admin_promo_name = ""
admin_promo_reward = 1000
admin_promo_stage = 0  
class Player:
    def __init__(self):
        self.rect = pygame.Rect(
            SW // 2 - 15, 
            SH - 200, 
            30, 
            30
        )
        self.vel_y = 0
        self.spawn_timer = 0.0 if not SETTINGS["animations_on"] else 0.0
        if not SETTINGS["animations_on"]:
            self.spawn_timer = 1.0
        self.is_spawning = SETTINGS["animations_on"]
        self.death_timer = 0.0
        self.is_dying = False
        self.scale_x, self.scale_y = 1.0, 1.0

    def move(self, joystick_x):
        if SETTINGS["animations_on"]:
            if self.is_spawning or self.is_dying: 
                return
        keys = pygame.key.get_pressed()
        kb_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            kb_x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            kb_x = 1
        move_input = joystick_x if joystick_x != 0 else kb_x
        self.rect.x += move_input * (SW * 0.006)
        
        if self.rect.left > SW: 
            self.rect.right = 0
        if self.rect.right < 0: 
            self.rect.left = SW
            
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        if self.rect.y > SH and not self.is_dying:
            if SETTINGS["animations_on"]: 
                self.is_dying = True
            else:
                global game_state
                game_state = "GAMEOVER"

    def update_animations(self):
        if not SETTINGS["animations_on"]:
            self.is_spawning = False
            self.scale_x, self.scale_y = 1.0, 1.0
            return
        if self.is_spawning:
            self.spawn_timer += 0.05
            if self.spawn_timer >= 1.0:
                self.spawn_timer = 1.0
                self.is_spawning = False
            self.scale_x = self.spawn_timer
            self.scale_y = self.spawn_timer
        elif self.is_dying:
            self.death_timer += 0.08
            if self.death_timer >= 1.0:
                global game_state
                game_state = "GAMEOVER"
            self.scale_x = 1.0 + self.death_timer * 2
            self.scale_y = max(0.0, 1.0 - self.death_timer)
    def draw(self):
        self.update_animations()
        if SETTINGS["animations_on"]:
            w = int(30 * self.scale_x)
            h = int(30 * self.scale_y)
            cx, cy = self.rect.center
            draw_rect = pygame.Rect(
                cx - w // 2, 
                cy - h // 2, 
                w, 
                h
            )
        else:
            draw_rect = self.rect
        
        if draw_rect.width > 0 and draw_rect.height > 0:
            skin_name = player_data["current_skin"]
            skin_color = SKINS.get(
                skin_name, 
                {"color": CYAN}
            )["color"]
            pygame.draw.rect(
                screen, 
                skin_color, 
                draw_rect, 
                border_radius=6
            )
            
            if skin_name in [
                "Обычный куб", "Неон", 
                "Аметист", "Изумруд"
            ]:
                pygame.draw.rect(
                    screen, WHITE, 
                    (draw_rect.x + 5, draw_rect.y + 8, 5, 5)
                )
                pygame.draw.rect(
                    screen, WHITE, 
                    (draw_rect.x + 19, draw_rect.y + 8, 5, 5)
                )
                pygame.draw.rect(
                    screen, BLACK, 
                    (draw_rect.x + 6, draw_rect.y + 9, 2, 2)
                )
                pygame.draw.rect(
                    screen, BLACK, 
                    (draw_rect.x + 20, draw_rect.y + 9, 2, 2)
                )
            elif skin_name == "Самурай":
                pygame.draw.rect(
                    screen, RED, 
                    (draw_rect.x, draw_rect.y + 4, draw_rect.width, 5)
                )
                pygame.draw.circle(
                    screen, YELLOW, 
                    (draw_rect.centerx, draw_rect.y + 6), 2
                )
                pygame.draw.rect(
                    screen, WHITE, 
                    (draw_rect.x + 4, draw_rect.y + 12, 6, 2)
                )
                pygame.draw.rect(
                    screen, WHITE, 
                    (draw_rect.x + 19, draw_rect.y + 12, 6, 2)
                )
            elif skin_name == "Кибер Кошка":
                pygame.draw.polygon(
                    screen, skin_color, 
                    [
                        (draw_rect.left, draw_rect.top), 
                        (draw_rect.left + 5, draw_rect.top - 6), 
                        (draw_rect.left + 9, draw_rect.top)
                    ]
                )
                pygame.draw.polygon(
                    screen, skin_color, 
                    [
                        (draw_rect.right, draw_rect.top), 
                        (draw_rect.right - 5, draw_rect.top - 6), 
                        (draw_rect.right - 9, draw_rect.top)
                    ]
                )
            elif skin_name == "Пламя":
                pygame.draw.rect(
                    screen, YELLOW, 
                    (draw_rect.left + 3, draw_rect.top - 4, 3, 5)
                )
                pygame.draw.rect(
                    screen, YELLOW, 
                    (draw_rect.right - 6, draw_rect.top - 4, 3, 5)
                )
            elif skin_name == "Тень":
                pygame.draw.rect(
                    screen, PURPLE, 
                    (draw_rect.x + 5, draw_rect.y + 10, 5, 3)
                )
                pygame.draw.rect(
                    screen, PURPLE, 
                    (draw_rect.x + 19, draw_rect.y + 10, 5, 3)
                )
            elif skin_name == "Золото":
                pygame.draw.rect(
                    screen, BG_EURO, 
                    (draw_rect.x, draw_rect.y + 8, draw_rect.width, 5)
                )
            elif skin_name == "АДМИН-КУБ":
                pygame.draw.rect(
                    screen, GREEN, 
                    (draw_rect.x + 4, draw_rect.y + 8, 6, 2)
                )
                pygame.draw.rect(
                    screen, GREEN, 
                    (draw_rect.x + 19, draw_rect.y + 8, 6, 2)
                )

class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(
            x, 
            y, 
            int(SW * 0.07), 
            int(SH * 0.02)
        )
    def draw(self):
        w_data = WORLDS[current_world]
        pygame.draw.rect(
            screen, 
            w_data["plat"], 
            self.rect, 
            border_radius=4
        )
class TouchJoystick:
    def __init__(self):
        self.update_size()
    def update_size(self):
        self.base_radius = int(SW * 0.03) + SETTINGS["joystick_size"] * 8
        self.stick_radius = self.base_radius // 2
        self.base_pos = [
            self.base_radius + 40, 
            SH - self.base_radius - 40
        ]
        self.stick_pos = list(self.base_pos)
        self.active = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            dist = math.hypot(
                mx - self.base_pos[0], 
                my - self.base_pos[1]
            )
            if dist < self.base_radius: 
                self.active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False
            self.stick_pos = list(self.base_pos)
        if event.type == pygame.MOUSEMOTION and self.active:
            mx, my = event.pos
            dx = mx - self.base_pos[0]
            dy = my - self.base_pos[1]
            dist = math.hypot(dx, dy)
            if dist <= self.base_radius - self.stick_radius:
                self.stick_pos = [mx, my]
            else:
                angle = math.atan2(dy, dx)
                r_limit = self.base_radius - self.stick_radius
                self.stick_pos[0] = self.base_pos[0] + int(
                    math.cos(angle) * r_limit
                )
                self.stick_pos[1] = self.base_pos[1] + int(
                    math.sin(angle) * r_limit
                )
    def get_axis_x(self):
        if not self.active: 
            return 0.0
        dx = self.stick_pos[0] - self.base_pos[0]
        max_limit = self.base_radius - self.stick_radius
        if max_limit > 0:
            return dx / max_limit
        return 0.0
    def draw(self):
        bx = int(self.base_pos[0])
        by = int(self.base_pos[1])
        sx = int(self.stick_pos[0])
        sy = int(self.stick_pos[1])
        pygame.draw.circle(
            screen, CARD_EURO, 
            (bx, by), self.base_radius, 0
        )
        pygame.draw.circle(
            screen, GREEN, 
            (bx, by), self.base_radius, 2
        )
        pygame.draw.circle(
            screen, CYAN, 
            (sx, sy), self.stick_radius
        )

def draw_button(text, x, y, w, h, bg_color, text_color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(
        screen, bg_color, 
        rect, border_radius=12
    )
    b_border = YELLOW if bg_color != GREEN else WHITE
    pygame.draw.rect(
        screen, b_border, 
        rect, 2, border_radius=12
    )
    txt_surf = FONT_BTN.render(
        text, True, text_color
    )
    txt_rect = txt_surf.get_rect(
        center=rect.center
    )
    screen.blit(txt_surf, txt_rect)
    return rect

player = Player()
joystick = TouchJoystick()
platforms = []
score = 0
def generate_platforms(start_y, count=10):
    plat_w = int(SW * 0.07)
    if len(platforms) > 0:
        last_x = platforms[-1].rect.x
        last_y = platforms[-1].rect.y
    else:
        last_x = SW // 2 - 50
        last_y = start_y
        
    for _ in range(count):
        next_y = last_y - random.randint(90, 130)
        min_x = max(0, last_x - 140)
        max_x = min(SW - plat_w, last_x + 140)
        next_x = random.randint(min_x, max_x)
        platforms.append(
            Platform(next_x, next_y)
        )
        last_y = next_y
        last_x = next_x

def reset_game():
    global player, platforms, score, current_world
    player = Player()
    score = 0
    current_world = "CYBER"
    platforms = [
        Platform(SW // 2 - 50, SH - 170)
    ]
    generate_platforms(SH - 170, 15)
    joystick.update_size()

reset_game()
clock = pygame.time.Clock()
while True:
    screen.fill(WORLDS[current_world]["bg"])
    mx, my = pygame.mouse.get_pos()
    click = False
    tx = LOCALIZATION[current_lang]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_data()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                save_data()
                pygame.quit()
                sys.exit()
                
            if game_state == "PROMO":
                if event.key == pygame.K_v and (
                    pygame.key.get_mods() & pygame.KMOD_CTRL
                ):
                    try:
                        promo_input_text += pyperclip.paste().strip()
                    except:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    promo_input_text = promo_input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    click_trigger_promo = True
                else:
                    if len(promo_input_text) < 25:
                        promo_input_text += event.unicode
                        
            elif game_state == "ADMIN" and not admin_target_found:
                if event.key == pygame.K_v and (
                    pygame.key.get_mods() & pygame.KMOD_CTRL
                ):
                    try:
                        admin_id_input += pyperclip.paste().strip()
                    except:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    admin_id_input = admin_id_input[:-1]
                elif event.key == pygame.K_RETURN:
                    click_trigger_admin_id = True
                else:
                    if len(admin_id_input) < 15:
                        admin_id_input += event.unicode

            elif game_state == "CREATE_PROMO" and admin_promo_stage == 0:
                if event.key == pygame.K_BACKSPACE:
                    admin_promo_name = admin_promo_name[:-1]
                elif event.key == pygame.K_RETURN and (
                    admin_promo_name.strip() != ""
                ):
                    admin_promo_stage = 1
                else:
                    if len(admin_promo_name) < 20:
                        admin_promo_name += event.unicode.upper()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True
        if game_state == "GAME":
            joystick.handle_event(event)

    CX = SW // 2
    CY = SH // 2
    if game_state == "MENU":
        title = FONT_MENU.render(tx["title"], True, YELLOW)
        screen.blit(title, title.get_rect(center=(CX, CY - 220)))
        
        p_id = player_data['user_id']
        id_surf = FONT_SUB.render(f"{tx['id']} {p_id}", True, CYAN)
        
        p_g = player_data['gems']
        p_c = player_data['coins']
        p_bx = player_data['cases']
        g_txt = f"{tx['gems']}: {p_g} | 🪙 {tx['coins']}: {p_c} | {tx['cases']}: {p_bx}"
        gems_surf = FONT_SUB.render(g_txt, True, WHITE)
        
        screen.blit(id_surf, id_surf.get_rect(center=(CX, CY - 160)))
        screen.blit(gems_surf, gems_surf.get_rect(center=(CX, CY - 130)))
        
        b_pl = draw_button(tx["play"], CX - 150, CY - 80, 300, 48, GREEN, BLACK)
        b_sh = draw_button(tx["shop"], CX - 150, CY - 20, 300, 48, CARD_EURO, WHITE)
        b_cs = draw_button(tx["open_cases"], CX - 150, CY + 40, 300, 48, CARD_EURO, WHITE)
        b_pr = draw_button(tx["promo"], CX - 150, CY + 100, 300, 48, CARD_EURO, WHITE)
        b_st = draw_button(tx["sett"], CX - 150, CY + 160, 300, 48, CARD_EURO, WHITE)
        
        if click:
            if b_pl.collidepoint(mx, my):
                reset_game()
                game_state = "GAME"
            elif b_sh.collidepoint(mx, my):
                game_state = "SHOP"
            elif b_cs.collidepoint(mx, my):
                game_state = "CASES"
            elif b_pr.collidepoint(mx, my):
                promo_input_text = ""
                promo_message = ""
                game_state = "PROMO"
            elif b_st.collidepoint(mx, my):
                game_state = "SETTINGS"

    elif game_state == "SETTINGS":
        title = FONT_TITLE.render(tx["sett"], True, WHITE)
        screen.blit(title, title.get_rect(center=(CX, CY - 150)))
        
        b_ln = draw_button(f"{tx['lang_lbl']}: {current_lang}", CX - 150, CY - 70, 300, 45, CARD_EURO, YELLOW)
        b_sz = draw_button(f"{tx['joy_size']}: {SETTINGS['joystick_size']}", CX - 150, CY - 10, 300, 45, CARD_EURO, WHITE)
        
        anim_st = tx["on"] if SETTINGS["animations_on"] else tx["off"]
        b_an = draw_button(f"{tx['anim']}: {anim_st}", CX - 150, CY + 50, 300, 45, CARD_EURO, WHITE)
        b_bk = draw_button(tx["back"], CX - 150, CY + 130, 300, 45, RED, WHITE)
        
        if click:
            if b_ln.collidepoint(mx, my):
                idx = LANGUAGES.index(current_lang)
                current_lang = LANGUAGES[(idx + 1) % len(LANGUAGES)]
                save_data()
            elif b_sz.collidepoint(mx, my):
                SETTINGS["joystick_size"] = (SETTINGS["joystick_size"] % 3) + 1
                joystick.update_size()
            elif b_an.collidepoint(mx, my):
                SETTINGS["animations_on"] = not SETTINGS["animations_on"]
            elif b_bk.collidepoint(mx, my):
                game_state = "MENU"

    elif game_state == "PROMO":
        title = FONT_TITLE.render(tx["enter_promo"], True, CYAN)
        screen.blit(title, title.get_rect(center=(CX, CY - 160)))
        
        pygame.draw.rect(screen, CARD_EURO, (CX - 250, CY - 60, 500, 45), border_radius=8)
        pygame.draw.rect(screen, GREEN, (CX - 250, CY - 60, 500, 45), 2, border_radius=8)
        
        txt_surf = FONT_SUB.render(promo_input_text + "|", True, WHITE)
        screen.blit(txt_surf, (CX - 235, CY - 48))
        
        if promo_message:
            msg_surf = FONT_SUB.render(promo_message, True, promo_message_color)
            screen.blit(msg_surf, msg_surf.get_rect(center=(CX, CY + 25)))
            
        b_ac = draw_button("АКТИВИРОВАТЬ", CX - 150, CY + 60, 300, 45, GREEN, BLACK)
        b_bk = draw_button(tx["back"], CX - 150, CY + 120, 300, 45, RED, WHITE)
        
        if (click and b_ac.collidepoint(mx, my)) or 'click_trigger_promo' in locals():
            if 'click_trigger_promo' in locals():
                del click_trigger_promo
            clean_promo = promo_input_text.strip().upper()
            
            if clean_promo in player_data["custom_promos"]:
                if clean_promo not in player_data["used_promos"]:
                    player_data["coins"] += player_data["custom_promos"][clean_promo]
                    player_data["used_promos"].append(clean_promo)
                    promo_message = tx["success_promo"]
                    promo_message_color = GREEN
                    save_data()
                else:
                    promo_message = tx["used_promo"]
                    promo_message_color = RED
            elif clean_promo == "RSMPTOTIP27463JFUDNCF":
                game_state = "ADMIN"
                promo_message = ""
                promo_input_text = ""
                admin_id_input = ""
                admin_target_found = False
            elif clean_promo == "GEMS2026":
                if "GEMS2026" not in player_data["used_promos"]:
                    player_data["gems"] += 500
                    player_data["used_promos"].append("GEMS2026")
                    promo_message = tx["success_promo"]
                    promo_message_color = GREEN
                    save_data()
                else:
                    promo_message = tx["used_promo"]
                    promo_message_color = RED
            else:
                promo_message = tx["invalid_promo"]
                promo_message_color = RED
        if click and b_bk.collidepoint(mx, my):
            game_state = "MENU"

    elif game_state == "ADMIN":
        if not admin_target_found:
            title = FONT_TITLE.render("ВВЕДИТЕ ID И НАЖМИТЕ ПОДТВЕРДИТЬ", True, YELLOW)
            screen.blit(title, title.get_rect(center=(CX, CY - 130)))
            
            pygame.draw.rect(screen, CARD_EURO, (CX - 200, CY - 60, 400, 45), border_radius=8)
            pygame.draw.rect(screen, GREEN, (CX - 200, CY - 60, 400, 45), 2, border_radius=8)
            
            id_surf = FONT_SUB.render(admin_id_input + "|", True, WHITE)
            screen.blit(id_surf, (CX - 185, CY - 48))
            
            b_cf = draw_button("ПОДТВЕРДИТЬ ID", CX - 150, CY + 10, 300, 45, GREEN, BLACK)
            b_bk = draw_button(tx["back"], CX - 150, CY + 70, 300, 45, RED, WHITE)
            
            if (click and b_cf.collidepoint(mx, my)) or 'click_trigger_admin_id' in locals():
                if 'click_trigger_admin_id' in locals():
                    del click_trigger_admin_id
                c_in = admin_id_input.strip().replace(" ", "").upper()
                c_tg = player_data["user_id"].strip().replace(" ", "").upper()
                if c_in == c_tg:
                    admin_target_found = True
                else:
                    admin_id_input = ""
            if click and b_bk.collidepoint(mx, my):
                game_state = "MENU"
        else:
            title = FONT_TITLE.render(f"АДМИН: {player_data['user_id']}", True, GREEN)
            screen.blit(title, title.get_rect(center=(CX, CY - 220)))
            
            b_gm = draw_button(tx["admin_gems"], CX - 210, CY - 80, 200, 45, CARD_EURO, YELLOW)
            b_cs = draw_button(tx["admin_cases"], CX + 10, CY - 80, 200, 45, CARD_EURO, PURPLE)
            b_sk = draw_button(tx["admin_skins"], CX - 210, CY - 20, 420, 45, CARD_EURO, GREEN)
            b_cp = draw_button("🆕 СОЗДАТЬ ПРОМОКОД", CX - 210, CY + 40, 420, 45, GOLD, BLACK)
            b_ex = draw_button(tx["admin_exit"], CX - 150, CY + 120, 300, 45, RED, WHITE)
            
            if click:
                if b_gm.collidepoint(mx, my):
                    player_data["gems"] += 5000
                    player_data["coins"] += 10000
                    save_data()
                elif b_cs.collidepoint(mx, my):
                    player_data["cases"] += 10
                    save_data()
                elif b_sk.collidepoint(mx, my):
                    player_data["owned_skins"] = list(SKINS.keys())
                    save_data()
                elif b_cp.collidepoint(mx, my):
                    game_state = "CREATE_PROMO"
                    admin_promo_name = ""
                    admin_promo_stage = 0
                elif b_ex.collidepoint(mx, my):
                    game_state = "MENU"

    elif game_state == "CREATE_PROMO":
        if admin_promo_stage == 0:
            title = FONT_TITLE.render("НАЗВАНИЕ КОДА", True, CYAN)
            screen.blit(title, title.get_rect(center=(CX, CY - 100)))
            
            pygame.draw.rect(screen, CARD_EURO, (CX - 250, CY - 30, 500, 45), border_radius=8)
            t_surf = FONT_SUB.render(admin_promo_name + "|", True, WHITE)
            screen.blit(t_surf, (CX - 235, CY - 18))
            
            b_bk = draw_button("ОТМЕНА", CX - 150, CY + 100, 300, 45, RED, WHITE)
            if click and b_bk.collidepoint(mx, my):
                game_state = "ADMIN"
        else:
            title = FONT_TITLE.render(f"НАГРАДА ДЛЯ: {admin_promo_name}", True, GOLD)
            screen.blit(title, title.get_rect(center=(CX, CY - 120)))
            
            b_1k = draw_button("+1000 Монет", CX - 150, CY - 50, 300, 45, CARD_EURO, WHITE)
            b_5k = draw_button("+5000 Монет", CX - 150, CY + 10, 300, 45, CARD_EURO, WHITE)
            b_10k = draw_button("+10000 Монет", CX - 150, CY + 70, 300, 45, CARD_EURO, WHITE)
            
            if click:
                if b_1k.collidepoint(mx, my):
                    player_data["custom_promos"][admin_promo_name] = 1000
                    save_data()
                    game_state = "ADMIN"
                elif b_5k.collidepoint(mx, my):
                    player_data["custom_promos"][admin_promo_name] = 5000
                    save_data()
                    game_state = "ADMIN"
                elif b_10k.collidepoint(mx, my):
                    player_data["custom_promos"][admin_promo_name] = 10000
                    save_data()
                    game_state = "ADMIN"
    elif game_state == "SHOP":
        title = FONT_TITLE.render(tx["shop_title"], True, CYAN)
        screen.blit(title, title.get_rect(center=(CX, CY - 240)))
        
        skin_list = list(SKINS.keys())
        idx = 0
        for row in range(2):
            for col in range(5):
                if idx >= len(skin_list):
                    break
                name = skin_list[idx]
                info_skin = SKINS[skin_list[idx]]
                x = CX - 510 + col * 205
                y = CY - 110 + row * 150
                
                pygame.draw.rect(screen, CARD_EURO, (x, y, 190, 130), border_radius=12)
                if player_data["current_skin"] == name:
                    pygame.draw.rect(screen, GREEN, (x, y, 190, 130), 2, border_radius=12)
                    
                pygame.draw.rect(screen, info_skin["color"], (x + 80, y + 12, 30, 30), border_radius=6)
                
                if name in player_data["owned_skins"]:
                    lbl = tx["select"] if player_data["current_skin"] != name else tx["selected"]
                    bg_b = GREEN if player_data["current_skin"] != name else YELLOW
                    s_btn = draw_button(lbl, x + 15, y + 85, 160, 32, bg_b, BLACK)
                    if click and s_btn.collidepoint(mx, my):
                        player_data["current_skin"] = name
                        save_data()
                else:
                    s_btn = draw_button(f"{info_skin['price']} 💎", x + 15, y + 85, 160, 32, PURPLE, WHITE)
                    if click and s_btn.collidepoint(mx, my) and player_data["gems"] >= info_skin["price"]:
                        player_data["gems"] -= info_skin["price"]
                        player_data["owned_skins"].append(name)
                        save_data()
                idx += 1
                
        b_bk = draw_button(tx["back"], CX - 150, CY + 220, 300, 45, RED, WHITE)
        if click and b_bk.collidepoint(mx, my):
            game_state = "MENU"

    elif game_state == "CASES":
        title = FONT_TITLE.render(tx["cases_title"], True, PURPLE)
        screen.blit(title, title.get_rect(center=(CX, CY - 200)))
        
        c_txt = f"{tx['your_cases']}: {player_data['cases']} | {tx['coins']}: {player_data['coins']}"
        c_surf = FONT_SUB.render(c_txt, True, WHITE)
        screen.blit(c_surf, c_surf.get_rect(center=(CX, CY - 150)))
        
        b_by = draw_button(tx["buy_case"], CX - 150, CY + 50, 300, 45, CARD_EURO, GOLD)
        b_op = draw_button(tx["open_btn"], CX - 150, CY + 110, 300, 45, YELLOW, BLACK)
        b_bk = draw_button(tx["back"], CX - 150, CY + 170, 300, 45, RED, WHITE)
        
        if case_is_opening:
            case_animation_timer -= 1
            box_colors = [RED, GREEN, CYAN, YELLOW, PURPLE]
            pygame.draw.rect(screen, random.choice(box_colors), (CX - 20, CY - 30, 40, 40), border_radius=6)
            if case_animation_timer <= 0:
                case_is_opening = False
                if type(case_reward_item) is int:
                    player_data["coins"] += case_reward_item
                elif case_reward_item not in player_data["owned_skins"]:
                    player_data["owned_skins"].append(case_reward_item)
                save_data()
        elif case_reward_item:
            if type(case_reward_item) is int:
                res_txt = f"📦 {tx['dropped']}: +{case_reward_item}"
            else:
                res_txt = f"🔥 {tx['dropped']}: {case_reward_item}"
            res_surf = FONT_SUB.render(res_txt, True, GREEN)
            screen.blit(res_surf, res_surf.get_rect(center=(CX, CY - 10)))
            
        if click and not case_is_opening:
            if b_by.collidepoint(mx, my) and player_data["coins"] >= 500:
                player_data["coins"] -= 500
                player_data["cases"] += 1
                save_data()
            elif b_op.collidepoint(mx, my) and player_data["cases"] > 0:
                player_data["cases"] -= 1
                case_is_opening = True
                case_animation_timer = 60
                if random.random() < 0.85:
                    # ЖЁСТКИЙ ФИКС: Отрезанная строка полностью восстановлена
                    coin_rewards = [50, 100, 250, 500]
                    case_reward_item = random.choice(coin_rewards)
                else:
                    case_reward_item = random.choice(list(SKINS.keys()))
                save_data()
            elif b_bk.collidepoint(mx, my):
                case_reward_item = ""
                game_state = "MENU"
    elif game_state == "GAME":
        axis_x = joystick.get_axis_x()
        player.move(axis_x)
        if player.vel_y > 0:
            for plat in platforms:
                if player.rect.colliderect(plat.rect) and player.rect.bottom <= plat.rect.top + 15:
                    player.vel_y = JUMP_POWER
                    break
        if player.rect.y < CY:
            diff = CY - player.rect.y
            player.rect.y = CY
            score += diff
            for plat in platforms:
                plat.rect.y += diff
        platforms = [p for p in platforms if p.rect.y < SH]
        if len(platforms) < 15:
            generate_platforms(0, 10)
        if score < 5000:
            current_world = "CYBER"
        elif score < 12000:
            current_world = "HELL"
        else:
            current_world = "SPACE"
        for plat in platforms:
            plat.draw()
        player.draw()
        joystick.draw()
        
        score_surf = FONT_SUB.render(f"{tx['score_lbl']}: {int(score)}", True, WHITE)
        world_surf = FONT_SUB.render(f"{tx['world_lbl']}: {WORLDS[current_world]['name']}", True, WORLDS[current_world]['plat'])
        screen.blit(score_surf, (20, 20))
        screen.blit(world_surf, (20, 60))

    elif game_state == "GAMEOVER":
        title = FONT_MENU.render(tx["game_over"], True, RED)
        screen.blit(title, title.get_rect(center=(CX, CY - 100)))
        earned_coins = int(score // 10)
        
        go_txt = f"{tx['high_score']}: {max(player_data['high_score'], int(score))} | {tx['earned']}: +{earned_coins} "
        score_txt = FONT_TITLE.render(go_txt, True, WHITE)
        text_rect = score_txt.get_rect(center=(CX, CY - 20))
        screen.blit(score_txt, text_rect)
        
        if score > player_data["high_score"]:
            player_data["high_score"] = int(score)
        if score > 0:
            player_data["coins"] += earned_coins
            save_data()
            score = 0
            
        coin_x = text_rect.right + 10
        pygame.draw.circle(screen, YELLOW, (coin_x, text_rect.centery), 8)
        pygame.draw.circle(screen, WHITE, (coin_x, text_rect.centery), 8, 1)
        
        b_rs = draw_button(tx["retry"], CX - 150, CY + 50, 300, 48, GREEN, BLACK)
        b_mn = draw_button(tx["back"], CX - 150, CY + 110, 300, 48, CARD_EURO, WHITE)
        if click:
            if b_rs.collidepoint(mx, my):
                reset_game()
                game_state = "GAME"
            elif b_mn.collidepoint(mx, my):
                game_state = "MENU"

    pygame.display.flip()
    clock.tick(60)
