#/usr/bin/python3
# -*- coding: utf-8 -*-
# V1.2
# Thanks to Ocean, JS, Montaulab, Claudine, CQuest, Musée du minitel....
#*************************************************************
import csv, sqlite3, sys, pynitel, serial, mysql.connector, os

###
# Utility functions
####
#****** Write csv datafile to dataobject "data"
def create_data(csv_dateipfad):
    data = {}    
    # CSV-Datei öffnen und auslesen
    with open(csv_dateipfad, "r") as csv_datei:
        csv_reader = csv.reader(csv_datei, delimiter=";")
        spaltenueberschriften = next(csv_reader)
        for zeile in csv_reader:
            beschreibung = zeile[0]            
            spalten_werte = {}            
            for i in range(1, len(zeile)):
                spaltenueberschrift = spaltenueberschriften[i]                
                wert = zeile[i]
                spalten_werte[spaltenueberschrift] = wert            
            data[beschreibung] = spalten_werte    
    return data

#**************Read text from csv file "data" and use choosen language
def transl(beschreibung):
    global lang, data
    # Überprüfen, ob die Beschreibung im Datenobjekt vorhanden ist
    if beschreibung in data:
        # Überprüfen, ob die Spaltenüberschrift im Datenobjekt vorhanden ist
        if lang in data[beschreibung]:
            # Wert aus dem Datenobjekt abrufen und zurückgeben
            wert = data[beschreibung][lang]
            return wert
        else:
            print("Spaltenüberschrift nicht gefunden: ")
    else:
        print("Beschreibung nicht gefunden: ", beschreibung)



#******Screenprint centered
def strcenter(row = 0,pos=20, txt = ' ', width = 40, size = 0):
    out = pos - len(txt)//2
    if out < 1:
        out = 1
    m.pos(row,out)
    m.scale(size)
    m._print(txt)
    m.scale(1)
    return()

#****** Adultcheck with code
def adultcheck(time):
    global st
    st = time
    m.home()
    
    strcenter(row = 4,pos=20, txt=transl("p6t1"), width=40, size=1)
    m.pos(11,4)
    m.plot('*', 34)
    for x in range(12,19):
        m.pos(x,4)
        m.plot('*',2)
        m.pos(x,36)
        m.plot('*',2)
    m.pos(19,4)    
    m.plot('*', 34)
    m.pos(12,6)
    m._print("                              " )
    m.pos(13,6)
    m._print(transl("p6t2") )
    m.pos(14,6)
    m._print(transl("p6t3"))
    m.pos(15,6)
    m._print(transl("p6t4"))
    m.pos(16,6)
    m._print(transl("p6t5"))
    m.pos(17,6)
    m._print(transl("p6t6"))
    m.pos(23,1)
    m.backcolor(m.blanc)
    m.color(m.blanc)
    m._print(transl("p6t7"))
    (choix, touche) = m.input(23, 1, 5, sltime)   
    if touche == m.envoi and choix == "69696":
        return("A")
    else:
        m.home()
        return("")
    
#******Format to left and to right
def strformat(left='', right='', fill=' ', width=40):
    " formattage de texte "
    total = width-len(left+right)
    if total > 0:
        out = left + fill * total + right
    else:
        out = left+right
    print("'"+out+"'", width, total, len(out))
    return(out)
        
###
# State machine aka "The brain"
###
class StateMachine:
    def __init__( self ):
        self.stack = []
        self.push( self.stateInit )
        self.radarCount = 0
        self.time = 0
        self.time1 = 0
        self.halftime =0
        self.offStageLimit = 0
        self.offStageMessage = 0
        

    def push( self, state ):
        self.stack.append( state )
        self.changing = True
        
    def pop( self ):
        self.stack.pop()
        
    def changeState( self, state ):
        self.pop()
        self.push( state )

    def update( self ):
        if( len( self.stack ) <= 0 ):
            return
        
        entering = self.changing
        self.changing = False;
        self.stack[-1]( entering  )
#*****************************************************
    #****** Initialisation with setting of variables      
    def stateInit( self, entering  ):
        print("~~~ Initialisation ~~~")        
        print("Minitel init")
        global m, lang, th1,data,sltime
        lang = "DE"
        sltime = 120
        
        m = pynitel.Pynitel(serial.Serial('/dev/ttyUSB0', 1200, parity=serial.PARITY_EVEN, bytesize=7, timeout=2))
        self.changeState( self.stateLanguage )
       
    def stateWishPic( self, entering  ):
        global lang, sltime, ver
        
        print("Wish wizard picture")
        m.home()
        m.load(1,'./WM/WishWizard.vdt')
        m.draw(1)
        
        while True:
            # ligne finale
            m.pos(24, 1)            
            m.color(m.vert)
            m._print('To continue press ')
            m.pos(24, 19)
            m.inverse()
            m.color(m.cyan)
            m._print('  ENVOI ')
            
         # attente saisie
            m.cursor(False)
            (choix1, touche) = m.input(23, 1, 0, sltime)
    
            if touche != "": 
                break
            elif choix1 != "" :
                break
            
        if touche != "" or choix1 != "" :
            self.changeState( self.stateWelcome )
            
    def statePrefs(self, entering): # Prefs: timer screensave, perhaps 
        print("State Preferences")
        global m,wish1, wish2, lang,sltime, db_cursor     
        m.resetzones()
        m.clear        
        db_conn.commit()
        db_cursor.close()
        db_cursor = db_conn.cursor()             
        db_cursor.execute("SELECT * FROM pref")        
        res = db_cursor.fetchall()
        r = res[0]        
        m.zone(7, 15, 23, r[1], m.blanc)        
        m.zone(9, 15, 23, str(r[2]), m.blanc)
        m.zone(11, 15, 23, "NO", m.blanc)
        m.zone(13, 15, 23, "NO", m.blanc)
        r = res[0]        
        touche = m.repetition
        zone = 1
        m.home()
        
        while True:
            m.home()
            m.pos(0,1)
            m._print("Version " + ver)
            m.pos(2,1)
            m.scale(3)
            m._print(transl("p3t1"))
            m.pos(4,1)
            m.scale(3)
            m._print(transl("p3t2"))
            m.scale(0)
            strcenter(row = 1,pos=28, txt = transl("p3t3"), width = 40, size = 0)
            strcenter(row = 3,pos=28, txt = transl("p3t4"), width = 40, size = 0)
            strcenter(row = 4,pos=28, txt = transl("p3t5"), width = 40, size = 0)
            m.pos(5)
            m.color(m.bleu)
            m.plot('̶', 40)
            m.pos(7)
            m._print(''+ strformat(left="Local / IP"[:11],right="*........................" , width=39))
            m.pos(9)
            m._print(''+ strformat(left="Time sleep"[:11],right="*........................" , width=39))            
            m.pos(11)
            m._print(''+ strformat(left="Reboot"[:11],right="*........................" , width=39))            
            m.pos(13)
            m._print(''+ strformat(left="Shutdown"[:11],right="*........................" , width=39))            

