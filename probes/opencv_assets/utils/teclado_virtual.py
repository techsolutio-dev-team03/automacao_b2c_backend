# cria config do teclado virtual (ex: Netflix, Vivo Play), para que o OpenCV possa
# digitar a senhas dinamicamente.
import sys
sys.path.append('..\\comum')
import parametros as p
import funcoes_gerais as fg
import funcoes_visuais as fv
import controle_remoto as cr
import variaveis as var
import json
import ast
import cv2
import time
import matplotlib.pyplot as plt

def iniciar(cfg,nome_teclado):
    global teclas, funcoes, areas, porta_hdmi
    
    # cfg = array com os arquivos de configuração a ser usado
    # nome_teclado = como se referenciar ao tv
    
    var.tv_teclas[nome_teclado] = {}
    var.tv_funcoes[nome_teclado] = {}
    var.tv_areas[nome_teclado] = {}
    
    cnt_cfg=""
    
    for c in cfg:
        f = open(p.dir_config+c,'r', encoding='utf-8')
        cnt_cfg=f.read()
        f.close()
        
        ary_tmp=ast.literal_eval(cnt_cfg)
        
        for e in ary_tmp["tecla"]:
            var.tv_teclas[nome_teclado][e]=ary_tmp["tecla"][e]
            if ary_tmp["tecla"][e][4]=="funcao_sim":

                try:
                    var.tv_funcoes[nome_teclado][e]
                except:
                    var.tv_funcoes[nome_teclado][e]="nao_selecionado"
                    
        for a in ary_tmp["area"]:
            try:
                var.tv_areas[nome_teclado][a]
            except:
                var.tv_areas[nome_teclado][a]=ary_tmp["area"][a]
                
def qual_funcao_ativa(nome_teclado):
    for f in var.tv_funcoes[nome_teclado]:
        if (f=="<shift>" or f=="<unshift>"):
            continue
        
        if var.tv_funcoes[nome_teclado][f]=="selecionado":
            return f
            
    return "raiz"
    
def detecta_tecla_selecionada(nome_teclado):
    #global var.tv_funcoes, var.tv_teclas, 
    #global cap
    cap = cv2.VideoCapture(var.porta_hdmi)
    
    funcao_ativa = qual_funcao_ativa(nome_teclado)
    
    for t in var.tv_teclas[nome_teclado]:
        if var.tv_teclas[nome_teclado][t][5] != funcao_ativa:
            continue
            
        ret, frame = cap.read()
                
        lde=var.tv_teclas[nome_teclado][t][0]
        late=var.tv_teclas[nome_teclado][t][0]+var.tv_teclas[nome_teclado][t][1]
        cde=var.tv_teclas[nome_teclado][t][2]
        cate=var.tv_teclas[nome_teclado][t][2]+var.tv_teclas[nome_teclado][t][3]

        tecla=frame[lde:late,cde:cate]
                
        tecla=cv2.cvtColor(tecla, cv2.COLOR_BGR2GRAY)
        
        histr = cv2.calcHist([tecla],[0],None,[256],[0,256])
        
        escuro=0
        claro=0
        
        for i in range(len(histr)):
            if 30 <= i <= 40:
                escuro=escuro+histr[i][0]
            elif 175 <= i <= 230:
                claro=claro+histr[i][0]

        porc_claro=round(claro/(claro+escuro)*100,0)
        
        if porc_claro > 50:
            # Para debug. Não apagar!
            #fv.atualiza_tela()
            #print("tecla",nome_teclado,var.tv_teclas[nome_teclado][t],t)
            #ret ,frame = cap.read()
            #cv2.imshow('tec',tecla)
            #cv2.waitKey(1)
            #time.sleep(3)
            return t
         
        # Para debug. Não apagar!
        #print("tecla",nome_teclado,var.tv_teclas[nome_teclado][t],t,porc_claro)
        #ret ,frame = cap.read()
        #cv2.imshow('tec',tecla)
        #cv2.waitKey(1)
        #time.sleep(0.2)
    return False
    
