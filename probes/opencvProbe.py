# from probes import atuadoresProbe
# from probes import iptvProbe
# import inspect
# import cv2
# import copy
# import numpy as np
# import threading
# import pathlib
# import time
# import re
# from flask import jsonify, request
# #from skimage.measure import compare_ssim
# #from skimage import measure
# from skimage.metrics import structural_similarity as ssim

# class opencv:
#     def __init__(self):
#         self.freeze_sensib = 50 # qtde quadros necessarios para considerar freeze
#         self.threshold_mt_min = 2500000 # matchTemplate - valor máximo para variável min_val (p/ considerar Match) - anterior: 3900000

#         self.omw_ver = "00.08.27"
#         self.dir_atual = str(pathlib.Path(__file__).parent.absolute())
#         self.dir_images = "\\opencv_assets\\" + self.omw_ver + "\\images\\"
#         self.dir_config = "\\opencv_assets\\" + self.omw_ver + "\\config\\"
#         self.dir_relatorios = "\\opencv_assets\\relatorios\\"

#         self.procCtrl = ""  # processo que está controlando o objeto no momento
#         self.captura = False
#         self.portas_hdmi = 4
#         self.cap = [0] * self.portas_hdmi
#         self.cap_exibir = [False] * self.portas_hdmi
#         self.retCtrl = [0] * self.portas_hdmi
#         self.frameCtrl = [0] * self.portas_hdmi
#         self.timer = {}

#         self.workers = [0] * self.portas_hdmi

#     def capThread(self):
#         tnum = threading.current_thread().name.split("_")[1]
#         print(".. HDMI #" + tnum + ": rodando")

#         while (self.captura == True):
#             self.retCtrl[int(tnum)], self.frameCtrl[int(tnum)] = self.cap[int(tnum)].read()

#             #if k == ord('q'):
#             #    self.captura = False

#         print(".. HDMI #" + tnum + ": parou")

#     def inicializaCaptura(self):
#         # o primeiro metodo que chamou que controla
#         procCaller = inspect.getouterframes(inspect.currentframe(), 2)[1][3]

#         if ( self.procCtrl == "" ):
#             self.procCtrl = procCaller
#         elif ( self.procCtrl != procCaller ):
#             return
#         # proc check - fim

#         self.captura = True

#         for i in range(self.portas_hdmi):
#             self.cap[i] = cv2.VideoCapture(i)

#         self.workers = [threading.Thread(target=self.capThread, args=tuple(), name='thread_' + str(i)) for i in range(self.portas_hdmi)]

#         print("Iniciando captura de tela...")
#         time.sleep(0.5)

#         for worker in self.workers:
#             if (not worker.is_alive()):
#                 worker.start()

#     def finalizaCaptura(self):
#         # o primeiro metodo que chamou que controla
#         procCaller = inspect.getouterframes(inspect.currentframe(), 2)[1][3]

#         if ( self.procCtrl == "" or self.procCtrl != procCaller ):
#             return
#         else:
#             self.procCtrl = ""
#         # proc check - fim

#         self.captura = False

#         #[worker.raise_exception(), worker.join() for worker in self.workers]
#         for worker in self.workers:
#             worker.join()

#         print("Captura de tela finalizada...")

#         for i in range(self.portas_hdmi):
#             self.cap[i].release()

#         cv2.destroyAllWindows()

#     def leTela(self, stbID):
#         #frame = np.copy(self.frameCtrl[int(stbID)])
#         frame = self.frameCtrl[int(stbID)]

#         if (self.cap_exibir[int(stbID)] == True):
#             cv2.imshow('STB ' + str(stbID), frame)

#         k = cv2.waitKey(1)

#         return frame

#     def start_timer(self, oque, silencioso):
#         try:
#             self.timer[oque]
#             if silencioso == False:
#                 print("Timer para '" + oque + "' já iniciado.")
#             return False
#         except:
#             self.timer[oque] = {}
#             self.timer[oque]["s"] = time.perf_counter()

