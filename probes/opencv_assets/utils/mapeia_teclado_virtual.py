# Desenvolvido por: Marcio Cavalcante
# Data: 06/2020
# Descrição: Mapeia teclados virtuais e gera arquivo de configuração para importação nos demais scripts.

import sys
import cv2 
import re
import os
import time
import numpy as np
import pytesseract
from datetime import datetime

def mapeia_teclas(funcao_ativada):
    global lfrom,lto,cfrom,cto,frame,teclado

    # 1º insere a area da tela
    # 2º insere a posicao de cada tecla
    # funcao_ativada --> por exemplo, para acessar um caracter em maíusculo, necessário pressionar <shift>. Então, preencher com '<shift>' essa variavel.

    entrada=""
    funcao=False
    ocr_ok=False

    legenda=""
    
    teclado["area"][funcao_ativada]=[lfrom,lto,cfrom,cto]

    for i in reversed(range(len(contours))):
        # verifica as coordenadas da tecla
        cnt = contours[i]
        c,l,w,h = cv2.boundingRect(cnt)
                    
        l=lfrom+l
        c=cfrom+c
        
        tecla=frame[l:l+h, c:c+w]
        
        #tecla_resized = cv2.resize(tecla, (w*8,h*8), interpolation = cv2.INTER_AREA)
        tecla_resized=tecla
        
        ret,tecla_resized = cv2.threshold(tecla_resized,127,255,cv2.THRESH_BINARY_INV)
            
        frame = cv2.rectangle(frame,(c,l),(c+w,l+h),(0,255,255),2)
        
        cv2.imshow('Graphene', frame) 
        cv2.waitKey(1)
        
        if cv2.waitKey(1) == ord('q'):
            break

        # identifica tecla primeiro com OCR, e pede para usuario confirmar
        txt_wl='1234567890abcdefghijklmnopqrstuvxwyz@._-'
        texto_ocr = pytesseract.image_to_string(tecla_resized, config='--psm 13 --oem 3 -c tessedit_char_whitelist='+txt_wl)
        
        if len(texto_ocr) > 1:
        
            msg="Não detectada"
        else:
            msg=texto_ocr
        
        while True:
            entrada = input("\nEsta tecla é ["+msg+"]?\n Pressione 'Enter' para confirmar.\n Ou digite '<apagar>','<shift>','<unshift>','<simbolos>', '<acentos>' (sem aspas), ou o caracter correto: ")
            
            if entrada=="":
                entrada=texto_ocr
                ocr="ocr_ok"
            else:
                ocr="ocr_nok"
        
            retorno = re.search("<", entrada)

            if retorno:
                funcao="funcao_sim"
            else:
                funcao="funcao_nao"
           
            # funcao = informa se a tecla atual é uma função. Por exemplo: <shift>, <simbolos>
            
            try:
                teclado["tecla"][entrada][0]
                print(" Função já inserida ("+entrada+"). Tente outro nome.")
                continue
            except:
                teclado["tecla"][entrada]=[l,h,c,w,funcao,funcao_ativada,ocr]
                break
            
        frame = cv2.rectangle(frame,(c,l),(c+w,l+h),(0,255,0),2) 
        cv2.imshow('Graphene', frame) 
        cv2.waitKey(1)

def log_tela(msg):
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-5])+" - "+msg)

def mouse_drawing(event, x, y, flags, params):
    global lfrom, lto, cfrom, cto, selecao_ok, selecao, contours
    
    if event == cv2.EVENT_LBUTTONDOWN:
        r = cv2.selectROI("Graphene",frame)
        
        selecao = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        lfrom=int(r[1])
        lto=int(r[1]+r[3])
        cfrom=int(r[0])
        cto=int(r[0]+r[2])
               
        selecao = cv2.cvtColor(selecao, cv2.COLOR_BGR2GRAY)
        selecao = cv2.Canny(selecao, 30, 200)
        kernel = np.ones((5,5),np.uint8)
        selecao = cv2.dilate(selecao, kernel, iterations = 1)

        contours, hierarchy = cv2.findContours(selecao,  
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
        
        resp = input("\nNumero de teclas detectadas = " + str(len(contours)) + ".\n Seleção Ok? (S/N):")

        if resp=="S":
            selecao_ok=True
        if resp=="N":
            print(" Selecione novamente...")
        
        cv2.namedWindow("Graphene")
        cv2.setMouseCallback("Graphene", mouse_drawing)
        
def ver_funcoes():
    global funcoes, teclado
    # Array:
    #  0 - id da funcao
    #  1 - nome da funcao
    #  2 - mapeada
    
    tam_funcoes = len(funcoes)
    
    if tam_funcoes==0:
        # (escopo,funcao,ja foi mapeada)
        funcoes.append(["raiz","raiz",False])
    else:
        for t in teclado["tecla"]:
            encontrado=False
            if teclado["tecla"][t][4]=="funcao_sim":
                for f in funcoes:
                    #print(f[1],teclado["tecla"][t][5],t)
                    if f[1]==t:
                        encontrado=True
                        break
                
                if encontrado==False:
                    # (escopo,funcao,ja foi mapeada)
                    #print("adicionado"+teclado["tecla"][t][5])
                    funcoes.append([teclado["tecla"][t][5],t,False])

def grava_config():
    global teclado
    
    f = open("config", 'w', encoding='utf-8')
    f.write(str(teclado))
    f.close()

    print("Gerado arquivo config com:"+str(teclado))
#########
# Inicio

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def msg_erro_sintaxe():
    print("Sintaxe correta:")
    print("  > python mapeia_teclado_virtual.py POD\n")
    print("  POD=Valor de 1 à 4")
    
try:
    pod=int(sys.argv[1])
    if not (pod>=1 and pod<=4):
        sys.exit(0)
except:
    msg_erro_sintaxe()
    sys.exit(0)

cap = cv2.VideoCapture(pod-1)

os.system('cls')
print("Inicio do mapeamento de teclado virtual.")

teclado={}
teclado["area"]={}
teclado["tecla"]={}
funcoes=[]

sair=False

while sair==False:
    # selecionar funcao à mapear
    
    ver_funcoes()
    
    while True:
        print("Funções:")
        
        i=0

        for f in funcoes:
            msg=""
            
            if f[2]==True:
                msg="(mapeado)"
                
            print(" ",i+1,"-",f[0],"-->",f[1],msg)
            i=i+1
        print("  S - Sair")
        
        funcao_op = input("Qual funcao deseja mapear? ")
                
        if funcao_op=="S":
            cap.release()
            cv2.destroyAllWindows()
            grava_config()
            sys.exit(0)

        try:
            funcoes[int(funcao_op)-1]
            break
        except:
            print("Opcao inválida!")
            time.sleep(1)
            os.system('cls')
            continue

        if funcoes[int(funcao_op)-1][1]==True:
            print("Função já mapeada!")
            continue
            


    
    # mapear funcao
    print("\nNavegue até o teclado virtual que deseja mapear, e clique para selecionar a área.")

    contours=[]
    selecao=[]
    selecao_ok=False
    lfrom=0
    lto=0
    cfrom=0
    cto=0
    
    cv2.namedWindow("Graphene")
    cv2.setMouseCallback("Graphene", mouse_drawing)

    while(selecao_ok==False):
        ret ,frame = cap.read()
        
        cv2.imshow('Graphene',frame)
        
        if cv2.waitKey(1) == ord('q'):
            sair=True
            break
    
    mapeia_teclas(funcoes[int(funcao_op)-1][1])
    funcoes[int(funcao_op)-1][2]=True

