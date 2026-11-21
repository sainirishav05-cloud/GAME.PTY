import pygame
import sys
import random
import winsound  # Windows पर आवाज़ बजाने का सबसे पक्का तरीका

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tractor King Hardcore 3D - Rishav Saini")

GREEN = (34, 139, 34)
ROAD_GRAY = (45, 45, 45)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 20)
YELLOW = (255, 215, 0)
BLUE = (0, 102, 204)
ORANGE = (255, 140, 0)

tractor_x = 380
tractor_y = 420
tractor_speed = 7

enemies = []
spawn_timer = 0
score = 0
game_over = False

clock = pygame.time.Clock()

def reset_game():
    global tractor_x, tractor_y, enemies, score, game_over
    tractor_x = 380
    tractor_y = 420
    enemies.clear()
    score = 0
    game_over = False

running = True
beat_timer = 0

while running:
    screen.fill(GREEN)
    
    # चौड़ी और भारी सड़क
    pygame.draw.rect(screen, ROAD_GRAY, (180, 0, 440, HEIGHT))
    
    road_offset = (pygame.time.get_ticks() // 3) % 60
    for i in range(-60, HEIGHT, 60):
        pygame.draw.rect(screen, WHITE, (395, i + road_offset, 10, 30))
        pygame.draw.rect(screen, YELLOW, (280, i + road_offset, 6, 20))
        pygame.draw.rect(screen, YELLOW, (510, i + road_offset, 6, 20))

    # बैकग्राउंड म्यूजिक/बीट लगातार बजेगी
    beat_timer += 1
    if beat_timer > 35:
        try:
            winsound.Beep(450, 40)  # बैकग्राउंड म्यूजिकल बीट
        except:
            pass
        beat_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if game_over:
                if 300 <= mx <= 500 and 330 <= my <= 380:
                    reset_game()
            else:
                if 40 <= mx <= 140 and 500 <= my <= 580:
                    tractor_x -= 40
                    try: winsound.Beep(800, 30)
                    except: pass
                elif 170 <= mx <= 270 and 500 <= my <= 580:
                    tractor_x += 40
                    try: winsound.Beep(800, 30)
                    except: pass
                elif 650 <= mx <= 750 and 380 <= my <= 460:
                    tractor_y -= 35
                elif 650 <= mx <= 750 and 480 <= my <= 560:
                    tractor_y += 35

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and tractor_x > 190:
            tractor_x -= tractor_speed
        if keys[pygame.K_RIGHT] and tractor_x < 550:
            tractor_x += tractor_speed
        if keys[pygame.K_UP] and tractor_y > 40:
            tractor_y -= tractor_speed
        if keys[pygame.K_DOWN] and tractor_y < HEIGHT - 140:
            tractor_y += tractor_speed

        spawn_timer += 1
        if spawn_timer > 22:
            enemy_x = random.randint(200, 530)
            enemy_y = -120
            enemies.append([enemy_x, enemy_y, random.randint(5, 9)])
            spawn_timer = 0

        tractor_rect = pygame.Rect(tractor_x, tractor_y, 55, 85)

        for enemy in enemies:
            enemy[1] += enemy[2]
            
            pygame.draw.rect(screen, BLUE, (enemy[0], enemy[1], 55, 85), border_radius=10)
            pygame.draw.rect(screen, BLACK, (enemy[0] + 5, enemy[1] + 10, 45, 20))
            pygame.draw.circle(screen, YELLOW, (enemy[0] + 10, enemy[1] + 5), 6)
            pygame.draw.circle(screen, YELLOW, (enemy[0] + 45, enemy[1] + 5), 6)
            
            pygame.draw.rect(screen, BLACK, (enemy[0] - 6, enemy[1] + 15, 6, 18))
            pygame.draw.rect(screen, BLACK, (enemy[0] + 55, enemy[1] + 15, 6, 18))
            pygame.draw.rect(screen, BLACK, (enemy[0] - 6, enemy[1] + 65, 6, 18))
            pygame.draw.rect(screen, BLACK, (enemy[0] + 55, enemy[1] + 65, 6, 18))

            enemy_rect = pygame.Rect(enemy[0], enemy[1], 55, 85)
            
            if tractor_rect.colliderect(enemy_rect):
                game_over = True
                try: winsound.Beep(150, 400) # टक्कर पर भारी आवाज़
                except: pass

        for enemy in enemies[:]:
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                score += 1
                try: winsound.Beep(1200, 50) # कॉइन मिलने पर टन-टन आवाज़
                except: pass

    # ट्रैक्टर और ट्रॉली का मॉडल
    pygame.draw.rect(screen, BROWN, (tractor_x - 12, tractor_y + 50, 60, 50), border_radius=6)
    pygame.draw.circle(screen, BLACK, (tractor_x - 12, tractor_y + 90), 16)
    pygame.draw.circle(screen, BLACK, (tractor_x + 48, tractor_y + 90), 16)
    
    pygame.draw.rect(screen, RED, (tractor_x, tractor_y, 36, 55))
    pygame.draw.rect(screen, YELLOW, (tractor_x - 4, tractor_y - 30, 44, 30), border_radius=5)
    pygame.draw.rect(screen, BLACK, (tractor_x + 12, tractor_y - 42, 8, 15))
    pygame.draw.rect(screen, BLACK, (tractor_x - 10, tractor_y - 10, 56, 8))
    
    pygame.draw.circle(screen, BLACK, (tractor_x - 8, tractor_y - 18), 11)
    pygame.draw.circle(screen, BLACK, (tractor_x + 44, tractor_y - 18), 11)
    pygame.draw.circle(screen, BLACK, (tractor_x - 12, tractor_y + 28), 18)
    pygame.draw.circle(screen, BLACK, (tractor_x + 48, tractor_y + 28), 18)

    # टच बटंस
    pygame.draw.rect(screen, YELLOW, (40, 500, 100, 75), border_radius=15)
    pygame.draw.rect(screen, YELLOW, (170, 500, 100, 75), border_radius=15)
    pygame.draw.rect(screen, ORANGE, (650, 380, 100, 75), border_radius=15)
    pygame.draw.rect(screen, RED, (650, 480, 100, 75), border_radius=15)

    font_btn = pygame.font.SysFont(None, 24)
    screen.blit(font_btn.render("LEFT", True, BLACK), (68, 528))
    screen.blit(font_btn.render("RIGHT", True, BLACK), (192, 528))
    screen.blit(font_btn.render("RACE+", True, WHITE), (672, 408))
    screen.blit(font_btn.render("BRAKE-", True, WHITE), (665, 508))

    font = pygame.font.SysFont(None, 28)
    screen.blit(font.render(f"Rishav Saini Tractor King | Coins: {score}", True, WHITE), (20, 20))
    screen.blit(font.render(f"SPEED: {tractor_speed * 20} KM/H", True, YELLOW), (20, 55))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        go_font = pygame.font.SysFont(None, 52)
        over_text = go_font.render("CRASHED! KHATAM GAME", True, RED)
        screen.blit(over_text, (180, 230))

        score_text = font.render(f"Total Coins Collected: {score}", True, YELLOW)
        screen.blit(score_text, (280, 290))

        pygame.draw.rect(screen, GREEN, (300, 330, 200, 50), border_radius=10)
        btn_text = font.render("PLAY AGAIN", True, WHITE)
        screen.blit(btn_text, (340, 345))

    pygame.display.flip()
    clock.tick(60)