#             if silencioso == False:
#                 print("Timer '" + oque + "' iniciado.")
#             return True

#     def stop_timer(self, oque, silencioso):
#         try:
#             self.timer[oque]
#             self.timer[oque]["e"] = time.perf_counter()
#             tempo = round(self.timer[oque]["e"] - self.timer[oque]["s"], 4)
#             if silencioso == False:
#                 print("Stop timer '" + oque + "'=" + str(tempo))
#             del self.timer[oque]
#             return tempo
#         except:
#             if silencioso == False:
#                 print("Timer " + oque + " nao foi iniciado.")

#         return 0

#     def consulta_timer(self, oque, silencioso):
#         try:
#             self.timer[oque]
#             self.timer[oque]["e"] = time.perf_counter()
#             tempo = round(self.timer[oque]["e"] - self.timer[oque]["s"], 4)

#             if silencioso == False:
#                 print("Consulta: timer '" + oque + "'=" + str(tempo))

#             return tempo
#         except:
#             if silencioso == False:
#                 print("Timer '" + oque + "' nao foi iniciado.")

#         return False

#     def ver_area(self, nome_arquivo):
#         try:
#             area = re.search('_l(\d+)x(\d+)_c(\d+)x(\d+)', nome_arquivo).group(1, 2, 3, 4)
#         except:
#             return (-1, -1, -1, -1)

#         return area

#     def criterio_imagens_dinamicas(self, criterio):  # para imagens em movimento
#         cri_video = []

#         for i in range(len(criterio)):
#             nome_arquivo = criterio[i][0]
#             tipo = criterio[i][1]

#             if (tipo == "video"):
#                 resultado_esperado = criterio[i][2]
#                 area = self.ver_area(nome_arquivo)
#                 cri_video.append([nome_arquivo, area, resultado_esperado])

#         return cri_video

#     def criterio_imagens_estaticas(self, criterio):
#         cri_img = []

#         for i in range(len(criterio)):
#             nome_arquivo = criterio[i][0]
#             tipo = criterio[i][1]

#             if (tipo != "video"):
#                 resultado_esperado = criterio[i][2]
#                 area = self.ver_area(nome_arquivo)
#                 img_color = cv2.imread(self.dir_atual + self.dir_images + nome_arquivo)
#                 img_pb = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
#                 cri_img.append([nome_arquivo, img_color, img_pb, area, tipo, resultado_esperado])

#         return cri_img

#     def extrai_faixa_cores(self, nome_arquivo):
#         prop_masc = []
#         canais = int(re.search('_fc\((\d+)\)', nome_arquivo).group(1))

#         if canais == 1:
#             fc = re.search('fc\(.\)(\d+)x(\d+)', nome_arquivo).group(1, 2)
#         elif canais == 3:
#             fc = re.search('fc\(.\)(\d+)x(\d+)b_(\d+)x(\d+)g_(\d+)x(\d+)r', nome_arquivo).group(1, 2, 3, 4, 5, 6)
#         else:
#             return False

#         return fc

#     def compara_imagens(self, imgs, frame):
#         # nome_arquivo,img_file,area,tela_preta,resultado_esperado

#         c = len(imgs)
#         matches = 0

#         #print("1 - imgs:" + str(imgs))
#         #cv2.imshow('compara_imagens frame', frame)
#         #cv2.waitKey(1)

#         for img in imgs:
#             nome_arquivo = img[0]
#             lde = int(img[3][0])
#             lpara = int(img[3][1])
#             cde = int(img[3][2])
#             cpara = int(img[3][3])
#             tipo = img[4]
#             resultado_esperado = img[5]

#             if not (lde == -1 and lpara == -1 and cde == -1 and cpara == -1):
#                 roi_col = frame[lde:lpara, cde:cpara]
#                 roi_pb = cv2.cvtColor(roi_col, cv2.COLOR_BGR2GRAY)
#             else:
#                 frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 tipo = "sem_coordenada"

