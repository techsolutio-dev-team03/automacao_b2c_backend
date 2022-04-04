#include <SPI.h>
#include <Ethernet.h>

unsigned long stTime;

String readString;
//boolean incoming = 0;

int thrLEDOff = 8;

int anPin1 = A0;
int anPin2 = A1;
int anPin3 = A2;
int anPin4 = A3;
int anPin5 = A4;
int anPin6 = A5;

int Relay1 = 2;
int Relay2 = 3;
int Relay3 = 4;
int Relay4 = 5;

int analogValue = 0;

byte mac[] = { 0x00, 0xAA, 0xBB, 0xCC, 0xDA, 0x02 };
IPAddress ip(192,168,16,14); //

EthernetServer server(80);

void setup()
{
  pinMode(Relay1, OUTPUT); 
  pinMode(Relay2, OUTPUT); 
  pinMode(Relay3, OUTPUT); 
  pinMode(Relay4, OUTPUT); 

  // Para inverter a lógica
  digitalWrite(Relay1, HIGH);
  digitalWrite(Relay2, HIGH);
  digitalWrite(Relay3, HIGH);
  digitalWrite(Relay4, HIGH);

  Ethernet.begin(mac, ip);
  server.begin();
  
  Serial.begin(9600);
}

void loop()
{
    EthernetClient client = server.available(); 
    
    if (client) { 
        while (client.connected()) { 
            if (client.available()) { 
                char c = client.read();

                if (readString.length() < 100) {
                    readString += c; 
                }

                if (c == 0x0D) { 
                    String cmd = getValue(readString,'_',1);

                    if (cmd == "ligaDesliga") {
                      ///////////////////////////////////
                      // Liga / Desliga com repetição.
                      //
                      String regua= getValue(readString,'_',2);
                      int espera_des = (getValue(readString,'_',3)).toInt();
                      int espera_lig = (getValue(readString,'_',4)).toInt();
                      int repete = (getValue(readString,'_',5)).toInt();
                      
                      for (int i=1; i<=repete; i++) {
                        // ### DESLIGA ###

                        if(regua.indexOf("1") > -1) // Régua 1
                        { 
                          digitalWrite(Relay1, LOW);   
                        } 
                        if(regua.indexOf("2") > -1) 
                        { 
                          digitalWrite(Relay2, LOW);  // Régua 2
                        } 
                        if(regua.indexOf("3") > -1) 
                        { 
                          digitalWrite(Relay3, LOW);  // Régua 3 (O relay individual não está com a lógica invertida (normalmente fechado/aberto)
                        }
                        if(regua.indexOf("4") > -1) 
                        { 
                          digitalWrite(Relay4, LOW);  // Régua 4 (O relay individual não está com a lógica invertida (normalmente fechado/aberto)
                        }
                        
                        // ### ESPERA ###
                        delay(espera_des);
                        
                        // ### RELIGA ###
                        if(regua.indexOf("1") > -1) // Régua 1
                        { 
                          digitalWrite(Relay1, HIGH);  
                        } 
                        if(regua.indexOf("2") > -1) // Régua 2
                        { 
                          digitalWrite(Relay2, HIGH);  
                        }
                        if(regua.indexOf("3") > -1) // Régua 3
                        { 
                          digitalWrite(Relay3, HIGH);  
                        } 
                        if(regua.indexOf("4") > -1) // Régua 4
                        { 
                          digitalWrite(Relay4, HIGH);  
                        } 
                        delay(espera_lig);
                      }
                      retornaHTTP(client, "OK");
                    }
                    else if (cmd == "pressSimult") {
                      ///////////////////////////////////
                      // Pressiona botao simultaneamente.
                      //
                      
                      int rele1 = (getValue(readString,'_',2)).toInt();
                      int rele2 = (getValue(readString,'_',3)).toInt();
                      int rele3 = (getValue(readString,'_',4)).toInt();
                      int tempo = (getValue(readString,'_',5)).toInt();

                      if(rele1 == 1 || rele2 == 1 || rele3 == 1) { 
                        digitalWrite(Relay1, LOW);   
                      } 
                      if(rele1 == 2 || rele2 == 2 || rele3 == 2) {
                        digitalWrite(Relay2, LOW);   
                      }
                      if(rele1 == 3 || rele2 == 3 || rele3 == 3) {
                        digitalWrite(Relay3, LOW);   
                      }
                      
                      delay(tempo);

                      if(rele1 == 1 || rele2 == 1 || rele3 == 1) { 
                        digitalWrite(Relay1, HIGH);   
                      } 
                      if(rele1 == 2 || rele2 == 2 || rele3 == 2) {
                        digitalWrite(Relay2, HIGH);   
                      }
                      if(rele1 == 3 || rele2 == 3 || rele3 == 3) {
                        digitalWrite(Relay3, HIGH);   
                      }

                      retornaHTTP(client, "OK");
                    }
                    else if (cmd == "medeLuzFreqIntermit") {
                      ///////////////////////////////////////////
                      // Mede Frequencia da Intermitencia da Luz
                      //
                      
                      int anPin = (getValue(readString,'_',2)).toInt()+53;
                      int tempo_s = (getValue(readString,'_',3)).toInt();
                      double freq[2];

                      medeFreqIntermit(anPin, tempo_s, freq);

                      retornaHTTP(client, "OK," + String(freq[0])+"ms/"+String(freq[1])+"ms");
                    }
                    else if (cmd == "medeLuzTempoIntermit") {
                      ///////////////////////////////////////////
                      // Mede Tempo da Intermitencia da Luz
                      //
                      int anPin = (getValue(readString,'_',2)).toInt()+53;
                      int tempo_lim = (getValue(readString,'_',3)).toInt(); // tempo esperado para ficarno estado intermitente
                      int tempo_tol = (getValue(readString,'_',4)).toInt(); // tolerancia para cima e para baixo em relacao ao tempo
                      int timeout = tempo_lim+tempo_tol+5; // tempo máximo para realizar a medicao
                      double freq[2];

                      bool intermitOn=false;
                      bool intermitOff=false;
                      bool ledStatusAnt = false;
                      bool intermitOk=false;
                      double intermitMedida=0;

                      double medIni=millis();

                      delay(3);

                      medeFreqIntermit(anPin, 2, freq);
                      
                      if (freq[0] != -1 && freq[1] != -1) {
                        // no passo anterior foi verificado se a luz está intermitente de fato
                        long medUlt=millis();
  
                        while ((millis()-medIni)/1000 <= (timeout-1)){
                          analogValue = analogRead(anPin);
                          
                          if (analogValue >= thrLEDOff && ledStatusAnt == true){
                            if ((millis()-medUlt) > freq[0]*1.5) {
                              intermitOk=true;
                              break;
                            }
                          }
                          else if (analogValue < thrLEDOff && ledStatusAnt == true){
                            medUlt=millis();
                            ledStatusAnt=false;
                          }
                          else if (analogValue >= thrLEDOff && ledStatusAnt == false){
                            medUlt=millis();
                            ledStatusAnt=true;                            
                          }
                          //Serial.println("Tempo exec:" + String((millis()-medIni)/1000) + " timeout:" + String(timeout-1));
                        }
                        
                        if ( intermitOk == true ){
                          intermitMedida=(medUlt-medIni)/1000;
  
                          if (intermitMedida >= tempo_lim-tempo_tol && intermitMedida <= tempo_lim+tempo_tol) {
                            retornaHTTP(client, "OK,"+String(intermitMedida) + "s");
                          }
                          else {
                            retornaHTTP(client, "NOK,"+String(intermitMedida) + "s");
                          }
                        }
                        else {
                          retornaHTTP(client, String("NOK, aguardado tempo maximo."));
                        }
                      }
                      else {
                        retornaHTTP(client, String("NOK, intermitencia nao detectada (>2s)"));
                      }
                    }
                    
                    readString="";
                    client.stop(); // Para fins de debug
                }
            } 
        } 
    }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

double medeFreqIntermit(int anPin, int tempo_s, double *freq){
  bool ledStatusAnt = false;
  int thrLEDOff = 8;
  int iOn=0;
  int iOff=0;

  //double freq[2];
  long tempoOn=0;
  long tempoOff=0;
  long tempoOnMedia=0;
  long tempoOffMedia=0;
  
  analogValue = analogRead(anPin);
  if (analogValue < thrLEDOff)
    ledStatusAnt=false;
  else
    ledStatusAnt=true;
  
  long medIni=millis();
  long medUlt=medIni;
  
  //Serial.println(String(millis())+" medIni:"+String(medIni)+" tempo_s:" + String(tempo_s));
  
  while ((millis()-medIni)/1000 <= (tempo_s-1)){
    //Serial.println(String((millis()-medIni)/1000)+" "+String(tempo_s-1)+" "+String(ledStatusAnt)+" "+String(tempoOn)+" "+String(iOn)+" "+analogValue);
    analogValue = analogRead(anPin);
  
    if (analogValue < thrLEDOff){
      if (ledStatusAnt == true){
        ledStatusAnt=false;
        tempoOn=tempoOn+(millis()-medUlt);
        medUlt=millis();
        iOn++;
      }
    }
    else{
      if (ledStatusAnt == false){
        ledStatusAnt=true;
        tempoOff=tempoOff+(millis()-medUlt);
        medUlt=millis();
        iOff++;
      }
    }
  }
    
  if (iOn == 0 || iOff == 0){
    tempoOnMedia=-1;
    tempoOffMedia=-1;
  }
  else {
    tempoOnMedia=tempoOn/iOn;
    tempoOffMedia=tempoOff/iOff;
  }

  freq[0]=tempoOnMedia;
  freq[1]=tempoOffMedia;
  //Serial.println(String(freq[0]) + "ms " + String(freq[1]) + "ms");
}

void retornaHTTP(EthernetClient client, String texto){
  client.println("HTTP/1.1 200 OK"); //send new page 
  client.println("Content-Type: text/html"); 
  client.println(); // nao pode tirar essa linha
  client.println(texto);
}
