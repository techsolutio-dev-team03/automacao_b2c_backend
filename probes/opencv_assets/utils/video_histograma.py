#####################################################################
# Desenvolvido por: Marcio Cavalcante
# Data: 27/04/2020
# Descrição: Via histograma, gera templates para comparação de tela.
#
# Funções:
#   p = histograma da imagem selecionada em preto e branco
#   r = histograma da imagem selecionada em RGB
#   m = reseta valores de bins [maior / menor]
#   c = congela valores dos bins
#   d = descongela valores dos bins
#   a = visualiza / analisa mascara
#   t = gera arquivo em png da mascara
#   clique esquerdo = histograma da imagem selecionada em movimento
#   clique direito = histograma da imagem selecionada congelada
#   <ESC> = desmarca selecao / mascara
#   q = sai
######################################################################

# import the necessary packages
import sys
import copy
import time
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

def cria_mascara():
    global bin_menor, bin_maior, hist_rgb, frame_roi

    frm=copy.deepcopy(frame_roi)

    if hist_rgb==True:
        linhas,colunas,canais=frm.shape

        for l in range(linhas):
            for co in range(colunas):
                if (frm.item(l,co,0)>=bin_menor[0] and frm.item(l,co,0)<=bin_maior[0] and 
                 frm.item(l,co,1)>=bin_menor[1] and frm.item(l,co,1)<=bin_maior[1] and 
                 frm.item(l,co,2)>=bin_menor[2] and frm.item(l,co,2)<=bin_maior[2]):
                    frm.itemset((l,co,0),0)
                    frm.itemset((l,co,1),0)
                    frm.itemset((l,co,2),0)
                else:
                    frm.itemset((l,co,0),255)
                    frm.itemset((l,co,1),255)
                    frm.itemset((l,co,2),255)

    else:
        linhas,colunas=frm.shape
    
        for l in range(linhas):
            for co in range(colunas):
                    if frm.item(l,co)>=bin_menor[0] and frm.item(l,co)<=bin_maior[0]:
                        frm.itemset((l,co),0)
                    else:
                        frm.itemset((l,co),255)
    return frm

def reseta_bin():
    global bin_menor, bin_maior, congela_bins

    if congela_bins == False:
        for i in range(3):
            bin_menor[i]=256
            bin_maior[i]=0

def get_max_min_bin (hist,canal):
    global bin_menor, bin_maior, congela_bins

    if congela_bins==True:
        return

    for i in range(len(hist)):
        if hist[i]>0:
            if i < bin_menor[canal]:
                bin_menor[canal]=i
            elif i>bin_maior[canal]:
                bin_maior[canal]=i
    return
   
def mouse_drawing(event, x, y, flags, params):
    global r, roi_mov, roi_est, frame_roi, lfrom, lto, cfrom, cto
    global bin_menor, bin_maior
    
    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
        reseta_bin()
        
        r = cv2.selectROI("Graphene",frame)
        lfrom=int(r[1])
        lto=int(r[1]+r[3])
        cfrom=int(r[0])
        cto=int(r[0]+r[2])
        
        if event == cv2.EVENT_LBUTTONDOWN:
            roi_mov=True # imagem em movimento
            roi_est=False # estatico
        elif event == cv2.EVENT_RBUTTONDOWN:
            roi_est=True # estatico
            roi_mov=False
            frame_roi=frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

        cv2.destroyAllWindows()    
        cv2.namedWindow("Graphene")
        cv2.setMouseCallback("Graphene", mouse_drawing)

def __draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 3

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

def msg_erro_sintaxe():
    print("Sintaxe correta:")
    print("  > python video_histograma.py POD\n")
    print("  POD=Valor de 1 à 4")
    
try:
    pod=int(sys.argv[1])
    if not (pod>=1 and pod<=4):
        sys.exit(0)
except:
    msg_erro_sintaxe()
    sys.exit(0)

cap = cv2.VideoCapture(pod-1)

# fonte textos
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 0.4
color = (0, 0, 0)
thickness = cv2.FILLED
margin = 2
    
# para histograma em preto e branco, False
hist_rgb=True

# desvia clique para função
cv2.namedWindow("Graphene")
cv2.setMouseCallback("Graphene", mouse_drawing)