#             if (tipo == "telapreta"):
#                 if (resultado_esperado == True):
#                     if cv2.countNonZero(roi_pb) == 0:  # tela preta
#                         matches = matches + 1
#                 else:
#                     if not (cv2.countNonZero(roi_pb) == 0):
#                         matches = matches + 1

#             elif tipo == "mascara":
#                 fc = self.extrai_faixa_cores(nome_arquivo)

#                 if (len(fc) / 2 == 3):
#                     mascara = self.cria_mascara(fc, roi_col)
#                 else:
#                     mascara = self.cria_mascara(fc, roi_pb)

#                 #(score, diff) = compare_ssim(mascara, img[2], full=True)
#                 (score, diff) = ssim(mascara, img[2], full=True)
#                 diff = (diff * 255).astype("uint8")

#                 if (resultado_esperado == True):
#                     if (score >= 0.93):
#                         matches = matches + 1
#                 else:
#                     if not (score >= 0.93):
#                         matches = matches + 1

#             elif tipo == "sem_coordenada":
#                 result = self.match_figura(img[1], frame)

#                 if (resultado_esperado == True and result == True):
#                     matches = matches + 1
#                 elif (resultado_esperado == False and result == False):
#                     matches = matches + 1

#             else:  # imagem estática
#                 #(score, diff) = measure.compare_ssim(roi_pb, img[2], full=True)
#                 (score, diff) = ssim(roi_pb, img[2], full=True)
#                 diff = (diff * 255).astype("uint8")

#                 if (resultado_esperado == True):
#                     if (score == 1):
#                         matches = matches + 1
#                 else:
#                     if not (score == 1):
#                         matches = matches + 1

#         #print("True:" + tipo + " " + str(matches) + " " + str(c))
#         if (matches == c):
#             return True
#         else:
#             return False

#     def cria_mascara(self, fc, frame):
#         # fc=faixa de cores, podendo ser imagens de 1 canal (preto e branco) ou colorida (3 canais)

#         frm = copy.deepcopy(frame)

#         canais = int(len(fc) / 2)

#         bin_menor = [0] * canais
#         bin_maior = [0] * canais

#         if canais == 3:
#             bin_menor[0] = int(fc[0])
#             bin_menor[1] = int(fc[2])
#             bin_menor[2] = int(fc[4])
#             bin_maior[0] = int(fc[1])
#             bin_maior[1] = int(fc[3])
#             bin_maior[2] = int(fc[4])

#             linhas, colunas, canais = frm.shape

#             for l in range(linhas):
#                 for co in range(colunas):
#                     if (frm.item(l, co, 0) >= bin_menor[0] and frm.item(l, co, 0) <= bin_maior[0] and
#                             frm.item(l, co, 1) >= bin_menor[1] and frm.item(l, co, 1) <= bin_maior[1] and
#                             frm.item(l, co, 2) >= bin_menor[2] and frm.item(l, co, 2) <= bin_maior[2]):
#                         frm.itemset((l, co, 0), 0)
#                         frm.itemset((l, co, 1), 0)
#                         frm.itemset((l, co, 2), 0)
#                     else:
#                         frm.itemset((l, co, 0), 255)
#                         frm.itemset((l, co, 1), 255)
#                         frm.itemset((l, co, 2), 255)

#         else:
#             bin_menor[0] = int(fc[0])
#             bin_maior[0] = int(fc[1])

#             linhas, colunas = frm.shape

#             for l in range(linhas):
#                 for co in range(colunas):
#                     if frm.item(l, co) >= bin_menor[0] and frm.item(l, co) <= bin_maior[0]:
#                         frm.itemset((l, co), 0)
#                     else:
#                         frm.itemset((l, co), 255)

#         if (len(frm.shape) == 3):
#             frm = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