# ligne finale
            m.pos(21)
            m.color(m.bleu)
            m.plot('̶', 40)
            m.pos(22, 1)
            m._print(transl("p3t11"))             
            m.pos(23, 1)

            m.color(m.vert)
            m._print(transl("p3t12"))
            m.pos(23, 12) 
            m.inverse()
            m.color(m.cyan)
            m.underline()
            m._print("_SUITE ")
            
            m.pos(24, 1)
            m.color(m.vert)
            m._print(transl("p3t13"))
            m.pos(24, 12)
            m.inverse()
            m.color(m.cyan)
            m._print(" RETOUR")
            m.pos(24, 25)
            m._print(transl("p3t15"))
            m.pos(24, 33)
            m.inverse()
            m.color(m.cyan)
            m._print("SOMMAIRE")
            m.pos(22, 21)
            m._print(transl("p3t14"))
            m.pos(22, 33)
            m.inverse()
            m.color(m.cyan)
            m._print('  ENVOI ')
            m.pos(24, 28)            
            
            # gestion de la zone de saisie courante
            (zone, touche) = m.waitzones(zone, sltime)
            print(touche)
            
            if touche == 1:
                print("Touche ENVOI: " + str(touche))
                choice = ""
                if m.zones[0] =="":
                    m.zones[0] = "localhost"
                prefs = (m.zones[0]['texte'], m.zones[1]['texte'])
                #print(prefs)
                sql = "UPDATE pref SET id = 1, IP_adr = %s, timer = %s WHERE id = 1"                      
                # Execute SQL statement with provided values
                db_cursor.execute(sql, prefs)
                db_conn.commit()
                break
            if touche == 3:
                break            
            if touche == 5:
                break
            if touche == 6:
                break
        if touche == 1:
            print("check & prepare data ")            
            self.changeState( self.stateWelcome )
        elif touche == 3 and str(m.zones[2]['texte']) == "YES":
            m.home()
            m.message(15, 7, 3,"Go to reboot ", bip=True)
            m.home()
            os.system('reboot')
            
        elif touche == 3 and m.zones[3]['texte'] == "YES":
            m.home()
            m.message(15, 7, 3,"Go to shutdown", bip=True)
            m.home()
            os.system('shutdown now')
        elif touche == 6:
            self.changeState( self.stateWelcome )
        else:
            print(m.zones[2], " ", m.zones[3])
            print("stay in stream")        
        
    def stateLanguage(self, entering): #p0t1
        print("State Welcome")
        global lang, th1, sltime, ver
        m._del(0,0)        
        while True:# t2 > time.time():#True:
            if True == True:  # affichage
            # entête sur 2 lignes + séparation
                m.home()
                m.pos(0)
                m.pos(0,0)
                m._print("V" + ver + " / " + lang)
                m.pos(2)
                m.pos(2,1)
                m.scale(3)
                m._print(transl("p1t1"))
                m.pos(4,1)
                m.scale(3)
                m._print(transl("p1t2"))
                m.scale(0)
                strcenter(row = 4,pos=27, txt = transl("p1t3"), width = 40, size = 0)
                m.pos(5)
                m.color(m.bleu)
                m.plot('̶', 40)
                strcenter(row = 8,pos=20, txt = transl("p1t4"), width = 40, size = 0)
                #strcenter(row = 9,pos=20, txt = 'choice', width = 40, size = 0)
                strcenter(row = 11,pos=10, txt = transl("p1t5"), width = 40, size = 0)
                strcenter(row = 11,pos=30, txt = transl("p1t6"), width = 40, size = 0)
                strcenter(row = 13,pos=10, txt = transl("p1t7"), width = 40, size = 0)
                strcenter(row = 13,pos=30, txt = transl("p1t8"), width = 40, size = 0)
        # ligne finale
                m.pos(21)
                m.color(m.bleu)
                m.plot('̶', 40)
                m.pos(22, 1)
                
                m.pos(24, 1)
                m.color(m.vert)                
                m._print(transl("p1t9"))
                m.pos(24, 8)
                m.inverse()
                m.color(m.cyan)
                m._print("GUIDE")
                
                m.pos(24, 22)
                m.color(m.vert)
                m._print(transl("p1t10"))
                m.pos(24, 36)
                m.inverse()
                m.color(m.cyan)
                m._print("ENVOI")
            else:
                page = abs(page)            
            
            (choix1, touche) = m.input(24, 33, 2,sltime)                 
            m.cursor(False)
            
            if touche == m.suite:
                return(touche)
                    
            elif touche == m.chariot:
                break
            
            elif touche == m.retour or touche== m.annulation:
                break
            elif touche == m.envoi:                
                break
            elif touche == m.sommaire:
                print("touche sommaire")
                break
                           
            elif touche == m.guide:
                break
            elif touche == m.correction:  # retour saisie pour correction
                return(touche)
            #elif touche != m.repetition:
                #print("Beep")#m.bip()         

        print("Bin hier")               
        #if t2 < time.time():
            #m.message(15, 7, 5,"timer passed", bip=True)
        if choix1 == "":
            choix1 = lang
        if touche == m.sommaire and choix1 == "sleep":
            #choix1 = ""
            print("Go to sleeper")
            self.changeState( self.stateWelcome )
        if touche == m.envoi and choix1 == "FR" :
            lang = "FR"
            m.message(16, 7, 2,transl("p1t11"), bip=False)            
            self.changeState( self.stateWelcome )
        elif touche == m.envoi and choix1 == "EN" :
            lang = "EN"
            m.message(16, 7, 2,transl("p1t11"), bip=False)            
            self.changeState( self.stateWelcome )
        elif touche == m.envoi and choix1 == "DE" :
            lang = "DE"
            m.message(16, 7, 2,transl("p1t11"), bip=False)            
            self.changeState( self.stateWelcome )
        elif touche == m.envoi and choix1 == "ES" :
            lang = "ES"
            m.message(16, 7, 2,transl("p1t11"), bip=False)            
            self.changeState( self.stateWelcome )
            
        elif touche == m.envoi:
            if choix1 != "FR" or choix1 != "EN" or choix1 != "DE" or choix1 != "ES":
                m.clear
                m.home()
                m.message(15, 7, 3,"Wrong CODE, try again ", bip=True)
        elif touche == m.guide:
            self.changeState( self.stateInfo1 ) 
        
    def stateWelcome(self, entering):
        print("State Welcome")
        global lang, sltime
        m.clear
        m.home()        
        while True:
            if True == True:  # affichage
            # entête sur 2 lignes + séparation
                m.home()
                m.pos(2)
                m.pos(2,1)
                m.scale(3)
                m._print(transl("p2t1"))
                m.pos(4,1)
                m.scale(3)
                m._print(transl("p2t2"))
                m.scale(0)
                strcenter(row = 4,pos=28, txt = transl("p2t3"), width = 40, size = 0)
                m.pos(5)
                m.color(m.bleu)
                m.plot('̶', 40)
                strcenter(row = 8,pos=10, txt = transl("p2t4"), width = 40, size = 0)
                strcenter(row = 9,pos=10, txt = transl("p2t5"), width = 40, size = 0)
                strcenter(row = 10,pos=10, txt = transl("p2t6"), width = 40, size = 0)
                strcenter(row = 13,pos=10, txt = transl("p2t7"), width = 40, size = 3)
                #strcenter(row = 13,pos=20, txt = transl("p2t8"), width = 40, size = 3)
                strcenter(row = 8,pos=30, txt = transl("p2t9"), width = 40, size = 0)
                strcenter(row = 9,pos=30, txt = transl("p2t10"), width = 40, size = 0)
                strcenter(row = 10,pos=30, txt = transl("p2t11"), width = 40, size = 0)
                strcenter(row = 13,pos=30, txt = transl("p2t12"), width = 40, size = 3)
                strcenter(row = 16,pos=20, txt = transl("p2t13"), width = 40, size = 3)
                strcenter(row = 18,pos=20, txt = transl("p2t14"), width = 40, size = 0)
            
            # ligne finale
                m.pos(21)
                m.color(m.bleu)
                m.plot('̶', 40)
                m.pos(22, 1)
                
                m.color(m.vert)
                m.pos(24, 1)
                m._print(transl("p2t15"))
                m.pos(24, 10)
                m.inverse()
                m.color(m.cyan)
                m._print("SOMMAIRE")
                m.pos(23, 1)
                m._print(transl("p2t16"))
                m.pos(23, 10)
                m.inverse()
                m.color(m.cyan)
                m._print("GUIDE")
                m.pos(24, 24)
                m.color(m.vert)
                m._print(transl("p2t17"))
                m.pos(24, 36)
                m.inverse()
                m.color(m.cyan)
                m._print("ENVOI")
            else:
                page = abs(page)
                        
            (choix1, touche) = m.input(24, 33, 2, sltime)
            #****** check for integer
            if choix1 != "sleep":
                if not isinstance(choix1,int):
                    if not choix1.isdigit():
                        choix1 = 0
                    choix1 = int(choix1)
            
            m.cursor(False)                       
            if touche == m.suite:
                return(touche)
            elif touche == m.chariot:
                break            
            elif touche == m.retour or touche== m.annulation:
                break
            elif touche == m.envoi:                
                break
            elif touche == m.sommaire:
                break                           
            elif touche == m.guide:
                break
            elif touche == m.correction:  # retour saisie pour correction
                return(touche)
            elif touche != m.repetition:
                m.bip()  
        print("Bin hier")          
        if touche == m.envoi and choix1 == 1 :          
            self.changeState( self.stateEnterwish )
        #elif  touche == m.chariot:
            #print("!!!Last key: " + str(m.key()))                
        elif touche == m.envoi and choix1 == 2 :
            self.changeState( self.stateWishread1 )
        elif touche == m.envoi and choix1 == 99 :
            self.changeState( self.stateWishdelete )
        elif touche == m.envoi and choix1 == 98 :
            self.changeState( self.statePrefs )
        elif touche == m.envoi:
            if choix1 < 1 or choix1 > 2 or choix1 == 99:                
                m.home()
                m.message(15, 7, 3,"Wrong Number, try again ", bip=True)             
        elif touche == m.sommaire and choix1 == "sleep":
            print("sommaire to sleep")
            self.changeState( self.stateWishPic ) #***new ?????
            #return
        elif touche == m.sommaire and choix1 == 0:
            print("sommaire to Language")
            self.changeState( self.stateLanguage )
        if touche == m.guide:
            self.changeState( self.stateInfo1 ) 
       
    def stateInfo1( self, entering  ):        
        print("State INFO 1")        
        global choix1, lang, sltime
        m.home()
        while True:
            if True == True:  # affichage
            # entête sur 2 lignes + séparation
                m.home()
                m.pos(2)
                m.pos(2,1)
                m.scale(3)
                m._print(transl("p8t1"))
                m.pos(4,1)
                m.scale(3)
                m._print(transl("p8t2"))
                m.scale(0)
                strcenter(row = 2,pos=30, txt = transl("p8t3"), width = 40, size = 1)
                strcenter(row = 4,pos=30, txt = transl("p8t4"), width = 40, size = 0)
                m.pos(5)
                m.color(m.bleu)
                m.plot('̶', 40)
                #####14 Zeilen max
                strcenter(row = 7,pos=20, txt = transl("p8t5"), width = 40, size = 0)
                strcenter(row = 8,pos=20, txt = transl("p8t6"), width = 40, size = 0)
                strcenter(row = 9,pos=20, txt = transl("p8t7"), width = 40, size = 0)
                strcenter(row = 10,pos=20, txt = transl("p8t8"), width = 40, size = 0)
                strcenter(row = 11,pos=20, txt = transl("p8t9"), width = 40, size = 0)
                strcenter(row = 12,pos=20, txt = transl("p8t10"), width = 40, size = 0)
                strcenter(row = 13,pos=20, txt = transl("p8t11"), width = 40, size = 0)
                strcenter(row = 14,pos=20, txt = transl("p8t12"), width = 40, size = 0)
                strcenter(row = 15,pos=20, txt = transl("p8t13"), width = 40, size = 0)
                strcenter(row = 16,pos=20, txt = transl("p8t14"), width = 40, size = 0)
                strcenter(row = 17,pos=20, txt = transl("p8t15"), width = 40, size = 0)
                strcenter(row = 18,pos=20, txt = transl("p8t16"), width = 40, size = 0)
                strcenter(row = 19,pos=20, txt = transl("p8t17"), width = 40, size = 0)
                strcenter(row = 20,pos=20, txt = transl("p8t18"), width = 40, size = 0)
            
            # ligne finale
                m.pos(21)
                m.color(m.bleu)
                m.plot('̶', 40)
                m.pos(22, 1)
                
                m.color(m.vert)
                m.pos(23, 29)
                
                m.pos(24, 26)
                m.color(m.vert)
                m._print("Back → ")
                m.inverse()
                m.color(m.cyan)
                m._print(" ENVOI ")
            else:
                page = abs(page)
        # attente saisie             
            (choix1, touche) = m.input(24, 31, 0,sltime)
            #if choix1 == "":
            #    choix1 = ""
            #else:
                #choix1 = choix1
            m.cursor(False)
            if touche == m.suite:
                return(touche)
                    #page = -page  # pas de ré-affichage
            
            elif touche == m.retour or touche== m.annulation:
                break
            elif touche == m.envoi:
                break
            elif touche == m.sommaire:
                break
                           
            elif touche == m.guide:
                break
            elif touche == m.correction:  # retour saisie pour correction
                return(touche)
            elif touche != m.repetition:
                m.bip()
        if touche == m.envoi:
            self.changeState( self.stateWelcome)
        elif touche == m.sommaire and choix1 == "sleep":
            print("Go to sleeper")
            self.changeState( self.stateWelcome )
            
    def stateEnterwish( self, entering  ):
        
        global m,wish1, wish2, lang,sltime
        print("State Enterwish")
        m.resetzones()
        m.clear
        t = ["'Title'", "'Description'","","", "'Your name'", "'Adult wish y/n'", "'How to find you'"]        
        m.zone(7, 15, 23, '', m.blanc)        
        m.zone(9, 15, 23, '', m.blanc)
        m.zone(11, 15, 23, '', m.blanc)
        m.zone(13, 15, 23, '', m.blanc)        
        m.zone(15, 15, 1, '', m.blanc)        
        m.zone(17, 15, 23, '', m.blanc)
        m.zone(19, 15, 23, '', m.blanc)        
        touche = m.repetition
        zone = 1
        m.home()
        #m.draw(2)
        while True:
            m.home()
            m.pos(2)
            m.pos(2,1)
            m.scale(3)
            m._print(transl("p3t1"))
            m.pos(4,1)
            m.scale(3)
            m._print(transl("p3t2"))
            m.scale(0)
            strcenter(row = 1,pos=28, txt = transl("p3t3"), width = 40, size = 0)
            strcenter(row = 3,pos=28, txt = transl("p3t4"), width = 40, size = 0)
            strcenter(row = 4,pos=28, txt = transl("p3t5"), width = 40, size = 0)
            m.pos(5)
            m.color(m.bleu)
            m.plot('̶', 40)
            m.pos(7)
            m._print(''+ strformat(left=transl("p3t6")[:11],right="*........................" , width=39))
            m.pos(9)
            m._print(''+ strformat(left=transl("p3t7")[:11],right="*........................" , width=39))
            m.pos(11)
            m._print(''+ strformat(left=""[:6],right="........................." , width=39))
            m.pos(13)
            m._print(''+ strformat(left=""[:6],right="........................." , width=39))
            m.pos(15)
            m._print(''+ strformat(left=transl("p3t8")[:9],right="*                        " , width=39))
            m.pos(17)
            m._print(''+ strformat(left=transl("p3t9")[:10],right="*........................" , width=39))
            m.pos(19)
            m._print(''+ strformat(left=transl("p3t10")[:12],right="*........................" , width=39))