# parametros para histograma da area selecionada
roi_mov=False # em movimento
roi_est=False # estatico
frame_roi=""
r=[]
lfrom=0
lto=0
cfrom=0
cto=0

# para encontrar range de bits
bin_menor=[0,1,2]
bin_maior=[0,1,2]
congela_bins=False
analisa_mascara=False
reseta_bin()

plt.ion()

while True:
    ret ,frame = cap.read()
    
    if roi_mov==True:
        frame_roi=frame[lfrom:lto, cfrom:cto]
    elif roi_est!=True:
        frame_roi=frame
        
    plt.clf() # limpa gráfico (ou cla())

    faixa_bin=""
    if (hist_rgb==True):
        # histograma colorido
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([frame_roi],[i],None,[256],[0,256])  # 40x mais rapida que np.histogram
            get_max_min_bin(histr,i)
            plt.plot(histr,color = col)
            faixa_bin=col+":"+str(bin_menor[i])+"/"+str(bin_maior[i])+" "+faixa_bin
            plt.xlim([0,256])
    else:
        # histograma preto e branco
        col="b"
        try:
            frame_roi=cv2.cvtColor(frame_roi, cv2.COLOR_BGR2GRAY)
        except:
            pass
        histr = cv2.calcHist([frame_roi],[0],None,[256],[0,256])
        get_max_min_bin(histr,0)
        plt.plot(histr,color = col)
        faixa_bin=col+":"+str(bin_menor[0])+"/"+str(bin_maior[0])

    if congela_bins == True:
        faixa_bin=faixa_bin+" (congelado)"
    
    plt.xlabel(faixa_bin)

    # exibe frames
    cv2.imshow('Graphene',frame)
    
    if roi_mov==True or roi_est==True:
        cv2.imshow('Selecionado',frame_roi)

        if analisa_mascara==True and (congela_bins == True or roi_est == True):
            mascara=cria_mascara()
            cv2.imshow('Mascara',mascara)
            
    # controle exibição
    plt.pause(0.00001)

    k = cv2.waitKey(1)
    
    if k == 27:
        roi_mov=False
        roi_est=False
        cv2.destroyWindow("Selecionado")
        cv2.destroyWindow("Mascara")
    elif k == ord('r'):
        hist_rgb=True
    elif k == ord('p'):
        hist_rgb=False
    elif k == ord('m'):
        faixa_bin=faixa_bin+" (resetando)"
        plt.xlabel(faixa_bin)
        plt.pause(0.00001)
        time.sleep(0.5)
        reseta_bin()
        cv2.destroyWindow("Mascara")
    elif k == ord('a') and (congela_bins == True or roi_est == True):
        analisa_mascara=True
    elif k == ord('t') and analisa_mascara==True:
        # salva mascara
        
        # defini nome do arquivo
        # fc(x)=faixa de cor (canais) --> MINxMAX(Cor) - Cor:R, G ou B
        fc=""
        if (hist_rgb==True):
            for i,col in enumerate(color):
                if i>0:
                    fc=fc+"_"
                fc=fc+str(bin_menor[i])+"x"+str(bin_maior[i])+col
            fc="fc(3)"+fc
        else:
            fc="fc(1)"+str(bin_menor[0])+"x"+str(bin_maior[0])
        print(fc)
        nome_arquivo="picture_mascara_l"+str(lfrom)+"x"+str(lto)+"_c"+str(cfrom)+"x"+str(cto)+"_"+fc+".png"

        # salva arquivo
        cv2.imwrite(nome_arquivo, mascara)
        __draw_label(frame, "Mascara salva: "+nome_arquivo, (20,20), (255,0,0))
        print("Mascara salva: "+nome_arquivo)
        cv2.imshow('Graphene',frame)
        plt.pause(0.00001)
        time.sleep(5)
        cv2.destroyAllWindows()
        cv2.namedWindow("Graphene")
        cv2.setMouseCallback("Graphene", mouse_drawing)
    elif k == ord('c') and roi_mov==True:
        congela_bins=True
    elif k == ord('d'):
        congela_bins=False
    elif k == 27:
        break

print("Finalizando...")
plt.ioff() # due to infinite loop, this gets never called. 
cap.release()
cv2.destroyAllWindows()
      
