import os
import pygame

pygame.init() # 초기화

# 화면크기
screen_width = 640 # 가로
screen_height = 480 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀
pygame.display.set_caption("설이와 지미")

# FPS
clock = pygame.time.Clock()

# 1. 사용자 게임 초기화 (배경 화면, game image, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # image 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지 높이 위에 캐릭터를 두기 위에 사용


# 캐릭터(스프라이트) 불러오기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size # 이미지의 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로크기
character_height = character_size[1] # 캐릭터의 세로크기
character_x_pos = (screen_width / 2) - (character_width /2 ) # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height - stage_height # 화면 세로 크기 가장 아래에 캐릭터가 위치

# 이동할 좌표
to_x = 0
to_y = 0

# 이동 속도
character_speed = 0.6


# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러 발 발사 가능
weapons = []

weapon_speed = 5

# 공 만들기(4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png")),]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3에 해당하는 값


balls = []
# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50, #공의 x 좌표
    "pos_y" : 50, #공의 y 좌표
    "img_idx" : 0, #공의 이미지 인덱스
    "to_x": 3, #x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로
    "to_y": -6, # y축 이동방향
    "init_spd_y": ball_speed_y[0]})# y 최초 속도

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# 적 캐릭터

# enemy = pygame.image.load("C:\\Users\\JUNGWON-KYG\\Desktop\\Pythonworkspace\\pygame_basic\\character.png")
# enemy_size = enemy.get_rect().size # 이미지의 크기를 구해옴
# enemy_width = enemy_size[0] # 캐릭터의 가로크기
# enemy_height = enemy_size[1] # 캐릭터의 세로크기
# enemy_x_pos = (screen_width / 2) - (enemy_width / 2) # 화면 가로의 절반 크기에 해당하는 곳에 위치
# enemy_y_pos = (screen_height / 2) - (enemy_height / 2) # 화면 세로 크기 가장 아래에 캐릭터가 위치

# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)

# 총 시간
total_time = 100

# 시간계산
start_ticks = pygame.time.get_ticks() # 시작 tick을 받아옴



# 이벤트 루프
running = True # 게임진행중?
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수를 설정

    print("fps : " + str(clock.get_fps()))

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): # 어떤 이벤트가 발생했나?
        if event.type == pygame.QUIT: # 창이 닫혔나?
            running = False # 게임진행아님

        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:
                to_x -= character_speed 
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_SPACE: #무기발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

                for weapon_x_pos, weapon_y_pos in weapons:
                    screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
            # elif event.key == pygame.K_UP:
            #     to_y -= character_speed
            # elif event.key == pygame.K_DOWN:
            #     to_y += character_speed

        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT or event.key  ==  pygame.K_RIGHT:
        #         to_x = 0
        #     elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #         to_y = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

# 3. 게임 캐릭터 위치 정의
    character_x_pos += to_x
    # 가로 경계값 처리(캐릭터가 화면 밖으로 못나가게 하는트리거)
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    #천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        
        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 그외의 모든 경우에는 속도 증가
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    # 세로 경계값 처리
    # if character_y_pos < 0:
    #     character_y_pos = 0
    # elif character_y_pos > screen_height - character_height:
    #     character_y_pos = screen_height - character_height

    # 4. 충돌 처리
    
    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            print("무기와 공의 충돌")
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크 
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정


                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기 
                if ball_img_idx < 3:

                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), #공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), #공의 y 좌표
                        "img_idx" : ball_img_idx + 1, #공의 이미지 인덱스
                        "to_x": -3, #x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6, # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})# y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), #공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), #공의 y 좌표
                        "img_idx" : ball_img_idx + 1, #공의 이미지 인덱스
                        "to_x": 3, #x축 이동방향, -3 이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6, # y축 이동방향
                        "init_spd_y": ball_speed_y[ball_img_idx +1]})# y 최초 속도
                print("무기와 공의 충돌")
                break
            else:
                continue
            break

    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1



    # enemy_rect = enemy.get_rect()
    # enemy_rect.left = enemy_x_pos
    # enemy_rect.top = enemy_y_pos

    # 충돌체크
    # if character_rect.colliderect(enemy_rect):
    #     print("충돌했어요")
    #     running = False

# 5. 화면에 그리기

    #screen.filll((0, 0, 255)) # RGB값으로 배경설정방법
    screen.blit(background, (0, 0)) # 배경 그리기

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x,ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))

    screen.blit(character, (character_x_pos, character_y_pos))
   
    # screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    
    pygame.display.update() # 게임화면을 다시 그리기!

    # 타이머 집어 넣기
    # 경과시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    # 경과 시간(ms)을 1000으로 나누어서 초(s)단위로 표시

    timer =game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
    # 출력할 글자, True, 글자색상
    screen.blit(timer, (10, 10))

    # 만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print("타임아웃")
        running = False

    pygame.display.update() # 게임화면 다시 그리기

# 잠시 대기
pygame.time.delay(2000) # 2초 정도 대기 (ms)

# pygame 종료
pygame = quit()