# ligne finale
            m.pos(21)
            m.color(m.bleu)
            m.plot('̶', 40)
            m.pos(22, 1)
            m._print(transl("p3t11"))             
            m.pos(23, 1)

            m.color(m.vert)
            m._print(transl("p3t12"))
            m.pos(23, 12) 
            m.inverse()
            m.color(m.cyan)
            m.underline()
            m._print("_SUITE ")
            
            m.pos(24, 1)
            m.color(m.vert)
            m._print(transl("p3t13"))
            m.pos(24, 12)
            m.inverse()
            m.color(m.cyan)
            m._print(" RETOUR")
            m.pos(24, 25)
            m._print(transl("p3t15"))
            m.pos(24, 33)
            m.inverse()
            m.color(m.cyan)
            m._print("SOMMAIRE")
            m.pos(22, 21)
            m._print(transl("p3t14"))
            m.pos(22, 33)
            m.inverse()
            m.color(m.cyan)
            m._print('  ENVOI ')
            m.pos(24, 28)
            
            
            # gestion de la zone de saisie courante
            (zone, touche) = m.waitzones(zone, sltime)
            print(touche)
            
            if touche == 1:
                print("Touche ENVOI: " + str(touche))
                choice = ""
                annu_save ="n"
                for i in range(0 , 6):
                    if i <= 1 or i >= 4:
                        if str(m.zones[i]['texte']) == "":
                            m.message(21, 5, 4,"Field " + t[i] + " required!", bip=False)
                            annu_save = "y"
                            touche = 0
                            break
                if annu_save != "y":
                    break
            if touche == 6:
                break
            if touche == 5:
                break
        if touche == 1:
            print("check & prepare data ")
            #*** prepare Adultcheck
            if m.zones[4]['texte'] == "y":
                m.zones[4]['texte'] = "Y"             
            if m.zones[4]['texte'] != "Y" :
                m.zones[4]['texte'] = "N"
            
            wish1 = (m.zones[0]['texte'], m.zones[1]['texte'],m.zones[2]['texte'], m.zones[3]['texte'], m.zones[5]['texte'], m.zones[4]['texte'], m.zones[6]['texte'])#.strip()
            self.changeState( self.stateWishsaved )
        elif touche == 6:
            self.changeState( self.stateWelcome )
        else:
            print("stay in stream")
            
    def stateWishsaved( self, entering ):
                
        #if( entering ):
        print("State Wishsave")
        
        global wish1, wish2, db_cursor, db_conn, lang
        db_cursor.close() #Close DB
        db_cursor = db_conn.cursor() #Open db
        db_cursor.execute("SELECT COUNT(*) FROM wishes")
        db_result = db_cursor.fetchone()
        db_num = int(db_result[0])+1
        sql = "INSERT INTO wishes (lfd,titel,descr1,descr2,descr3,name,rated,find,fullfilled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"        
        # Provide values for placeholders
        data = (db_result[0]+1,wish1[0], wish1[1], wish1[2], wish1[3], wish1[4], wish1[5], wish1[6], "")        
        # Execute SQL statement with provided values
        db_cursor.execute(sql, data)
        db_conn.commit()
        db_cursor.execute("SELECT * FROM wishes")
        inhalt = db_cursor.fetchall()
        
        m.clear
        m.home()
        #m.message(10, 10, 5,transl("p4t1")+ str(db_num) +transl("p4t2"), bip=False)
        m.message(10, 10, 5,transl("p4t1") + transl("p4t2"), bip=False)
        self.changeState( self.stateWelcome )


    def stateWishread1( self, entering  ):
        
        print("State read wish titel")
        global  m, choix, choix_lfd, lang, sltime, db_conn ,db_cursor
        choix = 0
        touche = 0
        db_conn.commit()
        db_cursor.close()
        db_cursor = db_conn.cursor()
        query = "SELECT COUNT(*) FROM wishes"
        db_cursor.execute(query)        
        db_result = db_cursor.fetchone()            
        db_num = int(db_result[0])
        print(db_num)            
        db_cursor.execute("SELECT * FROM wishes ORDER BY lfd DESC")        
        res = db_cursor.fetchall()
        #"Affiche les résultats de la recherche"
        m.home()
        m.clear
        m.resetzones()
        m.zone(22, 28, 30, '', m.blanc)
        m.pos(2)
        page = 1
        while True:                      
            if db_num > 0:  # affichage
            # entête sur 2 lignes + séparation
                m.home()
                m.pos(0)
                m._print(transl("p5t1"))
                if db_num != '':
                    m.pos(0, 39)
                    m.color(m.bleu)
                    m._print(str(db_num))
                m.pos(2)
                m.color(m.bleu)
                m.plot('̶', 40)
                
            # plusieurs pages ?
                if len(res) > 9:
                    m.pos(1, 37)
                    m._print(" "+str(int(abs(page)))+'/'+str(int((len(res)+8)/9)))
                    m.pos(3)

            # première ligne de résultat
                m.pos(3)
                for a in range((page-1)*9, page*9, ):
                #for a in range( page*9,(page-1)*9, -1): # neu rückwärts
                    print("Anzeige page:",(page-1)*9, "  ",page*9)
                    if a < len(res):
                        r = res[a]                        
                        m.color(m.blanc)
                        m._print(strformat(right=str(int(a+1)), width=3))
                        print("Datensatz: " + str(a) + " Inhalt Adulte: " + str(r[6]))
                        if str(r[6]) == "Y":
                            z= "18+"
                        else:
                            z ="   "
                        if str(r[8]) == "Y":
                            zz= " in prepa."
                        else:
                            zz ="  ---     "
                        m._print(' '+ strformat(left=z + zz, right=r[1][:24], width=36))
                        m.color(m.vert)
                        m.color(m.bleu)
                        if a < page*9:
                            m.plot(' ', 4)
                            m.plot('̶', 36)

            # ligne finale
                m.pos(21)
                m.color(m.bleu)
                m.plot('̶', 40)

                if page > 1:
                    if len(res) > page*9:  # place pour le SUITE
                        m.pos(22, 20)
                    else:
                        m.pos(22, 20)
                    m.color(m.vert)
                    m._print(transl("p5t7"))
                    m.pos(22, 33)
                    m.underline()
                    m._print(' ')
                    m.inverse()
                    m.color(m.cyan)
                    m._print('_RETOUR ' )
                    
                if len(res) > page*9:
                    m.pos(23, 21)
                    m.color(m.vert)
                    m._print(transl("p5t6"))
                    m.pos(23, 34)
                    m.underline()
                    m._print(' ')
                    m.inverse()
                    m.color(m.cyan)
                    m._print('_SUITE')

                m.pos(22, 1)
                m._print(transl("p5t2"))
                m.pos(23, 5)
                m._print(transl("p5t3"))

                m.underline()
                m._print(' ')
                m.inverse()
                m.color(m.cyan)
                m._print('_ENVOI ')
                m.pos(24, 1)
                m.color(m.vert)
                m._print(transl("p5t4"))
                m.pos(24, 11)
                m.inverse()
                m.color(m.cyan)
                m._print(' GUIDE')
                m.underline()
                m._print(' ')
                m.inverse()
                m.color(m.cyan)
                m.pos(24, 26)
                m.color(m.vert)
                m._print(transl("p5t5"))
                m.pos(24, 33)
                m.inverse()
                m.color(m.cyan)
                m._print("SOMMAIRE")
            
            elif db_num == 0:
                
                print("0 Data... und raus")
                m.message(15, 7, 5,transl("p5t8"), bip=True)
                break
            else:
                page = abs(page)

        # attente saisie            
            (choix, touche) = m.input(23, 1, 3, sltime)
            #****** check for integer
            if not isinstance(choix,int):
                if not choix.isdigit():
                    choix = 0
                choix = int(choix)
                m.clear
            
            if choix == "":
                choix = int(0)
            
            elif choix > db_num:
                return
            else:
                choix = int(choix)
            m.cursor(False)
            if touche == m.suite:
                if page*9 < len(res):
                    page = page + 1
                else:
                    m.bip()
            elif touche == m.retour:
                if page > 1:
                    page = page - 1
                else:
                    m.bip()
            elif touche == m.envoi:
                r = res[choix-1]                
                choix_lfd = r[0]
                break
                
            elif touche == m.guide:
                break
            elif touche == m.sommaire: 
                break
            elif touche == m.correction:  # retour saisie pour correction
                return(touche)
            elif touche != m.repetition:
                m.bip()
                page = -page  # pas de ré-affichage        
        print("auswahl Wish choix: " + str(choix) + " & Touche " + str(touche))
        if touche == m.guide:
            self.changeState( self.stateInfo1 )
        if touche == m.sommaire:
            self.changeState( self.stateWelcome )
            
        if touche == m.envoi and choix > 0:
            if choix > db_num:
                m.home()
                m.message(10, 7, 3," This wish doesn't exist "+ str(db_num), bip=True)
                return()
            print("CHoix > 0")
            # adult check
            r = res[choix-1]
            print(r)
            if r[6] == "Y" or r[6] == "y":
                print("Adult content" , sltime)
                a = adultcheck(sltime)
                if a =="A":
                    self.changeState( self.stateWishread2 )
                else:
                    
                    m.message(10, 7, 3,transl("p5t9"), bip=True)
                    return()
                
            else:
                print("Kids content")
            self.changeState( self.stateWishread2 )
        elif touche == m.envoi and choix < 0:
            print("CHoix <= 0")
            self.changeState( self.stateWelcome )
        if db_num == 0:
            self.changeState( self.stateWelcome )
         
            
    def stateWishread2( self, entering  ):
        
        print("State read wish details")
        global db_cursor, choix,  choix_lfd, lang, sltime        
        db_conn.commit()
        db_cursor.close() #Close DB
        db_cursor = db_conn.cursor() #Open db
          
        db_cursor.execute("SELECT * FROM wishes WHERE lfd="+str(choix_lfd))
        res1 = db_cursor.fetchall()
        m.home()
        while True:
            if True == True:  # affichage
            # entête sur 2 lignes + séparation
                m.home()
                m.pos(0,0)
                m._print(transl("p7t1"))
                m._print(str(choix))
                m.pos(2)
                m.color(m.bleu)
                m.plot('̶', 40)
            
            # première ligne de résultat
                m.pos(4)
                r = res1[0]
                m.color(m.blanc)
                m._print(' '+ strformat(left=transl("p7t2")[:8],right="" , width=37))
                strcenter(row = 4,pos=20, txt=r[1], width=40, size=1)
                m.pos(6)                
                m._print(' '+ strformat(left=transl("p7t3")[:8], right="", width=37))
                strcenter(row = 6,pos=20, txt=r[2], width=40, size=0)
                strcenter(row = 7,pos=20, txt=r[3], width=40, size=0)
                strcenter(row = 8,pos=20, txt=r[4], width=40, size=0)
                m.color(m.bleu)
                m.pos(9,4)    
                m.plot('*', 34)
                for x in range(9,20):
                    m.pos(x,4)
                    m.plot('*',2)
                    m.pos(x,36)
                    m.plot('*',2)
                m.pos(20,4)    
                m.plot('*', 34)                
                m.pos(11,6)
                m._print(transl("p7t4"))
                m.pos(12,6)                
                m._print(transl("p7t5"))
                m.pos(15,6)
                m.scale(1)
                m._print(transl("p7t6"))
                m.pos(17,6)
                m._print(transl("p7t7"))
                m.pos(18,6)
                m._print(transl("p7t8"))
            # ligne finale
                m.pos(21)
                m.color(m.bleu)
                m.plot('̶', 40)                
                m.pos(23, 26)
                m._print(transl("p7t9"))
                m.inverse()
                m.color(m.cyan)
                m._print("SOMMAIRE")
                m.pos(24, 1)
                m._print(transl("p7t10"))
                m.inverse()
                m.color(m.cyan)
                m._print(' ENVOI ')
                m.pos(24, 28)
                m.color(m.vert)
                m._print(transl("p7t11"))
                m.inverse()
                m.color(m.cyan)
                m._print("RETOUR")
            else:
                page = abs(page)
        # attente saisie
            (choix1, touche) = m.input(23, 1, 11, sltime)
            #****** check for integer NO NEED HERE
            #if not isinstance(choix1,int):
                #if not choix1.isdigit():
                    #choix1 = 0
                #choix1 = int(choix1)
                #m.clear            
            m.cursor(False)
            if touche == m.suite:
                m.bip()
            elif touche == m.retour:
                break
            elif touche == m.envoi:
                break    
            elif touche == m.sommaire:
                self.changeState( self.stateWelcome )
                break
            elif touche == m.correction:  
                return(touche)
            elif touche != m.repetition:
                m.bip()
        print("auswahl Wish: " + str(choix1))
        if touche == m.envoi:
            if choix1 == "OUI JE VEUX"  or choix1 == "YES I WILL"  or choix1 == "JA ICH WILL"  or choix1 == "YO LES":