#         return frm

#     def match_figura(self, ref, frame):
#         # ATENÇÃO NESTA FUNÇÃO: O THRESHOLD PARA CONSIDERAR UM SEGMENTO DE IMAGEM IGUAL SEM COORDENADA.
#         # procura no frame trecho de imagem contida em ref

#         frm = copy.deepcopy(frame)

#         method = eval('cv2.TM_SQDIFF')

#         res = cv2.matchTemplate(frm, ref, method)

#         # cv2.imshow('frm',frm)
#         # cv2.imshow('ref',ref)

#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

#         res_min = min_val < self.threshold_mt_min
#         # res_max = max_val < self.threshold_mt_max

#         tmatch = False

#         # print(str(self.threshold_mt_min),min_val)
#         # if (min_val < self.threshold_mt_min and max_val < self.threshold_mt_max):
#         if (min_val < self.threshold_mt_min):
#             tmatch = True
#         else:
#             tmatch = False

#         # print (str(min_val)+" "+str(max_val)+" ("+str(res_min)+"/"+str(res_max)+") Match="+str(tmatch))
#         # print (str(min_val)+" "+str(max_val)+" ("+str(res_min)+") Match="+str(tmatch))

#         return tmatch

#     def ondeEstou(self, stbID):
#         # retorna posicao da tela Graphene

#         if (self.aguardaTela(stbID, [['componentes_destaques.png', "imagem", True],
#                           ['componentes_vivoplay_csd_l81x103_c490x576_fc(3)253x253b_253x253g_253x253r.png', "mascara",
#                            True]], 1) != False):
#             onde = "tela_inicial"
#         elif (self.aguardaTela(stbID, [['tela_sair.png', "imagem", True]], 1) != False):
#             onde = "tela_sair"
#         elif (self.aguardaTela(stbID, [['booting_logo_vivo.png', "imagem", True]], 1) != False):
#             onde = "booting"
#         elif (self.aguardaTela(stbID, [['booting_senha_administrador_l168x275_c154x473.png', "imagem", True]], 1) != False):
#             onde = "senha_administrador"
#         elif (self.aguardaTela(stbID, [['booting_computador_andando.png', "imagem", True]], 1) == False):
#             onde = "booting"
#         elif (self.aguardaTela(stbID, [['sem_sinal_hdmi.png', "imagem", True]], 1) == False):
#             onde = "booting"
#         elif (self.aguardaTela(stbID, [['graphene_busca_l144x254_c85x551.png', "imagem", True]], 1) == False):
#             onde = "funcao_busca"
#         elif (self.aguardaTela(stbID, [['pergunta_deseja_sair_l159x316_c206x427.png', "imagem", True]], False) == True):
#             onde = "pergunta_sair"
#         elif (self.aguardaTela(stbID, [['botao_fechar.png', "imagem", True]], 1) == False):
#             onde = "fechar"
#         else:
#             onde = "indeterminado"

#         return onde

#     def posicionarGraphene(self, stbID, boot):
#         # posiciona a tela no mesmo ponto quando o STB acaba de ser ligado
#         # boot = True/False --> Reiniciar o STB eletricamente caso não esta respondendo ao posicionar a Graphene?

#         self.inicializaCaptura()
#         self.cap_exibir[int(stbID)] = True

#         print("\nPosicionando interface Graphene")

#         iptvObj = iptvProbe.iptv()
#         atuadoresObj = atuadoresProbe.atuadores()

#         if (atuadoresObj.reguaAPCLigaDesliga(iptvObj.ip_switch_hpe, (int(stbID) + 1), "status") == "OFF"):
#             print ("STB está desligando. Ligando-o,")
#             atuadoresObj.reguaAPCLigaDesliga(iptvObj.ip_switch_hpe, (int(stbID) + 1), "liga")

#         sair = False
#         tent = 1
#         respTela = False