def navegar_teclado(tecla_destino,nome_teclado):
    # navega até a tecla, e pressiona Ok
    
    plde,plate,pcde,pcate,pf = coordenadas_tecla(tecla_destino,nome_teclado)

    while True:
        fv.atualiza_tela()

        tec_sel=False

        while tec_sel==False:
            tec_sel=detecta_tecla_selecionada(nome_teclado)

        if tec_sel==tecla_destino:
            #fg.log_tela("Pressionando '"+tecla_destino+"'.")
            time.sleep(0.2)
            cr.chama_irtrans("OK_BUTTON",var.pod)
            time.sleep(0.2)
            fv.atualiza_tela()
            break
            
        else:
            h_tmp     = "" # tecla mais proxima horizontal
            h_dist    = 0 # distancia horizontal tecla de destino para a de origem
            h_sentido = "" # para onde ir na horizontal
            v_tmp     = "" # tecla mais proxima vertical
            v_dist    = 0 # distancia vertical tecla de destino para a de origem
            v_sentido = "" # para onde ir na vertical
            
            h_tmp, h_dist, h_sentido  = tecla_mais_proxima(tec_sel, tecla_destino, "h", nome_teclado)

            while tec_sel != h_tmp:
                cr.chama_irtrans(h_sentido,var.pod)
                fv.atualiza_tela()
                time.sleep(0.3)
                tec_sel=False
                while tec_sel==False:
                    tec_sel=detecta_tecla_selecionada(nome_teclado)
                h_tmp, h_dist, h_sentido  = tecla_mais_proxima(tec_sel, tecla_destino, "h", nome_teclado)

            v_tmp, v_dist, v_sentido  = tecla_mais_proxima(tec_sel, tecla_destino, "v", nome_teclado)
            
            while tec_sel != v_tmp:
                cr.chama_irtrans(v_sentido,var.pod)
                time.sleep(0.3)
                fv.atualiza_tela()
                tec_sel=False
                while tec_sel==False:
                    tec_sel=detecta_tecla_selecionada(nome_teclado)
                v_tmp, v_dist, v_sentido  = tecla_mais_proxima(tec_sel, tecla_destino, "v", nome_teclado)


    
def funcao_selecionada(nome_teclado):
    for f in var.tv_funcoes[nome_teclado]:
        if var.tv_funcoes[nome_teclado][f] == "selecionado":
            return f
            
    return "raiz"


def tecla_mais_proxima(tecla_origem, tecla_destino, direcao,nome_teclado):
    # dada a direcao, tecla_origem e tecla_destino, retorna a tecla mais proxima de destino, o sentido (esqueda,direita), e a distancia em pontos
    # direcao = h (horizontal) ou v (vertical)
    #
    # retorna --> tecla_mais_proxima,distancia,sentido
    
    sl_coord_de,sl_coord_ate,sc_coord_de,sc_coord_ate,_ = coordenadas_tecla(tecla_origem,nome_teclado) # sc_ selecionada / coluna   
    dl_coord_de,dl_coord_ate,dc_coord_de,dc_coord_ate,_ = coordenadas_tecla(tecla_destino,nome_teclado) # dl_ = tecla de destino / linha
    
    func_sel = funcao_selecionada(nome_teclado)
    teclas_dir=[]
    
    # cria lista de teclas na mesma direção (v ou h)
    for t in var.tv_teclas[nome_teclado]:
        if (var.tv_teclas[nome_teclado][t][5] == func_sel):
            al_coord_de,al_coord_ate,ac_coord_de,ac_coord_ate,_ = coordenadas_tecla(t,nome_teclado) # ac_ = tecla analisada coluna / al_ = tecla analisada linha
                
            if direcao=="h":
                if (((al_coord_de  >= sl_coord_de and al_coord_de  <= sl_coord_ate) or
                     (al_coord_ate >= sl_coord_de and al_coord_ate <= sl_coord_ate)) 
                   or
                    ((sl_coord_de  >= al_coord_de and sl_coord_de <= al_coord_ate) or
                     (sl_coord_ate >= al_coord_ate and sl_coord_ate <= al_coord_ate))):
                    teclas_dir.append(t)
                    
            elif direcao=="v":
                if (((ac_coord_de >= sc_coord_de  and ac_coord_de <= sc_coord_ate) or
                     (ac_coord_ate>= sc_coord_de  and ac_coord_ate <= sc_coord_ate))
                   or
                    ((sc_coord_de >= ac_coord_de  and sc_coord_de <= ac_coord_ate) or
                     (sc_coord_ate >= ac_coord_de and sc_coord_ate <= ac_coord_ate))):
                    teclas_dir.append(t)

    # verifica qual a tecla mais proxima na mesma direção
    tecla_mais_proxima=""
    tecla_mais_proxima_coord_de=0
    distancia_menor=999999
    distancia_positiva_atu=999999
    distancia_positiva_ant=999999
    sentido=""

    for t in teclas_dir:
        al_coord_de,al_coord_ate,ac_coord_de,ac_coord_ate,_ = coordenadas_tecla(t,nome_teclado) # ac_ = tecla analisada coluna / al_ = tecla analisada linha

        if direcao=="h":
            if (((ac_coord_de  >= dc_coord_de  and ac_coord_de  <= dc_coord_ate) or
                 (ac_coord_ate >= dc_coord_de  and ac_coord_ate <= dc_coord_ate))
               or
                ((dc_coord_de >= ac_coord_de   and dc_coord_de <= ac_coord_ate) or
                 (dc_coord_ate >= ac_coord_de  and dc_coord_ate <= ac_coord_ate))):
                tecla_mais_proxima=t
                tecla_mais_proxima_coord_de=ac_coord_de
                distancia_positiva_ant=0
                distancia_menor=0
                h_encontrou=True
            else:
                distancia_positiva_atu=ac_coord_de-dc_coord_de
                
                if (distancia_positiva_atu < 0):
                    distancia_positiva_atu=distancia_positiva_atu*-1
                    
                if distancia_positiva_atu < distancia_positiva_ant:
                    tecla_mais_proxima=t
                    tecla_mais_proxima_coord_de=ac_coord_de
                    distancia_menor=ac_coord_de-dc_coord_de
                    distancia_positiva_ant=distancia_positiva_atu

        elif direcao=="v":
            if (((al_coord_de  >= dl_coord_de  and al_coord_de  <= dl_coord_ate) or
                 (al_coord_ate >= dl_coord_de  and al_coord_ate <= dl_coord_ate))
               or
                ((dl_coord_de >= al_coord_de   and dl_coord_de <= al_coord_ate) or
                 (dl_coord_ate >= al_coord_de  and dl_coord_ate <= al_coord_ate))):
                tecla_mais_proxima=t
                tecla_mais_proxima_coord_de=al_coord_de
                distancia_positiva_ant=0
                distancia_menor=0
                h_encontrou=True
            else:
                distancia_positiva_atu=al_coord_de-dl_coord_de
                
                if (distancia_positiva_atu < 0):
                    distancia_positiva_atu=distancia_positiva_atu*-1
                    
                if distancia_positiva_atu < distancia_positiva_ant:
                    tecla_mais_proxima=t
                    tecla_mais_proxima_coord_de=al_coord_de
                    distancia_menor=al_coord_de-dl_coord_de
                    distancia_positiva_ant=distancia_positiva_atu
            
    if direcao=="h":
        if (tecla_mais_proxima_coord_de-sc_coord_de) < 0:
            sentido="LEFT_ARROW"
        elif (tecla_mais_proxima_coord_de-sc_coord_de) > 0:
            sentido="RIGHT_ARROW"
    elif direcao=="v":
        if (tecla_mais_proxima_coord_de-sl_coord_de) < 0:
            sentido="UP_ARROW"
        elif (tecla_mais_proxima_coord_de-sl_coord_de) > 0:
            sentido="DOWN_ARROW"

    distancia=distancia_menor

    return tecla_mais_proxima,distancia,sentido
    

