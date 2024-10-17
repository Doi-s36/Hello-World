import pygame
import sys
import random
from pygame.locals import *

# 初期設定
pygame.init()

# 定数定義
SCREEN_WIDTH = 5 * 50  # ゲーム盤の横幅（5マス * 1マスの幅）
SCREEN_HEIGHT = 12 * 50  # ゲーム盤の縦幅（12マス * 1マスの高さ）
PLAYER_SIZE = 50  # プレイヤーのサイズ
ENEMY_SIZE = 25  # 敵のサイズ（プレイヤーの半分）
BULLET_SIZE = 12  # 弾のサイズ
FPS = 60  # ゲームのFPS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER_SPEED = 1  # プレイヤーの移動速度（1マスずつ）

# ゲーム画面の設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('敵の弾を避けるゲーム')

# ゲームオブジェクトの初期位置設定
player_x = 2 * PLAYER_SIZE  # プレイヤーの初期X座標
player_y = 10 * PLAYER_SIZE  # プレイヤーの初期Y座標
player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

# 敵の初期位置設定
enemies = []
for i in range(5):
    enemy_x = i * SCREEN_WIDTH // 5 + (SCREEN_WIDTH // 5 - ENEMY_SIZE) // 2
    enemy_y = 1 * PLAYER_SIZE + (PLAYER_SIZE - ENEMY_SIZE) // 2
    enemies.append(pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE))

# 弾の初期設定
enemy_bullet = None  # 敵の弾のRectオブジェクト
bullet_speed = 13  # 弾の速度
bullet_active = False  # 弾が発射されているかどうか
last_bullet_time = 0  # 前の弾が発射された時間
bullet_interval = 1000  # 弾の発射間隔（ミリ秒）
bullet_rect = pygame.Rect(0, 0, BULLET_SIZE, BULLET_SIZE)

# タイマーの初期設定
game_font = pygame.font.SysFont(None, 48)  # フォントの設定
start_ticks = pygame.time.get_ticks()  # ゲーム開始時刻を取得

# メインループ
def main_loop():
    global player_x, bullet_active, enemy_bullet, last_bullet_time

    while True:
        screen.fill(BLACK)  # 画面を黒色で塗りつぶす

        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if player_x > 0:
                        player_x -= PLAYER_SIZE  # 左に1マス移動
                elif event.key == K_RIGHT:
                    if player_x < SCREEN_WIDTH - PLAYER_SIZE:
                        player_x += PLAYER_SIZE  # 右に1マス移動

        # プレイヤーのRectオブジェクトを更新
        player_rect.topleft = (player_x, player_y)

        # プレイヤーの描画
        pygame.draw.rect(screen, WHITE, player_rect)

        # 敵の描画
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # すべてのマス目の枠を描画
        for row in range(12):
            for col in range(5):
                pygame.draw.rect(screen, WHITE, (col * 50, row * 50, 50, 50), 1)

        # タイマーの計算と表示
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        timer_text = game_font.render(str(60 - seconds), True, WHITE)
        screen.blit(timer_text, (10, 10))

        # 敵の弾の挙動
        current_time = pygame.time.get_ticks()
        if not bullet_active and (current_time - last_bullet_time > bullet_interval):
            enemy_index = random.randint(0, len(enemies) - 1)
            enemy_bullet = pygame.Rect(enemies[enemy_index].centerx - BULLET_SIZE // 2, enemies[enemy_index].bottom, BULLET_SIZE, BULLET_SIZE)
            bullet_active = True
            last_bullet_time = current_time

        if bullet_active:
            pygame.draw.ellipse(screen, RED, enemy_bullet)
            enemy_bullet.y += bullet_speed

            # 敵の弾が画面外に出たら非アクティブにする
            if enemy_bullet.top > SCREEN_HEIGHT:
                bullet_active = False

        # 当たり判定
        if enemy_bullet is not None and isinstance(enemy_bullet, pygame.Rect):
            if player_rect.colliderect(enemy_bullet):
                game_over()

        # ゲームクリア判定
        if seconds >= 60:
            game_clear()

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

# ゲームオーバー時の処理
def game_over():
    screen.fill(BLACK)
    game_over_text = game_font.render("GAME OVER", True, WHITE)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# ゲームクリア時の処理
def game_clear():
    screen.fill(BLACK)
    game_clear_text = game_font.render("GAME CLEAR", True, WHITE)
    text_rect = game_clear_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(game_clear_text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# ゲームの実行
if __name__ == "__main__":
    main_loop()