#         while (sair == False):
#             if tent > 3 and boot == True:
#                 print("STB aparentemente travado. Reiniciando-o.")
#                 atuadoresObj.reguaAPCLigaDesliga(iptvObj.ip_switch_hpe, (int(stbID) + 1), "desliga")
#                 time.sleep(1)
#                 atuadoresObj.reguaAPCLigaDesliga(iptvObj.ip_switch_hpe, (int(stbID) + 1), "liga")
#                 time.sleep(7)
#                 tent = 1
#                 boot = False
#                 continue
#             elif tent > 3 and boot == False:
#                 sair = True
#                 continue
#             else:
#                 tent = tent + 1

#             tela = self.ondeEstou(stbID)

#             print ("Tela atual:" + tela)

#             if tela == "booting" or tela == "tela_inicial":
#                 if tela == "booting":
#                     print("STB em inicialização. Aguarde!")

#                 print("Aguardando conteúdo no STB.")

#                 respTela = self.aguardaTela(stbID, [['componentes_destaques.png', "imagem", True],
#                                 ['tela_inicial_area_video_tot_l65x280_c33x640.png', "video", True],
#                                 ['color_bar_l90x150_c7x378.png', "imagem", False],
#                                 ['erro_gcn11.png', "imagem", False],
#                                 ['componentes_vivoplay_csd_l81x103_c490x576_fc(3)253x253b_253x253g_253x253r.png', "mascara", True],
#                                 ['tela_inicial_area_video_dir_l133x263_c463x608.png', "telapreta", False],
#                                 ['erro_gcn11_2_l175x187_c384x454.png', "imagem", False]],180)
#                 if (respTela != False):
#                     print("Graphene posicionada (Ok).")
#                     sair = True
#             elif tela == "tela_sair":
#                 print("Responder se deseja sair: sim.")
#                 atuadoresObj.irtransComando(stbID, "left_arrow")
#                 time.sleep(1)
#                 atuadoresObj.irtransComando(stbID, "ok_button")
#                 time.sleep(2)
#             elif tela == "pergunta_sair":
#                 print("Saindo.")
#                 atuadoresObj.irtransComando(stbID, "back")
#                 time.sleep(1)
#             elif tela == "fechar":
#                 print("Fechando.")
#                 atuadoresObj.irtransComando(stbID, "ok_button")
#                 time.sleep(0.5)
#                 atuadoresObj.irtransComando(stbID, "back")
#                 time.sleep(0.5)
#                 atuadoresObj.irtransComando(stbID, "back")
#                 time.sleep(0.5)
#                 atuadoresObj.irtransComando(stbID, "back")
#                 time.sleep(0.5)
#                 atuadoresObj.irtransComando(stbID, "menu")
#                 time.sleep(1)
#             elif tela == "senha_administrador":
#                 print("Deseja sair? Sim.")
#                 atuadoresObj.irtransComando(stbID, "left_arrow")
#                 time.sleep(1)
#                 atuadoresObj.irtransComando(stbID, "ok_button")
#                 time.sleep(2)
#             else:
#                 print("Tentando voltar para tela inicial.")
#                 atuadoresObj.irtransComando(stbID, "menu")
#                 time.sleep(1)
#                 atuadoresObj.irtransComando(stbID, "menu")
#                 time.sleep(1)
#                 atuadoresObj.irtransComando(stbID, "back")
#                 time.sleep(2)

#         self.finalizaCaptura()