def digitar(texto,nome_teclado):
    fv.atualiza_tela()

    fg.log_tela("Teclado virtual - digitando:"+texto)
    
    for l in texto:
        # tecla de destino (para)
        plde,plate,pcde,pcate,pf = coordenadas_tecla(l,nome_teclado) #plde=para linhe de, pf=para a funcao
     
        # origem (tecla selecionada)
        tec_sel=detecta_tecla_selecionada(nome_teclado)
        slde,slate,scde,scate,sf = coordenadas_tecla(l,nome_teclado) #scate=selecionada coluna ate
               
        # se for necessario acionar funcao (ex: shift, simbolos, etc, navega até lá)            
        if sf != pf and pf!="<shift>" and pf!="<unshift>":
            if var.tv_funcoes[nome_teclado][l] != "selecionado":
                flde,flate,fcde,fcate,ff = coordenadas_tecla(pf,nome_teclado) # flde=funcao linha de, ff=funcao da funcao

                navegar_teclado(pf,nome_teclado)
                
                for f in var.tv_funcoes[nome_teclado]:
                    if f != "<shift>" and f != "<unshift>":
                        var.tv_funcoes[nome_teclado][f]= "nao_selecionado"
                    
                var.tv_funcoes[nome_teclado][pf]= "selecionado"
        if l.isupper() == True and var.tv_funcoes[nome_teclado]["<shift>"]=="nao_selecionado":
            flde,flate,fcde,fcate,ff = coordenadas_tecla("<shift>",nome_teclado) # flde=funcao linha de, ff=funcao da funcao
            navegar_teclado(pf,nome_teclado)
            var.tv_funcoes[nome_teclado]["<shift>"]=="selecionado"
        elif l.isupper() == False and var.tv_funcoes[nome_teclado]["<shift>"]=="selecionado":
            flde,flate,fcde,fcate,ff = coordenadas_tecla("<unshift>",nome_teclado) # flde=funcao linha de, ff=funcao da funcao
            navegar_teclado(pf,nome_teclado)
            var.tv_funcoes[nome_teclado]["<shift>"]=="nao_selecionado"

        navegar_teclado(l,nome_teclado)
        fv.atualiza_tela()

    
def coordenadas_tecla(tecla,nome_teclado):
    global teclas
    
    try:
        var.tv_teclas[nome_teclado][tecla]
    except:
        fg.log_tela("Posição não encontrada no teclado: "+nome_teclado+"/"+tecla)
        return False
        
    lde=var.tv_teclas[nome_teclado][tecla][0]
    late=var.tv_teclas[nome_teclado][tecla][0]+var.tv_teclas[nome_teclado][tecla][1]
    cde=var.tv_teclas[nome_teclado][tecla][2]
    cate=var.tv_teclas[nome_teclado][tecla][2]+var.tv_teclas[nome_teclado][tecla][3]
    f=var.tv_teclas[nome_teclado][tecla][5]
    
    return lde,late,cde,cate,f
    