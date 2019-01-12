# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 12:49:58 2019

@author: Javi_
"""

import pygame

screen = pygame.display.set_mode((640,480))
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GRAY = (130,130,130)
PAUSE = 1

WIDTH = 8
HEIGHT = 8
MARGIN = 1
WINDOW_CTE = WIDTH + MARGIN
EXTRA_WINDOW = 400


print("Introducir dimensión")
DIMENSION = int(input())
tablero = []

ultimo_movimiento = None #Ultimo movimiento que hizo la hormiga
casilla_actual = None    #Valor que tiene la casilla en la que está. 0 o 1

for row in range(DIMENSION):
    tablero.append([])
    for column in range(DIMENSION):
        tablero[row].append(0)

pygame.init()

WINDOW_SIZE = [WINDOW_CTE*DIMENSION + EXTRA_WINDOW, WINDOW_CTE*DIMENSION]
print(WINDOW_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Game of Life")
done = False
clock = pygame.time.Clock()

# -------- Texto -----------
pygame.font.init()
FONT_CABECERA = pygame.font.SysFont('Arial',20)
TEXT_CABECERA = FONT_CABECERA.render('Hormiga de Langton', True, WHITE)


def listener(tablero): #Está a la escucha del raton
    global PAUSE
    for event in pygame.event.get():  # usuario hace algo
        if event.type == pygame.QUIT:  # si el usuario hace click, cierra
            done = True  # variable done true, fin del bucle
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]: #Se ejecuta cada vez que se clicka
            pos = pygame.mouse.get_pos()
            if pos[0] < WINDOW_CTE*DIMENSION:
            # Cambiamos las coordenadas x/y por las del tablero
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
            # ponemos esta posición en 1
                if PAUSE == 1:
                    tablero[row][column] = 2
        elif event.type == pygame.KEYDOWN:
            if PAUSE==0:
                PAUSE = 1
            elif PAUSE == 1:
                PAUSE = 0


def dibujado(tablero_vacio): #Colorea la hormiga y su rastro
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = BLACK
            if tablero_vacio[row][column] == 1:
                color = WHITE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            if tablero_vacio[row][column] == 2:
                color = BLUE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

def iteracion(tablero, tablero_vacio): #Se modifica el tablero según las reglas del juego pero no se dibuja
    global casilla_actual
    global ultimo_movimiento
    for row in range(len(tablero_vacio)):
        for column in range(len(tablero_vacio)):
            try:
                hormiga = tablero[row][column]
                #Hacemos que el primero movimiento de la hormiga sea a la izquierda
                if hormiga == 2: #Posición hormiga
                    if ultimo_movimiento == None: 
                        casilla_actual = 0
                        ultimo_movimiento = "izquierda"
                        tablero_vacio[row][column-1] = 2
                        tablero_vacio[row][column] = 1
                    #Aquí van las reglas del juego
                    else:
                        if ultimo_movimiento == ("izquierda") and casilla_actual == 0:
                            tablero_vacio[row][column] = 1 #Cambia la casilla en la que estaba
                            casilla_actual = tablero[row-1][column] #Casilla a la que va
                            tablero_vacio[row-1][column] = 2 #Mueve la hormiga
                            ultimo_movimiento = "arriba"
                                
                        elif ultimo_movimiento == ("izquierda") and casilla_actual == 1:
                            tablero_vacio[row][column] = 0 
                            casilla_actual = tablero[row+1][column]
                            tablero_vacio[row+1][column] = 2 #Mueve la hormiga
                            ultimo_movimiento = "abajo"
                            
                        elif ultimo_movimiento == ("arriba") and casilla_actual == 0:
                            tablero_vacio[row][column] = 1
                            casilla_actual = tablero[row][column+1]
                            tablero_vacio[row][column+1] = 2 #Mueve la hormiga
                            ultimo_movimiento = "derecha"
                            
                        elif ultimo_movimiento == ("arriba") and casilla_actual == 1:
                            tablero_vacio[row][column] = 0
                            casilla_actual = tablero[row][column-1]        
                            tablero_vacio[row][column-1] = 2 #Mueve la hormiga
                            ultimo_movimiento = "izquierda"
                            
                        elif ultimo_movimiento == ("derecha") and casilla_actual == 0:
                            tablero_vacio[row][column] = 1
                            casilla_actual = tablero[row+1][column]
                            tablero_vacio[row+1][column] = 2 #Mueve la hormiga
                            ultimo_movimiento = "abajo"
                            
                        elif ultimo_movimiento == ("derecha") and casilla_actual == 1:
                            tablero_vacio[row][column] = 0
                            casilla_actual = tablero[row-1][column]
                            tablero_vacio[row-1][column] = 2 #Mueve la hormiga
                            ultimo_movimiento = "arriba"
                            
                        elif ultimo_movimiento == ("abajo") and casilla_actual == 0:
                            tablero_vacio[row][column] = 1
                            casilla_actual = tablero[row][column-1]
                            tablero_vacio[row][column-1] = 2 #Mueve la hormiga
                            ultimo_movimiento = "izquierda"
                            
                        elif ultimo_movimiento == ("abajo") and casilla_actual == 1:
                            tablero_vacio[row][column] = 0
                            casilla_actual = tablero[row][column+1]
                            tablero_vacio[row][column+1] = 2 #Mueve la hormiga
                            ultimo_movimiento = "derecha"      
            except:
                pass
    return tablero_vacio
    

def tablero_vacio():
    tablero_vacio = []
    for r in range(DIMENSION):
        row = []
        for c in range(DIMENSION):
            row.append(0)
        tablero_vacio.append(row)
    return tablero_vacio

# -------- Loop principal del script -----------
while not done:
    listener(tablero)  # Está a la escucha de los clicks
    screen.fill(GRAY) #Color del fondo
    screen.blit(TEXT_CABECERA, (10 + WINDOW_CTE * DIMENSION,50))
    
    #Aqui se ejecuta 
    if PAUSE == 0:
        generar_siguiente_generacion = iteracion(tablero, tablero) 
        dibujado(generar_siguiente_generacion) #Dibujamos la pantalla según el nuevo tablero
        tablero = generar_siguiente_generacion #Ponemos el tablero base como la nueva generación
    if PAUSE == 1:
        dibujado(tablero)
    #-------------------------------
    clock.tick(60) #Fps a los que ira el juego
    pygame.display.flip()  # actualizamos con lo que hemos dibujado

pygame.quit()

