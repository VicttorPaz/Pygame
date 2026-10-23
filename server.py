import json
import socket
import pygame

# --- CONFIGURACIÓN DE RED Y PANTALLA ---
HOST, PORT = "127.0.0.1", 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.setblocking(False)

W, H = 1280, 720
clock = pygame.time.Clock()

# --- ESTADO DEL JUEGO ---
ball_pos = pygame.Vector2(W / 2, H / 2)
ball_vel = pygame.Vector2(400, 300)
ball_r = 40
p_w, p_h, p_spd = 20, 120, 500

# Paletas izquierda y derecha
p_left = pygame.Rect(20, (H - p_h) / 2, p_w, p_h)
p_right = pygame.Rect(W - 40, (H - p_h) / 2, p_w, p_h)

score_l = score_r = 0
clientes = []

print(f"Servidor UDP en {HOST}:{PORT}... Esperando 2 jugadores.")

while True:
  dt = clock.tick(60) / 1000.0

  # 1. RECEPCIÓN DE ENTRADAS Y GESTIÓN DE CLIENTES
  try:
    while True:
      data, addr = sock.recvfrom(1024)
      teclas = json.loads(data.decode()).get("teclas", [])

      # Registro dinámico o reconexión de jugadores
      if addr not in clientes:
        if len(clientes) < 2:
          clientes.append(addr)
          print(f"-> Jugador {len(clientes)} conectado desde {addr}")
        else:
          clientes[1] = addr  # Reemplaza al segundo slot si se reconecta

      # Movimiento por índice de cliente
      if clientes and addr == clientes[0]:
        if "w" in teclas:
          p_left.y -= p_spd * dt
        if "s" in teclas:
          p_left.y += p_spd * dt
      elif len(clientes) > 1 and addr == clientes[1]:
        if "w" in teclas or "up" in teclas:
          p_right.y -= p_spd * dt
        if "s" in teclas or "down" in teclas:
          p_right.y += p_spd * dt
  except BlockingIOError:
    pass

  # Limitar paletas dentro de los márgenes de la pantalla
  p_left.top = max(0, min(p_left.top, H - p_h))
  p_right.top = max(0, min(p_right.top, H - p_h))

  # 2. FÍSICA DE LA PELOTA (SÓLO CUANDO HAY 2 JUGADORES)
  if len(clientes) == 2:
    ball_pos += ball_vel * dt
    
    # --- IMPRESIÓN DE DEPURACIÓN RESTAURADA ---
    print(
        f"Pelota -> X: {ball_pos.x:.1f} | Y: {ball_pos.y:.1f} || "
        f"Izq Y: {p_left.y:.1f} || "
        f"Der Y: {p_right.y:.1f}"
    )

    b_rect = pygame.Rect(
        ball_pos.x - ball_r, ball_pos.y - ball_r, ball_r * 2, ball_r * 2
    )

    # Rebote con paletas (invierte dirección y aumenta velocidad un 10%)
    if b_rect.colliderect(p_left):
      ball_pos.x = p_left.right + ball_r
      ball_vel.x *= -1
      ball_vel *= 1.1
    elif b_rect.colliderect(p_right):
      ball_pos.x = p_right.left - ball_r
      ball_vel.x *= -1
      ball_vel *= 1.1

    # Rebote con techos superior e inferior
    if ball_pos.y - ball_r <= 0 or ball_pos.y + ball_r >= H:
      ball_pos.y = max(ball_r, min(ball_pos.y, H - ball_r))
      ball_vel.y *= -1

    # Anotación de puntos y reseteo al centro
    if ball_pos.x < 0 or ball_pos.x > W:
      if ball_pos.x < 0:
        score_r += 1
        ball_vel = pygame.Vector2(400, 300)
      else:
        score_l += 1
        ball_vel = pygame.Vector2(-400, 300)
      ball_pos = pygame.Vector2(W / 2, H / 2)

  # 3. ENVÍO DE ESTADO (BROADCAST) A TODOS LOS CLIENTES
  estado = json.dumps({
      "ball_x": ball_pos.x,
      "ball_y": ball_pos.y,
      "paddle_left_y": p_left.y,
      "paddle_right_y": p_right.y,
      "score_left": score_l,
      "score_right": score_r,
  }).encode()

  for cliente in clientes:
    sock.sendto(estado, cliente)