####
                #**** write decision in fullfilled = Y update
                #sql = "INSERT INTO wishes (lfd,titel,descr1,descr2,descr3,name,rated,find,fullfilled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"        

                sql = "UPDATE wishes SET fullfilled = %s WHERE lfd= %s "
                new_value = "Y"
                record_id = str(choix_lfd)
                # Provide values for placeholders
                # Execute SQL statement with provided values
                db_cursor.execute(sql, (new_value, record_id))
                db_conn.commit()

#####

                
                print("Ok and go on")                
                
                m.canblock(11,24,1,True)
                self.changeState( self.stateWishtake )
            elif choix1 != "OUI JE VEUX"  or choix1 == "YES I WILL"  or choix1 == "JA ICH WILL"  or choix1 == "YO LES":
                print("Bad choice so, back")
                m.canblock(11,19,1,False)
                
                m.message(15, 7, 5,transl("p7t12"), bip=True)
                self.changeState( self.stateWishread1 )
        if touche == m.retour:
            
            self.changeState( self.stateWishread1 ) 
        
            
    def stateWishtake( self, entering  ):
        global choix, db_cursor,choix_lfd, lang, sltime
        db_conn.commit()
        db_cursor.close() #Close DB
        db_cursor = db_conn.cursor() #Open db 
        
        db_cursor.execute("SELECT * FROM wishes WHERE lfd="+str(choix_lfd))
        res1 = db_cursor.fetchall()
        print("State Take wish details")
        r = res1[0]
        while True:
            m.pos(10,4)    
            m.plot('*', 34)
            for x in range(11,19):
                m.pos(x,4)
                m.plot('*',2)
                m.pos(x,36)
                m.plot('*',2)
            m.pos(19,4)    
            m.plot('*', 34)
            m.pos(11,6)
            m._print("                              " )
            strcenter(row = 12,pos=20, txt='Person to surprise:', width=40, size=0)
            strcenter(row = 14,pos=20, txt=r[5], width=40, size=1)
            strcenter(row = 15,pos=20, txt="Where to find ?", width=40, size=0)
            strcenter(row = 17,pos=20, txt=r[7], width=40, size=1)
            # ligne finale
            m.pos(21)
            m.color(m.bleu)
            m.plot('̶', 40)
            
            m.pos(23, 26)
            m._print("Home → ")
            m.inverse()
            m.color(m.cyan)
            m._print("SOMMAIRE")
            m.pos(24, 1)
            m._print('      ')
            m.color(m.cyan)
            m._print('         ')
            m.pos(24, 28)
            m.color(m.vert)
            m._print("Back to Wishlist → ")
            m.inverse()
            m.color(m.cyan)
            m._print("RETOUR")
            
         # attente saisie
            m.cursor(False)
            (choix1, touche) = m.input(23, 1, 0, sltime)
            
            if touche == m.suite:
                m.bip()
            elif touche == m.retour:
                break 
            elif touche == m.envoi:
                break       
            elif touche == m.sommaire or touche == m.envoi:
                self.changeState( self.stateWelcome )
                break
            elif touche == m.correction:  # retour saisie pour correction
                return(touche)
            elif touche != m.repetition:
                m.bip()
        if touche == m.retour :
            self.changeState( self.stateWishread1 ) 

    def stateWishdelete( self, entering  ):
        
        print("State Delete datas ")
        global db_cursor, m, choix, choix_lfd, sltime, db_conn
        choix = 0
        touche = 0
        db_conn.commit()
        db_cursor.close() #Close DB
        db_cursor = db_conn.cursor() #Open db
        db_cursor.execute("SELECT COUNT(*) FROM wishes")
        db_num = db_cursor.fetchone()
        db_num = int(db_num[0])
        print(db_num)
        db_cursor.execute("SELECT * FROM wishes")
        res = db_cursor.fetchall()
        #"Affiche les résultats de la recherche"
        m.home()
        m.resetzones()
        m.zone(22, 28, 30, '', m.blanc)
        m.pos(2)
        page = 1
        while True:                      
            if db_num >= 1:  # affichage
            # entête sur 2 lignes + séparation
                m.home()
                m.pos(0)
                strcenter(row = 2,pos=20, txt="DELETE WISHES", width=40, size=1)
                #m._print("Actual Wishes")
                if db_num != '':
                    m.pos(0, 16)
                    m.color(m.bleu)
                    m._print(str(db_num))
                m.pos(3)
                m.color(m.bleu)
                m.plot('̶', 40)
            # plusieurs pages ?
                if len(res) > 5:
                    m.pos(1, 37)
                    print("Länge db: "+ str(len(res)))
                    m._print(" "+str(int(abs(page)))+'/'+str(int((len(res)+4)/5)))
                    m.pos(3)

            # première ligne de résultat
                m.pos(4)
                for a in range((page-1)*5, page*5):
                    if a < len(res):
                        r = res[a]                        
                        m.color(m.blanc)
                        m._print(strformat(right=str(int(a+1)), width=3))
                         
                        print("Datensatz: " + str(r[1]) + "-" +str(a) + " Inhalt Adulte: " + str(r[6]))
                        if str(r[6]) == "Y":
                            z= "Adulte"
                        else:
                            z ="All"                           
                        m._print(' '+ strformat(left=r[1][:17] + " " + r[6][:1], right=" "+r[2][:16], width=36))
                        m._print('    '+ strformat(left=r[3][:18], right=r[5][:18], width=36))                        
                        m.color(m.bleu)
                        if a < page*5:
                            m.plot(' ', 4)
                            m.plot('̶', 36)

            # ligne finale
                m.pos(21)
                m.color(m.bleu)
                m.plot('̶', 40)
                if page > 1:
                    if len(res) > page*5:  # place pour le SUITE
                        m.pos(22, 20)
                    else:
                        m.pos(22, 20)
                    m.color(m.vert)
                    m._print('Prev. page →')
                    m.underline()
                    m._print(' ')
                    m.inverse()
                    m.color(m.cyan)
                    m._print('_RETOUR ' )                    
                if len(res) > page*5:
                    m.pos(23, 21)
                    m.color(m.vert)
                    m._print('Next page →')
                    m.underline()
                    m._print(' ')
                    m.inverse()
                    m.color(m.cyan)
                    m._print('_SUITE  ')

                m.pos(22, 1)
                m._print('Your Choice:')
                m.pos(23, 5)
                m._print(' + →')

                m.underline()
                m._print(' ')
                m.inverse()
                m.color(m.cyan)
                m._print('_ENVOI ')
                m.pos(24, 1)
                m.color(m.vert)
                m._print("Manual →")
                m.underline()
                m._print(' ')
                m.inverse()
                m.color(m.cyan)
                m._print("_GUIDE ")
                m.pos(24, 26)
                m.color(m.vert)
                m._print("Home → ")
                m.inverse()
                m.color(m.cyan)
                m._print("SOMMAIRE")
            
            elif db_num == 0:
                print("0 Data... und raus")
                break
            else:
                page = abs(page)
        # attente saisie
            (choix, touche) = m.input(23, 1, 3, sltime)
            if not isinstance(choix,int):
                if not choix.isdigit():
                    choix = 0
                choix = int(choix)
            m.clear            
            m.cursor(False)
            if touche == m.suite:
                if page*5 < len(res):
                    page = page + 1
                else:
                    m.bip()
            elif touche == m.retour:
                if page > 1:
                    page = page - 1
                else:
                    m.bip()
            elif touche == m.envoi:
                if choix > db_num:
                    m.home()
                    m.message(10, 7, 3," This wish doesn't exist "+ str(db_num), bip=True)
                    return            
                r = res[choix-1]
                choix_lfd = r[0]
                print("auswahl Wish: " + str(choix) + " Lfd: " + str(choix_lfd))
                break
                
            elif touche == m.guide:
                break
            elif touche == m.sommaire: 
                break
            elif touche == m.annulation:  # retour saisie pour correction
                break
            elif touche == m.correction:  # retour saisie pour correction
                break
            elif touche != m.repetition:
                m.bip()
                page = -page  # pas de ré-affichage
        
        print("auswahl Wish choix: " + str(choix) + " & Touche " + str(touche))
        if touche == m.guide:
            self.changeState( self.stateInfo1 )
        if touche == m.sommaire:
            self.changeState( self.stateWelcome )
        if touche == m.annulation or touche == m.correction:
            print('Annu or corr')
            return()
        if touche == m.envoi and choix > 0:
            if choix > db_num:
                m.home()
                m.message(10, 7, 3," This wish doesn't exist "+ str(db_num), bip=True)
                return()
            print("CHoix > 0")
            m.home()
            m.message(15, 7, 2,"Data N° "+ str(choix)+ "will be deleted", bip=True)
            # Define SQL statement with WHERE clause to delete specific record
            sql = "DELETE FROM wishes WHERE lfd = %s"
            data = (choix_lfd ,)  # Specify the value for the 'lfd' field to be deleted
            # Execute SQL statement with provided value
            db_cursor.execute(sql, data)
            db_conn.commit()                        
            print("Anzahl Datensätze nach delete: " + str(db_num))              
            # Änderungen in der Datenbank speichern
            db_conn.commit()
            return()                
        elif touche == m.envoi and choix < 0:
            print("CHoix <= 0")
            self.changeState( self.stateWelcome )
        if db_num == 0:
            self.changeState( self.stateWelcome )

