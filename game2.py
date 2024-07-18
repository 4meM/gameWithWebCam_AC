import pygame
import random
import sys
import cv2
import numpy as np
from directkeys import A, D, Space, ReleaseKey, PressKey
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

# Clase Problema Matemático
class ProblemaMatematico:
    def __init__(self):
        self.generar_problema()

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

    def mostrar_problema(self):
        texto = f"{self.num1} {self.operador} {self.num2} = ?"
        return fuente.render(texto, True, BLANCO)

    def mostrar_respuestas(self):
        if self.posicion_correcta == 'izquierda':
            return (self.respuesta_correcta, self.respuesta_incorrecta)
        else:
            return (self.respuesta_incorrecta, self.respuesta_correcta)

# Inicialización de objetos
problema = ProblemaMatematico()
detector_color = ColorDetector()  # Instancia de ColorDetector

puntuacion = 0
eleccion_usuario = None
respuesta_enviada = False  # Bandera para controlar el envío de respuesta

# Bucle principal del juego
corriendo = True
clock = pygame.time.Clock()

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Procesamiento de la imagen y control de teclas por ColorDetector si está activo
    img = detector_color.process_frame()

    # Control de la elección de respuesta manualmente
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        eleccion_usuario = 'izquierda'
    elif teclas[pygame.K_d]:
        eleccion_usuario = 'derecha'
    elif teclas[pygame.K_SPACE] and not respuesta_enviada:
        if eleccion_usuario is not None:
            if eleccion_usuario == problema.posicion_correcta:
                puntuacion += 1
            problema.generar_problema()
            respuesta_enviada = True  # Marcar que la respuesta ha sido enviada

    # Integración con ColorDetector para controlar acciones del juego
    if detector_color.currentKey:
        for key in detector_color.currentKey:
            if key == A:
                eleccion_usuario = 'izquierda'
            elif key == D:
                eleccion_usuario = 'derecha'
            elif key == Space and not respuesta_enviada:
                if eleccion_usuario is not None:
                    if eleccion_usuario == problema.posicion_correcta:
                        puntuacion += 1
                    problema.generar_problema()
                    respuesta_enviada = True  # Marcar que la respuesta ha sido enviada

    pantalla.fill(NEGRO)

    problema_texto = problema.mostrar_problema()
    pantalla.blit(problema_texto, (ANCHO // 2 - problema_texto.get_width() // 2, 50))

    respuestas = problema.mostrar_respuestas()
    respuesta_izquierda_texto = fuente.render(str(respuestas[0]), True, BLANCO)
    respuesta_derecha_texto = fuente.render(str(respuestas[1]), True, BLANCO)

    # Posiciones de las respuestas
    pos_izquierda = (ANCHO // 4 - respuesta_izquierda_texto.get_width() // 2, ALTO // 2)
    pos_derecha = (3 * ANCHO // 4 - respuesta_derecha_texto.get_width() // 2, ALTO // 2)

    pantalla.blit(respuesta_izquierda_texto, pos_izquierda)
    pantalla.blit(respuesta_derecha_texto, pos_derecha)

    # Marco alrededor de la respuesta seleccionada
    if eleccion_usuario == 'izquierda':
        pygame.draw.rect(pantalla, ROJO, (pos_izquierda[0] - 10, pos_izquierda[1] - 10,
                                          respuesta_izquierda_texto.get_width() + 20,
                                          respuesta_izquierda_texto.get_height() + 20), 3)
    elif eleccion_usuario == 'derecha':
        pygame.draw.rect(pantalla, ROJO, (pos_derecha[0] - 10, pos_derecha[1] - 10,
                                          respuesta_derecha_texto.get_width() + 20,
                                          respuesta_derecha_texto.get_height() + 20), 3)

    puntuacion_texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
    pantalla.blit(puntuacion_texto, (10, 10))

    pygame.display.flip()

    clock.tick(60)  # Limitar el FPS a 60

    # Reiniciar la bandera de respuesta enviada si Space no está presionado
    if not teclas[pygame.K_SPACE] and not any(key == Space for key in detector_color.currentKey):
        respuesta_enviada = False

# Detener el detector de color y salir
detector_color.stop()
pygame.quit()
sys.exit()




