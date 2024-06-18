import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1800, 800
os.chdir(os.path.dirname(os.path.abspath(__file__)))

mov_dic = {  # 移動量辞書
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0, +5), 
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect　または　爆弾Rect
    戻り値：真理値タプル（横方向、縦方向）
    画面内ならTrue　画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def kk_swicth(yoko, tate):  # こうかとんの向きを変える関数
    """
    引数：縦方向、横方向
    戻り値：こうかとんsurface
    """
    if (yoko, tate) == (0, 0):  # 何も押していないとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)
    elif (yoko, tate) == (+5, 0):  # 右を押しているとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)
    elif (yoko, tate) == (+5, -5):  # 右と上を押しているとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)
    elif (yoko, tate) == (0, -5):  # 上を押しているとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)
    elif (yoko, tate) == (+5, +5):  # 右と下を押しているとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)
    elif (yoko, tate) == (0, +5):  # 下を押しているとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)
    elif (yoko, tate) == (-5, 0):  # 左を押しているとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    elif (yoko, tate) == (-5, -5):  # 左と上を押したとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0)
    elif (yoko, tate) == (-5, +5):  # 左と下を押したとき
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0)
    return kk_img   


# def accs_tpl():  # 演習問題２途中
#     accs = [a for a in range(1, 11)]  # 加速度のリスト
#     bb_imgs = []
#     for r in range(1, 11):
#         bb_img = pg.surface((20*r, 20*r))
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
#         bb_imgs.append()


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    bb_img = pg.Surface((20, 20))  # 1辺が20のからのsurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 空のsurfaceに赤い円を描く
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in mov_dic.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                kk_img = kk_swicth(sum_mv[0], sum_mv[1])
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
