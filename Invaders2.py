from PPlay.collision import *   
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from pygame.event import get
from random import *

import os

img_dir = os.path.dirname(os.path.abspath(__file__)) + '/img/'

def pad():

    #JOGAR
    pad1 = Sprite(img_dir + "pad1.png",1)
    pad1.x = janela.width/2 - pad1.width/2 
    pad1.y = janela.height/3.0 - pad1.height/2

    #DIFICULDADE
    pad2 = Sprite(img_dir + "pad2.png",1)
    pad2.x = janela.width/2 - pad2.width/2 
    pad2.y = janela.height/2.0 - pad2.height/2

    #RANKING
    pad3 = Sprite(img_dir + "pad3.png",1)
    pad3.x = janela.width/2 - pad3.width/2 
    pad3.y = janela.height/1.5 - pad2.height/2

    #SAIR
    pad4 = Sprite(img_dir + "pad4.png",1)
    pad4.x = janela.width/2 - pad4.width/2 
    pad4.y = janela.height/1.2 - pad4.height/2

    #FACIL
    pad5 = Sprite(img_dir + "pad5.png",1)
    pad5.x = janela.width/2 - pad1.width/2 
    pad5.y = janela.height/3.0 - pad1.height/2

    #MEDIO
    pad6 = Sprite(img_dir + "pad6.png",1)
    pad6.x = janela.width/2 - pad1.width/2 
    pad6.y = janela.height/2.0 - pad1.height/2

    #DIFICIL
    pad7 = Sprite(img_dir + "pad7.png",1)
    pad7.x = janela.width/2 - pad1.width/2 
    pad7.y = janela.height/1.5 - pad1.height/2

    lista_pad = [pad1, pad2, pad3, pad4, pad5, pad6, pad7]

    return lista_pad


def matriz(l,c, monstro_chefe):

    n2 =  1 # randint(0,1)
    n3 = randint(0,9)
    matriz= []

    for i in range(l):
        linha = []
        if i == n2:
            for j in range(c):
                if j == n3:
                    linha.append(monstro_chefe)
                else:
                    linha.append(Sprite(img_dir + "monstro.png", 1))
        else:
            for j in range(c):
                linha.append(Sprite(img_dir + "monstro.png", 1))
        matriz.append(linha)


    for x in range(l):  
        for y in range(c):
            matriz[x][y].set_position(y * monstro.width, x * monstro.height)
        
    lista = [matriz, n2, n3]
    
    return lista

#MENU E OUTRAS COISAS
janela = Window(728, 410)
janela.set_title(" ")
fundo = GameImage(img_dir + "fundo.jpg")
rato = Window.get_mouse()
teclado = Window.get_keyboard()

#SPRITES
pads = pad()
monstro = Sprite(img_dir + "monstro.png", 1)
monstro_chefe = Sprite(img_dir + "monstro_chefe.png", 1)
nave = Sprite(img_dir + "nave.png", 1)
nave.x = janela.width/2 - nave.width/2
nave.y = 360
lista_tiros = []
lista_tiros_inimigos = []

#PARAMETROS
estado_do_game = 0 
navevel = 250
tirovel = 300
tempo_recarga = 0 
tempo_recarga2 = 0
linha = 2
coluna = 10
coluna1 = coluna
coluna0 = coluna
ponto = 0
vida = 200
tiro_inimigo = 10 
pisca_nave_delay = 0
incremento = 0
incremento2 = 0
matriz_de_monstros = matriz(linha, coluna, monstro_chefe)
monstros = matriz_de_monstros[0]
n2 = matriz_de_monstros[1]
n3 = matriz_de_monstros[2]
n4 = n3

bateu_delay = 0
morte_boss = 0

