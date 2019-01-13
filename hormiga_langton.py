# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 12:49:58 2019

@author: Javi, Fabio
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
BORRAR = False
UNA_ITERACION = False
PAUSA_STR = "Pausado"
ITERACIONES = 0
POBLACION = 0
PULSAR_UNA_VEZ = 1

DIMENSION = 80
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
pygame.display.set_caption("Hormiga")
done = False
clock = pygame.time.Clock()

# -------- Texto -----------
pygame.font.init()
FONT_CABECERA = pygame.font.SysFont('Arial',20)
TEXT_CABECERA = FONT_CABECERA.render('Hormiga de Langton', True, WHITE)
FONT_CABECERA = pygame.font.SysFont('Arial',50)
FONT_START = pygame.font.SysFont('Arial',15)
FONT_AUTORES = pygame.font.SysFont('Arial',15)
INFO_TEXT1 = FONT_START.render("Pulsa espacio para reanudar/pausar el juego.", True, WHITE)
INFO_TEXT3 = FONT_START.render("Con el juego en pausa, pulsa R para reiniciar el juego.", True, WHITE)
INFO_TEXT4 = FONT_START.render("Con el juego en pausa, pulsa S para realizar una iteración.", True, WHITE)
PAUSA_TEXT = FONT_START.render("El juego está actualmente: " +PAUSA_STR, True, WHITE)
ITERA_TEXT = FONT_START.render("Número de iteraciones: " + str(ITERACIONES), True, WHITE)
POBLACION_TEXT = FONT_START.render("Población" + str(POBLACION), True, WHITE)
AUTORES_TEXT = FONT_AUTORES.render("Proyecto realizado por Fabio Rodríguez Macías y Javier Ortiz Pérez", True, WHITE)
AUTORES_TEXT2 = FONT_AUTORES.render("Matemáticas para la Computación", True, WHITE)
AUTORES_TEXT3 = FONT_AUTORES.render("Universidad de Sevilla", True, WHITE)
AUTORES_TEXT4 = FONT_AUTORES.render("Grado en Ingeniería Informática - Tecnologías Informáticas", True, WHITE)
AUTORES_TEXT5 = FONT_AUTORES.render("Curso 2018/2019", True, WHITE)


def listener(tablero): #Está a la escucha del raton
    global PAUSE
    global UNA_ITERACION
    global BORRAR
    global PAUSA_STR
    global PAUSA_TEXT
    global PULSAR_UNA_VEZ
    for event in pygame.event.get():  # usuario hace algo
        if event.type == pygame.QUIT:  # si el usuario hace click, cierra
            pygame.quit()
        if PULSAR_UNA_VEZ == 1:
            tablero[50][30] = 2
            PULSAR_UNA_VEZ = 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if PAUSE==0:
                PAUSA_STR = "Pausado"
                PAUSA_TEXT = FONT_START.render("El juego está actualmente: " +PAUSA_STR, True, WHITE)
                PAUSE = 1
                print(PAUSA_STR)
            elif PAUSE == 1:
                PAUSA_STR = "En ejecución"
                PAUSA_TEXT = FONT_START.render("El juego está actualmente: " + PAUSA_STR, True, WHITE)
                PAUSE = 0
                print(PAUSA_STR)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and PAUSE == 1:
            BORRAR = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and PAUSE == 1:
            UNA_ITERACION = True

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

def contador_poblacion(tablero):
    cont = 0
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if tablero[i][j] == 1:
                cont += 1
    return cont



# -------- Loop principal del script -----------
while not done:
    listener(tablero)
    screen.fill(BLACK)

    screen.blit(TEXT_CABECERA, (100 + WINDOW_CTE * DIMENSION, 25))
    screen.blit(INFO_TEXT1, (50 + WINDOW_CTE * DIMENSION, 100))
    screen.blit(INFO_TEXT3, (50 + WINDOW_CTE * DIMENSION, 110))
    screen.blit(INFO_TEXT4, (50 + WINDOW_CTE * DIMENSION, 120))
    screen.blit(PAUSA_TEXT, (50 + WINDOW_CTE * DIMENSION, 280))
    screen.blit(ITERA_TEXT, (50 + WINDOW_CTE * DIMENSION, 290))
    screen.blit(POBLACION_TEXT, (50 + WINDOW_CTE * DIMENSION, 300))
    screen.blit(AUTORES_TEXT, (50 + WINDOW_CTE * DIMENSION, 340))
    screen.blit(AUTORES_TEXT2, (50 + WINDOW_CTE * DIMENSION, 350))
    screen.blit(AUTORES_TEXT4, (50 + WINDOW_CTE * DIMENSION, 360))
    screen.blit(AUTORES_TEXT3, (50 + WINDOW_CTE * DIMENSION, 370))
    screen.blit(AUTORES_TEXT5, (50 + WINDOW_CTE * DIMENSION, 380))

    if PAUSE == 0:
        ITERACIONES += 1
        ITERA_TEXT = FONT_START.render("Número de iteraciones: " + str(ITERACIONES), True, WHITE)
        generar_siguiente_generacion = iteracion(tablero,tablero)  # En el tablero vacio generamos la siguiente generacion.
        dibujado(generar_siguiente_generacion)  # Dibujamos la pantalla según el nuevo tablero
        tablero = generar_siguiente_generacion  # Ponemos el tablero base como la nueva generación
        POBLACION = contador_poblacion(tablero)
        POBLACION_TEXT = FONT_START.render("Población: " + str(POBLACION), True, WHITE)

    if PAUSE == 1:
        POBLACION = contador_poblacion(tablero)
        POBLACION_TEXT = FONT_START.render("Población: " + str(POBLACION), True, WHITE)
        if BORRAR:
            ITERACIONES = 0
            ITERA_TEXT = FONT_START.render("Número de iteraciones: " + str(ITERACIONES), True, WHITE)
            tablero = tablero_vacio()
            tablero[50][30] = 2
            dibujado(tablero)
            BORRAR = False
        if UNA_ITERACION:
            ITERACIONES += 1
            ITERA_TEXT = FONT_START.render("Número de iteraciones: " + str(ITERACIONES), True, WHITE)
            generar_siguiente_generacion = iteracion(tablero,tablero)  # En el tablero vacio generamos la siguiente generacion.
            dibujado(generar_siguiente_generacion)  # Dibujamos la pantalla según el nuevo tablero
            tablero = generar_siguiente_generacion  # Ponemos el tablero base como la nueva generación
            UNA_ITERACION = False

        dibujado(tablero)
        #-------------------------------
    clock.tick(60) #Fps a los que ira el juego
    pygame.display.flip()  # actualizamos con lo que hemos dibujado

pygame.quit()

