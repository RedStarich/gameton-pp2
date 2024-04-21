from functions.getMouseAngle import get_mouse_angle

# Checking collision between two lines
def collideLineLine(P0, P1, Q0, Q1):
  d = (P1[0] - P0[0]) * (Q1[1] - Q0[1]) + (P1[1] - P0[1]) * (Q0[0] - Q1[0]) 
  if d == 0:
    return None
  t = ((Q0[0] - P0[0]) * (Q1[1] - Q0[1]) + (Q0[1] - P0[1]) * (Q0[0] - Q1[0])) / d
  u = ((Q0[0] - P0[0]) * (P1[1] - P0[1]) + (Q0[1] - P0[1]) * (P0[0] - P1[0])) / d

  if 0 <= t <= 2 and 0 <= u <= 1:
    return P1[0] * t + P0[0] * (1 - t), P1[1] * t + P0[1] * (1 - t)

# Checking collision between line and rect
def colide_rect_line(rect, p1, p2, laser):
  angle = get_mouse_angle(laser)

  collision_pos = None
  if 0 <= angle and angle < 180:
    collision_pos = collideLineLine(p1, p2, rect.bottomleft, rect.bottomright)
    if collision_pos:
      return collision_pos
  if 90 <= angle and angle < 270:
    collision_pos = collideLineLine(p1, p2, rect.bottomright, rect.topright)
    if collision_pos:
      return collision_pos
  if 180 <= angle and angle < 360:
    collision_pos = collideLineLine(p1, p2, rect.topright, rect.topleft)
    if collision_pos:
      return collision_pos
  if (270 <= angle and angle < 360) or (0 <= angle and angle < 90):
    collision_pos = collideLineLine(p1, p2, rect.topleft, rect.bottomleft)
    if collision_pos:
      return collision_pos

  return collision_pos

# Checking collision between polygon (laser) and rect (Wall, Student, etc)
def collide_rect_polygon(rect, polygon, laser):
    for i in range(len(polygon)-1):
        collision_pos = colide_rect_line(rect, polygon[i], polygon[i+1], laser)
        if collision_pos:
            return collision_pos
    return None