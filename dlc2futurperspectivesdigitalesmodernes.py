import pygame
"""Si objet atour du pc (ie epée):
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    dx = mouse_x-rect_x
    dy = mouse_y - rect_y
    theta_b = m.atan2(dy,dx)
    print(m.degrees(theta_b))
   
    if event.type == pygame.MOUSEBUTTONDOWN:
        direction = Vector2(dx,dy).unit
    else:
        direction = Vector2(0,0)
            
            
    pygame.draw.circle(fenetre, BLACK,((Vector2((rect_x+5)+25*m.cos(theta_b), (rect_y+5)+25*m.sin(theta_b))+direction*5).components), 10,)
            """

pygame.mouse.set_visible(False)
