import pygame
import random
import sys
import cv2
import numpy as np
from directkeys import A, D, W, S, Space, ReleaseKey, PressKey
from webCam import ColorDetector  # Asumiendo que ColorDetector está en webCam.py

pygame.init()

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Selección")

# Fuente
fuente = pygame.font.SysFont(None, 55)

# Clase Problema Matematico
class ProblemaMatematico:
    def __init__(self):
        self.generar_problema()
        self.y_pos = 0  # Posicion Y inicial de las respuestas

    def generar_problema(self):
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.operador = random.choice(['+', '-', '*'])
        if self.operador == '+':
            self.respuesta_correcta = self.num1 + self.num2
        elif self.operador == '-':
            self.respuesta_correcta = self.num1 - self.num2
        elif self.operador == '*':
            self.respuesta_correcta = self.num1 * self.num2

        self.respuesta_incorrecta = self.respuesta_correcta + random.choice([-2, -1, 1, 2])
        self.posicion_correcta = random.choice(['izquierda', 'derecha'])
        self.y_pos = 0  # Reiniciar la posicion Y al generar un nuevo problema

    def mostrar_problema(self):
        texto = f"{self.num1} {self.operador} {self.num2} = ?"
        return fuente.render(texto, True, BLANCO)

    def mostrar_respuestas(self):
        if self.posicion_correcta == 'izquierda':
            return (self.respuesta_correcta, self.respuesta_incorrecta)
        else:
            return (self.respuesta_incorrecta, self.respuesta_correcta)

    def actualizar(self):
        self.y_pos += 2  # Velocidad de caida de los bloques
        if self.y_pos > ALTO:
            self.generar_problema()  # Generar nuevo problema si las respuestas salen de la pantalla

speed = 10

# Clase Cubo
class Cubo:
    def __init__(self):
        self.rect = pygame.Rect(ANCHO // 2 - 25, ALTO - 50, 50, 50)  # Cubo en la parte inferior de la pantalla

    def mover(self, direccion):
        if direccion == 'izquierda' and self.rect.left > 0:
            self.rect.x -= speed
        elif direccion == 'derecha' and self.rect.right < ANCHO:
            self.rect.x += speed
        elif direccion == 'arriba' and self.rect.top > 0:
            self.rect.y -= speed
        elif direccion == 'abajo' and self.rect.bottom < ALTO:
            self.rect.y += speed

    def mostrar(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, self.rect)

# Inicializacion de objetos
problema = ProblemaMatematico()
cubo = Cubo()
detector_color = ColorDetector()  # Instancia de ColorDetector

puntuacion = 0
eleccion_usuario = None
respuesta_enviada = False  # Bandera para controlar el envio de respuesta

# Bucle principal del juego
corriendo = True
clock = pygame.time.Clock()

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Procesamiento de la imagen y control de teclas por ColorDetector si esta activo
    img = detector_color.process_frame()

    # Control de la eleccion de respuesta manualmente
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        cubo.mover('izquierda')
    elif teclas[pygame.K_d]:
        cubo.mover('derecha')
    elif teclas[pygame.K_w]:
        cubo.mover('arriba')
    elif teclas[pygame.K_s]:
        cubo.mover('abajo')

    # Integracion con ColorDetector para controlar acciones del juego
    if detector_color.currentKey:
        for key in detector_color.currentKey:
            if key == A:
                cubo.mover('izquierda')
            elif key == D:
                cubo.mover('derecha')
            elif key == W:
                cubo.mover('arriba')
            elif key == S:
                cubo.mover('abajo')

    pantalla.fill(NEGRO)

    problema_texto = problema.mostrar_problema()
    pantalla.blit(problema_texto, (ANCHO // 2 - problema_texto.get_width() // 2, 50))

    problema.actualizar()  # Actualizar la posicion de las respuestas

    respuestas = problema.mostrar_respuestas()
    respuesta_izquierda_texto = fuente.render(str(respuestas[0]), True, BLANCO)
    respuesta_derecha_texto = fuente.render(str(respuestas[1]), True, BLANCO)

    # Posiciones de las respuestas
    pos_izquierda = (ANCHO // 4 - respuesta_izquierda_texto.get_width() // 2, problema.y_pos)
    pos_derecha = (3 * ANCHO // 4 - respuesta_derecha_texto.get_width() // 2, problema.y_pos)

    pantalla.blit(respuesta_izquierda_texto, pos_izquierda)
    pantalla.blit(respuesta_derecha_texto, pos_derecha)

    # Dibujar marcos alrededor de las respuestas
    marco_izquierda = pygame.Rect(pos_izquierda[0] - 10, pos_izquierda[1] - 10,
                                  respuesta_izquierda_texto.get_width() + 20,
                                  respuesta_izquierda_texto.get_height() + 20)
    marco_derecha = pygame.Rect(pos_derecha[0] - 10, pos_derecha[1] - 10,
                                respuesta_derecha_texto.get_width() + 20,
                                respuesta_derecha_texto.get_height() + 20)
    pygame.draw.rect(pantalla, BLANCO, marco_izquierda, 3)
    pygame.draw.rect(pantalla, BLANCO, marco_derecha, 3)

    # Verificar colisiones
    if cubo.rect.colliderect(marco_izquierda):
        eleccion_usuario = 'izquierda'
        respuesta_enviada = True
    elif cubo.rect.colliderect(marco_derecha):
        eleccion_usuario = 'derecha'
        respuesta_enviada = True

    if respuesta_enviada:
        if eleccion_usuario == problema.posicion_correcta:
            puntuacion += 1
        problema.generar_problema()
        respuesta_enviada = False  # Reiniciar la bandera

    cubo.mostrar(pantalla)

    puntuacion_texto = fuente.render(f"Puntuacion: {puntuacion}", True, BLANCO)
    pantalla.blit(puntuacion_texto, (10, 10))

    pygame.display.flip()

    clock.tick(60)  # Limitar el FPS a 60

# Detener el detector de color y salir
detector_color.stop()
pygame.quit()
sys.exit()