while True:
    
    # GAME STAGE 0 (MENU)
    if (estado_do_game == 0):
        fundo.draw()
        for i in range(4):
            pads[i].draw()
    

        #RESET DA FASE
        vida = 3
        ponto = 0
        coluna1 = coluna
        coluna0 = coluna
        monstrovel = 70 + incremento
        tiro_inimigo = 10 - incremento2
        matriz_de_monstros = matriz(linha, coluna, monstro_chefe)
        monstros = matriz_de_monstros[0]
        morte_boss = 0
        n2 = matriz_de_monstros[1]
        n3 = matriz_de_monstros[2]
        n4 = n3

        if (rato.is_over_object(pads[0]) == True ) and (rato.is_button_pressed(1)):
            janela.delay(200)
            estado_do_game = 1

        if (rato.is_over_object(pads[1]) == True ) and (rato.is_button_pressed(1)):
            janela.delay(300)
            estado_do_game = 2
        if (rato.is_over_object(pads[2]) == True ) and (rato.is_button_pressed(1)):
            estado_do_game = 3
        if (rato.is_over_object(pads[3]) == True ) and (rato.is_button_pressed(1)):
            janela.close()

        # GAME STAGE 1 (JOGO)
    elif (estado_do_game == 1):
        tempo_recarga = tempo_recarga + janela.delta_time()
        tempo_recarga2 = tempo_recarga2 + janela.delta_time()
        bateu_delay += janela.delta_time()
        fundo.draw()
        nave.draw() 

        #MOVIMENTO DA NAVE
        if teclado.key_pressed("LEFT") and nave.x >= 0:
            nave.x -= navevel * janela.delta_time()
        if teclado.key_pressed("RIGHT") and nave.x <= janela.width - nave.width:
            nave.x += navevel * janela.delta_time()

        #CRIA O TIRO
        if teclado.key_pressed("SPACE") and (tempo_recarga > 1.1):
            tiro = Sprite(img_dir + "tiro.png", 1)
            lista_tiros.append(tiro)
            lista_tiros[-1].x = nave.x + nave.width/2 - lista_tiros[-1].width/2
            lista_tiros[-1].y = nave.y - 10
            tempo_recarga = 0     

        #MOVIMENTA O TIRO
        for i in lista_tiros:
            i.y -= tirovel * janela.delta_time()

        # DESENHA O TIRO
        for i in lista_tiros:
            i.draw()

        # APAGA O TIRO SE SAIR DA TELA
        for i in range(len(lista_tiros)):
            if lista_tiros[0].y < 0:
                lista_tiros.pop(0)

        #CRIA O TIRO INIMIGO
        if monstros[1] == []:
            n = 0
        elif monstros[0] == []: 
            n = 1           
        else: 
            n = randint(0,1)
        escolhido = choice(monstros[n])

        if(tempo_recarga2 > tiro_inimigo):
            tiro2 = Sprite(img_dir + "tiro2.png", 1)
            lista_tiros_inimigos.append(tiro2)
            lista_tiros_inimigos[-1].x = escolhido.x +  escolhido.width/3
            lista_tiros_inimigos[-1].y = escolhido.y + 20
            tempo_recarga2 = 0

        #MOVIMENTA O TIRO INIMIGO
        for i in lista_tiros_inimigos:
            i.y += tirovel * janela.delta_time()

        # DESENHA O TIRO
        for i in lista_tiros_inimigos:
            i.draw()
        # APAGA O TIRO SE SAIR DA TELA
        for i in range(len(lista_tiros_inimigos)):
            if lista_tiros_inimigos[0].y > 395:
                lista_tiros_inimigos.pop(0)

        # SE O TIRO ACERTAR A NAVE
        for t in range(len(lista_tiros_inimigos)):   
            if Collision.collided_perfect(lista_tiros_inimigos[t], nave):
                lista_tiros_inimigos.pop(0)
                vida -=1
                pisca_nave_delay = 75
                break

        if pisca_nave_delay > 0:
            pisca_nave_delay -= 1
            if pisca_nave_delay % 2 == 1:
                nave.set_curr_frame(1)
            if pisca_nave_delay % 2 == 0:
                nave.set_curr_frame(0)                     
    
        #CONTROLA E MOVIMENTA OS INIMIGOS
        contador = 30
        for l in monstros:
            for c in l:
            
                c.x += monstrovel * janela.delta_time()
                if(c.x >= 685) and bateu_delay > 0.5:
                    monstrovel = -monstrovel
                    for x in monstros:
                        for y in x:
                            y.y += contador
                    bateu_delay = 0
                elif (c.x <= -5) and bateu_delay > 0.5:
                    monstrovel = -monstrovel
                    for x in monstros:
                        for y in x:
                            y.y += contador
                    bateu_delay = 0

        #CONTROLE DA LINHA INFERIOR DOS MONSTROS
      
        for c in range(coluna1):
            for t in range(len(lista_tiros)):   
                if Collision.collided_perfect(lista_tiros[t], monstros[1][c]) and (monstros[1][c] != monstro_chefe):
                    lista_tiros.pop(0)
                    monstros[1].pop(c)
                    coluna1 -= 1
                    ponto += 1
                    break
                elif Collision.collided_perfect(lista_tiros[t], monstros[1][c]) and (monstros[1][c] == monstro_chefe):
                    morte_boss += 1
                    lista_tiros.pop(0)
                    if morte_boss == 3:
                        monstros[1].pop(c)
                        coluna1 -= 1
                        ponto += 1

        #CONTROLE DA LINHA SUPERIOR DOS MONSTROS    
        for c in range(coluna0):               
            for t in range(len(lista_tiros)):   
                if Collision.collided_perfect(lista_tiros[t], monstros[0][c]) and (monstros[0][c] != monstro_chefe):
                    lista_tiros.pop(0)
                    monstros[0].pop(c)
                    coluna0 -= 1
                    ponto += 1
                    break
                elif Collision.collided_perfect(lista_tiros[t], monstros[0][c]) and (monstros[0][c] == monstro_chefe):
                    morte_boss += 1
                    lista_tiros.pop(0)
                    if morte_boss == 3:
                        monstros[0].pop(c)
                        coluna0 -= 1
                        ponto += 1
        #DESENHA OS MONSTROS        
        for l in monstros:
            for c in l:
                c.draw() 
        
        if monstros == [[],[]]:
            matriz_de_monstros = matriz(linha, coluna, monstro_chefe)
            monstros = matriz_de_monstros[0]
            n2 = matriz_de_monstros[1]
            n3 = matriz_de_monstros[2]
            n4 = n3
            coluna1 = coluna
            coluna0 = coluna
            monstrovel *= 1.1
            tiro_inimigo -= 0.1
            morte_boss = 0

        janela.draw_text(f"Pontuação: {ponto}", 620, 385, 16,  (255,255,255), "Calibri", True)
        janela.draw_text(f"Vida: {vida}", 10, 385, 16,  (255,255,255), "Calibri", True)
              
        for l in monstros:
            for c in l:
                if Collision.collided_perfect(nave, c) or (c.y > 395) or (vida == 0):
                    estado_do_game = 0
                    coluna1 = coluna
                    coluna0 = coluna
                    monstrovel = 70
                    tiro_inimigo = 10
                    pisca_nave_delay = 0


        #GAME STAGE 2 (DIFICULDADES)
    elif (estado_do_game == 2):
        fundo.draw()
        for i in range(1, 4):
            pads[-i].draw()
        if (rato.is_over_object(pads[-3]) == True ) and (rato.is_button_pressed(1)):
            janela.delay(400)
            estado_do_game = 0
            incremento = 0
            incremento2 = 0
        if (rato.is_over_object(pads[-2]) == True ) and (rato.is_button_pressed(1)):
            janela.delay(400)
            estado_do_game = 0
            incremento = 20
            incremento2 = 3
        if (rato.is_over_object(pads[-1]) == True ) and (rato.is_button_pressed(1)):
            janela.delay(200)
            estado_do_game = 0
            incremento = 30
            incremento2 = 7
        if (teclado.key_pressed("ESC") == 1):      
            estado_do_game = 0
    
    elif(estado_do_game == 3):
        fundo.draw()
        janela.draw_text(f"Press ESC", 10, 10, 16,  (255,255,255), "Calibri", True)
        if(teclado.key_pressed("ESC") == 1):      
            estado_do_game = 0  
    janela.update()