#     def aguardaTela(self, stbID, criterio, tempo_maximo):
#         # ======================
#         # Função aguardaTela()
#         # ======================
#         # criterio = array[["nomearquivo.png","imagem|video|mascara|telapreta",True/False]["nomearquivo",...]...]
#         #    "nomearquivo.png" --> nome do arquivo à ser comparado, sendo que formato deve ser:
#         #            nome_l361x386_c14x33.png, onde os valores de L definem de qual a qual linha é a área da imagem, e C faz o mesmo para coluna. Ou seja, é a área da imagem na tela, ou..
#         #            nome.png, sem coordenadas, essa imagem será procurada na tela. É um tipo de busca mais lenta.
#         #    "imagem|video|mascara|telapreta" --> tipo do arquivo
#         #    Resultado esperado --> depende do campo anterior, sendo:
#         #       imagem    --> True=area da tela deve ter imagem igual a do arquivo | False=imagem deve ser diferente da do arquivo
#         #       video     --> True=area analisada deve ser em movimento | False=area analisada deve estar freezada
#         #       mascara   --> True=a masca da área deve ser igual a mascara do arquivo | False=as máscaras não devem coincidir
#         #       telapreta --> True=área da imagem deve ser preta | False=imagem deve ser diferente de preta
#         #
#         # tempo_maximo = tempo máximo à esperar em segundos

#         self.inicializaCaptura()
#         self.cap_exibir[int(stbID)] = True

#         tempo_maximo = int(tempo_maximo)

#         cri_img = self.criterio_imagens_estaticas(criterio)
#         cri_video = self.criterio_imagens_dinamicas(criterio)

#         sair_img = False
#         sair_video = False
#         res_img = False
#         res_video = False

#         self.start_timer("tela", True)

#         tempo_med = 0

#         while ((sair_img == False or sair_video == False) and tempo_med <= tempo_maximo):
#             #print("1 - res_video/res_img/sair_img/sair_video:" + str(res_video) + str(res_img) + str(sair_img) + str(res_video))

#             sair_img = False
#             sair_video = False

#             # compara imagem estática
#             if (len(cri_img) > 0 and sair_img == False):
#                 frame = self.leTela(stbID)

#                 if self.compara_imagens(cri_img, frame) == True:  # imagens a comparar por coordenada
#                     res_img = True
#                     # print("Aguardando tela - imagem(ns) Ok")
#                 else:
#                     res_img = False

#             # verifica se imagem (sub) é dinâmica / vídeo - mede por um tempo
#             if (len(cri_video) > 0):
#                 mov = [0] * len(cri_video)

#                 for j in range(self.freeze_sensib):
#                     frame = self.leTela(stbID)
#                     time.sleep(0.02)
#                     frame2 = self.leTela(stbID)

#                     for i in range(len(cri_video)):
#                         lde = int(cri_video[i][1][0])
#                         lpara = int(cri_video[i][1][1])
#                         cde = int(cri_video[i][1][2])
#                         cpara = int(cri_video[i][1][3])

#                         area_atu = cv2.cvtColor(frame[lde:lpara, cde:cpara], cv2.COLOR_BGR2GRAY)
#                         area_ant = cv2.cvtColor(frame2[lde:lpara, cde:cpara], cv2.COLOR_BGR2GRAY)

#                         #(score, diff) = compare_ssim(area_ant, area_atu, full=True)
#                         (score, diff) = ssim(area_ant, area_atu, full=True)
#                         diff = (diff * 255).astype("uint8")

#                         if not (score == 1):
#                             mov[i] = mov[i] + 1

#                 movimento = True

#                 for i in mov:
#                     porc_mov = (i / self.freeze_sensib * 100)

#                     if (porc_mov < 50): # se movimento foi menor que 50% do tempo, false
#                         movimento = False
#                         break

#                 if (movimento == False):
#                     res_img = False
#                     res_video = False
#                     sair_video = False
#                     sair_img = False
#                 else:
#                     res_video = True
#             else:
#                 res_video = True

#             if res_img == True and res_video == True:
#                 sair_img = True
#                 sair_video = True
#                 print("Aguardando tela - img/video(s) Ok")

#             tempo_med = self.consulta_timer("tela", True)

#         self.stop_timer("tela", True)
#         self.finalizaCaptura()

#         if (res_img == True and res_video == True):
#             return tempo_med
#         else:
#             return False