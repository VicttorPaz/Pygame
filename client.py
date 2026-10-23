import json
import socket
import pygame

SERVER_HOST, SERVER_PORT = "127.0.0.1", 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
ball_x, ball_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
p_l_y = p_r_y = SCREEN_HEIGHT / 2 - 60
score_left = score_right = 0
c_l = c_r = (50, 50, 50)
h_l = h_r = False
running = True

while running:
  clock.tick(60)
  teclas = [
      k
      for k, cond in [
          ("w", pygame.key.get_pressed()[pygame.K_w]),
          ("s", pygame.key.get_pressed()[pygame.K_s]),
          ("up", pygame.key.get_pressed()[pygame.K_UP]),
          ("down", pygame.key.get_pressed()[pygame.K_DOWN]),
      ]
      if cond
  ]
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      running = False
  try:
    sock.sendto(json.dumps({"teclas": teclas}).encode(), (SERVER_HOST, SERVER_PORT))
  except:
    pass
  try:
    while True:
      d, _ = sock.recvfrom(1024)
      st = json.loads(d.decode())
      ball_x, ball_y, p_l_y, p_r_y, score_left, score_right = (
          st["ball_x"],
          st["ball_y"],
          st["paddle_left_y"],
          st["paddle_right_y"],
          st["score_left"],
          st["score_right"],
      )
  except:
    pass

  if ball_x - 40 <= 40 and p_l_y <= ball_y <= p_l_y + 120:
    if not h_l:
      c_l, h_l = (255, 0, 0), True
  else:
    h_l = False

  if ball_x + 40 >= SCREEN_WIDTH - 40 and p_r_y <= ball_y <= p_r_y + 120:
    if not h_r:
      c_r, h_r = (0, 0, 255), True
  else:
    h_r = False

  screen.fill((135, 206, 235))
  score_txt = font.render(f"J1: {score_left}   J2: {score_right}", True, (0, 0, 0))
  screen.blit(score_txt, (SCREEN_WIDTH // 2 - 100, 20))
  pygame.draw.rect(screen, c_l, (20, p_l_y, 20, 120))
  pygame.draw.rect(screen, c_r, (SCREEN_WIDTH - 40, p_r_y, 20, 120))
  pygame.draw.circle(screen, (0, 0, 0), (int(ball_x), int(ball_y)), 40)
  pygame.display.flip()
pygame.quit()