####
# Program entry point
###
def main():
    
   
    global db_conn, db_cursor, data, ver

    # Define Version
    ver = "1.2"
    print( "WISH WIZARD " , ver)
    # create state machine object
    stateMachine=StateMachine()
    
    # Prepare dataobject with all Screen txts in diff languages
    csv_dateipfad = 'WM/lang.csv'
    data = create_data(csv_dateipfad) # to function
    
    # Prepare db and create if not exist from mariadb
    # and decision if local or client on 
    try:
        db_conn = mysql.connector.connect(
            host = '192.168.0.99',
            user = 'utilisateur1',
            password = '',
            database = 'minitel'
            )
        print("Connected to .99")
    except:
        db_conn = mysql.connector.connect(
            host = 'localhost',
            user = 'utilisateur1',
            password = '',
            database = 'minitel'
            )
        print("Connected to Local ")
    
        
    db_cursor = db_conn.cursor()    
    sql_anweisung1 = """
    CREATE TABLE IF NOT EXISTS wishes (
        lfd INTEGER,
        titel VARCHAR(24), 
        descr1 VARCHAR(24),
        descr2 VARCHAR(24),
        descr3 VARCHAR(24),
        name VARCHAR(24), 
        rated VARCHAR(1),
        find VARCHAR(24),
        fullfilled VARCHAR(1)
        );"""
    db_cursor.execute(sql_anweisung1)
    # Überprüfen, ob die Tabelle existiert
    db_cursor.execute("SHOW TABLES LIKE 'pref'")
    table_exists = db_cursor.fetchone()

    # Wenn die Tabelle noch nicht existiert, Tabelle erstellen und Daten einfügen
    if not table_exists:
        db_cursor.execute("""
            CREATE TABLE pref (
                id INT PRIMARY KEY,
                IP_adr VARCHAR(50),
                timer INT
            )
        """)
        db_cursor.execute("INSERT INTO pref (id, IP_adr, timer) VALUES (1, 'localhost', 30)")
        # Transaktion bestätigen
        db_conn.commit()
        print("Tabelle erstellt und Daten eingefügt.")
    else:
        print("Tabelle existiert bereits.")

    # Verbindung schließen
    db_cursor.close()                      

    # Prepa divers
    global m
    if len(sys.argv) > 2:
        (choice, ou) = (sys.argv[1], sys.argv[2])
    else:
        (choice, ou) = ('', '')
    
    print( "Bis hier erstmal" )
    ###
    # Main loop
    ###
    while True:
        stateMachine.update()
        
# start
if __name__ == '__main__':
    main()

exit();

#************************************** old stuff, and snipps
