import pygame
import random 
pygame.init()

# Inicializamos el módulo de mezcla de sonido y cargamos la música
pygame.mixer.init()
pygame.mixer.music.load('jugador.mp3')  # Ruta de tu archivo de música de fondo
pygame.mixer.music.set_volume(0.5)  

  
ANCHO = 1280
ALTO =850
#Se crea la ventana 
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('MAZE RUNNER')
 
class Pared(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
        self.image = pygame.image.load("marron.jpg").convert()
        self.rect=self.image.get_rect()
 
class Bola(pygame.sprite.Sprite): #Cargamos imagen sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("conejo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 80))
        self.rect=self.image.get_rect() 

class Zanahoria(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("zanahoria.png").convert_alpha() # Ruta de la imagen de la zanahoria
        self.image = pygame.transform.scale(self.image, (80, 80)) #tamaño imagen de zanahoria
        self.rect = self.image.get_rect()

class Explosivo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bomba.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class CaritaFeliz(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("feliz.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (ANCHO // 2 - 40, ALTO // 2 - 40)
        self.rect.center = (ANCHO // 2, ALTO // 2 + 50)  # Alinear en el centro, pero un poco más abajo

listaCaritaFeliz = pygame.sprite.Group()
carita_feliz = CaritaFeliz()
listaCaritaFeliz.add(carita_feliz)


def nueva_posicion_explosivos():
    x = random.randint(0, ANCHO-40)  # Genera una posición x aleatoria
    y = random.randint(0, ALTO-40)   # Genera una posición y aleatoria
    return x, y
 
#------------ MUROS --------------------------------------------
def construir_mapa(mapa): #Creamos una lista de rectángulos a partir de una listaMuros "mapa"
    listaMuros =[]
    x=0
    y=0
    for fila in mapa:
        for muro in fila:
            if muro =="X":
                listaMuros.append(pygame.Rect(x,y,80,80))
            x+=80
        x=0
        y+=80
    return listaMuros
 
def dibujar_muro(superficie, rectangulo): #Dibujamos un rectángulo
    pygame.draw.rect(superficie, NEGRO, rectangulo)
 
def dibujar_mapa(superficie, listaMuros): #Dibujamos listaMuros con los rectángulos muro
    for muro in listaMuros:
        dibujar_muro(superficie, muro)
         


movil = pygame.Rect(600,400, 40,40)
x=0
y=0
vel=0
alt=0
 
NEGRO = (0,0,0)
AZUL = (0,0,255)
VERDE = (65, 147, 52)
ROJO = (255, 0, 0)  

 
 

reloj = pygame.time.Clock()
 
listaPared = pygame.sprite.Group()
pared=Pared()
listaPared.add(pared)
 
listaBola = pygame.sprite.Group()
bola=Bola()
listaBola.add(bola)

listaExplosivos = pygame.sprite.Group()
explosivo1 = Explosivo(400, 300)  # Define la posición de los explosivos
explosivo2 = Explosivo(800, 400)
explosivo3 = Explosivo(600, 600)
explosivo4 = Explosivo(700, 400)
ExplosivO5 = Explosivo(700, 700)
Explosivo6 = Explosivo(300, 300)
listaExplosivos.add(explosivo1, explosivo2, explosivo3, explosivo4, ExplosivO5, Explosivo6)

fuente = pygame.font.Font(None, 150) 
fuente.set_bold(True)
 
 # Variables para controlar el tiempo
tiempo_anterior = pygame.time.get_ticks()
TIEMPO_CAMBIO_POSICION = 2000  # 2 segundos en milisegundos

 #Se dibuja el mapa del laberinto 
mapa = [
            "XXXXXXXXX XXXXXX"
            "X M XXXXXXXXXXXX",
            "X  X           X",
            "X XX X XXXXXXX X",
            "X X  X X  X    X",
            "X X XX X X XXX X",
            "XX    X    XX  X",
            "XXXX X XX X X XX",
            "X X   X X X    X",
            "X   X     XX XXX",
            "X X  XX        X",
            "XXXXXXXXXXXXXXXX",
    
        ]

 #dibuja las colisionas
listaMuros = construir_mapa(mapa)
meta_x = None
meta_y = None

# Encuentra la posición de la meta
for i, fila in enumerate(mapa):
    for j, caracter in enumerate(fila):
        if caracter == "M":
            meta_x = j * 40  # Multiplicamos por 40 porque cada celda es de 40x40
            meta_y = i * 40

meta = Zanahoria()
meta.rect.topleft = (meta_x, meta_y) # Posición de la meta
listaBola.add(meta)

victoria = False
 
 #bucle while que se encarga de los eventos el cual recoge los eventos del teclado
gameOver=False
musica_reproducida = False

mensaje_perdida = fuente.render('¡Perdiste!', True, ROJO)  # Agrega esta línea

#BUCLE PRINCIPAL
while not gameOver:
     
    reloj.tick(60)

         # Verifica si es tiempo de cambiar la posición de los explosivos
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_anterior >= TIEMPO_CAMBIO_POSICION:
        for explosivo in listaExplosivos:
            explosivo.rect.topleft = nueva_posicion_explosivos()
        tiempo_anterior = tiempo_actual

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver=True
 
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vel=-5
            elif event.key == pygame.K_RIGHT:
                vel=+5
            elif event.key == pygame.K_UP:
                alt=-5
            elif event.key == pygame.K_DOWN:
                alt=+5
            if not musica_reproducida:
                pygame.mixer.music.play()  # Reproducir música de fondo
                musica_reproducida = True
        else:
            vel=0
            alt=0
     
     #el jugador el cual se va desplazar
    movil.x += vel
    movil.y += alt

    bola.rect.x = movil.x
    bola.rect.y = movil.y
     #la colision  pasa por listaMuros y cuando colicione invierte a negativo x devolviendo el paso hacia atras
    for muro in listaMuros: #Recorremos cada cuadrado de la lista para comprobar las colisiones
        if movil.colliderect(muro):
            movil.x -= vel
            movil.y -= alt

    for explosivo in listaExplosivos:
        if bola.rect.colliderect(explosivo.rect):
            print("¡Perdiste!")  
            pygame.mixer.music.load('perdio.mp3')  # Carga la música de derrota
            pygame.mixer.music.play() 
            mensaje = fuente.render('GAME OVER!', True, ROJO)
            ventana.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2 - mensaje.get_height() // 2))
            #ventana.blit(mensaje, (ANCHO // 4 - mensaje.get_width() // 4, ALTO // 4 - mensaje.get_height() // 4))

            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            quit()


    # Verifica si el jugador ha alcanzado la meta
    if movil.colliderect(pygame.Rect(meta_x, meta_y, 40, 40)):
        victoria = True
    #-------------FONDO---------------------
    ventana.fill(NEGRO)
     
    #------------ DIBUJO ------------------
    x=0
    y=0
    for fila in mapa:
        for muro in fila:
            if muro=="X":
                pared.rect.x=x
                pared.rect.y=y
                listaPared.add(pared)
                listaPared.draw(ventana)
            x+=40
        x=0
        y+=40
    listaBola.draw(ventana)    
    dibujar_mapa(ventana,listaMuros)
    listaExplosivos.draw(ventana)
    pygame.display.flip()

    # Si el jugador alcanzó la meta, muestra un mensaje de victoria y termina el juego
    if victoria:
        pygame.mixer.music.load('gano.mp3')  # Carga la música de victoria
        pygame.mixer.music.play() 
        mensaje = fuente.render('¡Ganaste!', True, AZUL)
        #ventana.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 8, ALTO // 8 - mensaje.get_height() // 4))
        ventana.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2 - mensaje.get_height() // 2))
        carita_feliz.rect.center = (ANCHO // 2, ALTO // 2 + 100)  # Alinear la cara feliz debajo del mensaje
        listaCaritaFeliz.draw(ventana)
        pygame.display.flip()
        pygame.time.wait(2000) 
        print("¡Ganaste!") # Ruta de tu archivo de victoria
        
        break

pygame.quit()