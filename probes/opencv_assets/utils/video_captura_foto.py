import sys
import numpy as np
import cv2

def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        r = cv2.selectROI("Graphene",frame)
        
        selecao = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        lfrom=int(r[1])
        lto=int(r[1]+r[3])
        cfrom=int(r[0])
        cto=int(r[0]+r[2])
        print ("Selecao (l:l c:c): "+str(lfrom)+":"+str(lto)+" "+str(cfrom)+":"+str(cto))
        cv2.imshow("Selecao", selecao)
        #cv2.waitKey(0)

        nome_arquivo="picture_area_l"+str(lfrom)+"x"+str(lto)+"_c"+str(cfrom)+"x"+str(cto)+".png"
        print("Salvando area:"+nome_arquivo+".")
        cv2.imwrite(nome_arquivo, selecao)
        print("Concluido.")
        cv2.destroyAllWindows()
        
        cv2.namedWindow("Graphene")
        cv2.setMouseCallback("Graphene", mouse_drawing)

cv2.namedWindow("Graphene")
cv2.setMouseCallback("Graphene", mouse_drawing)

pod=int(sys.argv[1])

cap = cv2.VideoCapture(pod-1)

i=0
while(1):
    ret ,frame = cap.read()
    
    #frame=frame[85:490, 0:720]

    cv2.imshow('Graphene',frame)

    if cv2.waitKey(1) == 27:
        break
    
    if cv2.waitKey(1) == ord('t'):
        i=i+1
        nome_arquivo="picture_full_"+str(i)+".png"
        cv2.imwrite(nome_arquivo, frame)
        print("Imagem "+nome_arquivo+" salva!")
        
    if cv2.waitKey(1) == ord('q'):
        break

print("Finalizando...") 

cap.release()
cv2.destroyAllWindows()