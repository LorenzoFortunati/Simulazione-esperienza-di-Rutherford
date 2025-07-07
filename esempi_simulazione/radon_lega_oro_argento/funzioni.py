import random
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import colors
import math
from mpl_toolkits.mplot3d import Axes3D 



costante_dielettrica_vuoto = 8.9*10**(-12) #C2/(N·m2)
carica_elettrone =  -1.602*10**(-19) #couloumb 
carica_particella_alfa = 2*carica_elettrone
massa_particella_alfa = 1.660539040*10**( -27 ) #kg
velocita_luce = 299792458 #m/s
tangente_angolo_diffusione = "da mettere"
carica_elettroni_oro = carica_elettrone * 79
carica_elettroni_argento = carica_elettrone * 47
distanza_atomi = 4.08*10**(-10) #metri-->fonte chat gpt
z_oro = 79
z_argento = 47

raggio_atomico = 10**(-10) #metri

cost = ( carica_elettrone ** 2 ) / ( 2 * np.pi * costante_dielettrica_vuoto )




"""
SORGENTI RADIOATTIVE
"""


def mev_joule( energia_in_mev ) :

    """
    Descrizione
    -----------

        funzione che ha come input ha l'energia cinetica in mev e come output restituisce l'energia cinetica in joule.

    Parametri
    -----------

        energia_in_Mev : energia delle particelle in Mev
    
    Restituisce
    -----------

        energia_joule : energia in joule delle particelle della sorgente 

    """

    energia_joule = energia_in_mev * (10**6) * carica_elettrone 
    energia_joule = -1*energia_joule 

    return energia_joule


"""CREAZIONE FORO DI COLLIMAZIONE E DISTANZA SORGENTE-FORO"""

#generazione particelle alfa

def generazione_particelle_alpha( distanza , numero ) :

    """
    Descrizione
    -----------

        funzione utilizzata per generare N particelle, con N prefissato a 10^6, con distribuzione uniforme su tutto l'angolo solido.
        tale funzione inoltre restituisce le coordinate cartesiane e gli angoli principali di ogni particella generata, ossia sia le coordinate cartesiane
        che le stesse in sferiche.

    Parametri
    -----------
        
        distanza : numero che definisce la distanza in metri della sorgente dal foro di collimazione
        numero : è il numero di particelle alfa generato dalla sorgente radioattiva, fissato per default a 10^6 particelle.
    
    Restituisce
    -----------

        direzionez : np.array di dimensione pari al numero di particelle che ha in sè le coordinate lungo z di ciascuna particella
        direzioney : np.array di dimensione pari al numero di particelle che ha in sè le coordinate lungo y di ciascuna particella
        angolo_phi : np.array di dimensione pari al numero di particelle che ha in sè l'angolo compreso nel piano xy usato per definire x ed y della particella
        angolo_teta: np.array di dimensione pari al numero di particelle che ha in sè l'angolo compreso tra z e il vettore posizione che individua la particella
    
    """

    #generazione di particelle alfa con distribuzione uniforme su tutto l'angolo solido
    angolo_phi = np.random.uniform( low=0, high=2*np.pi , size = numero )
    angolo_teta = np.random.uniform( low=0, high=np.pi , size = numero )

    #calcolo le componenti cartesiane delle particelle

    direzionez = []
    direzioney = []
    
    #creo un ciclo for per togliere le particelle problematiche e creare le coordinate di tutte le particelle, per poi selezionare solo quelle non problematiche.

    for i in range( 0 , numero , 1 ) :

        #problema per y

        mask1 = ( ( np.abs( angolo_teta[i] - np.pi/2) < 1e-8 ) or ( np.abs(angolo_teta[i] - (3/2)*np.pi) < 1e-8 ) )

        #problema per z

        mask2 = (( ( angolo_teta[i] == 0 ) or ( np.abs(angolo_teta[i] - np.pi) < 1e-8 ) ) and ( ( np.abs(angolo_phi[i] - np.pi/2) < 1e-8 ) or ( np.abs(angolo_phi[i] - (3/2)*np.pi) < 1e-8) ))

        if mask1 or mask2 :

            pass

        else :

            y = distanza * math.tan( angolo_phi[i] )
            z = distanza / ( math.tan( angolo_teta[i] ) * math.cos( angolo_phi[i] ) )
            direzioney.append( y )
            direzionez.append( z )

            #print( f"\ncoordinata y: {y}\ncoordinata z: {z}" )
        
    
    direzionez = np.array(direzionez)
    direzioney = np.array(direzioney)

    #questi sotto posso direttamente crearli come np.array all'inizio credo.
    angolo_phi = np.array(angolo_phi)
    angolo_teta = np.array( angolo_teta )

    return  direzionez , direzioney , angolo_phi , angolo_teta

def particelle_alfa_sopravvissute_fino_prima_lamina( numero , raggio , direzionez , direzioney , angolo_phi , angolo_teta) : 
 
    """
    Descrizione
    -----------

        funzione utilizzata per selezionare solo le particelle che sopravvivono tra le N generate dalla funzione generazione_particelle_alpha
        tale funzione inoltre restituisce le coordinate cartesiane e gli angoli principali di ogni particella sopravvissuta al foro circolare,
        ossia sia le coordinate cartesiane che le stesse in sferiche.

    Parametri
    -----------

        numero : è il numero di particelle alfa generato dalla sorgente radioattiva, fissato per default a 10^6 particelle.
        raggio : numero che definisce il raggio del foro di collimazione
        direzionez : np.array di dimensione pari al numero di particelle che ha in sè le coordinate lungo z di ciascuna particella
        direzioney : np.array di dimensione pari al numero di particelle che ha in sè le coordinate lungo y di ciascuna particella
        angolo_phi : np.array di dimensione pari al numero di particelle che ha in sè l'angolo compreso nel piano xy usato per definire x ed y della particella
        angolo_teta: np.array di dimensione pari al numero di particelle che ha in sè l'angolo compreso tra z e il vettore posizione che individua la particella
    
        
    Restituisce
    -----------

        z : np.array di dimensione pari al numero di particelle alfa che hanno superato il foro di collimazione che ha in sè le coordinate lungo z di ciascuna particella
        y : np.array di dimensione pari al numero di particelle alfa che hanno superato il foro di collimazione che ha in sè le coordinate lungo y di ciascuna particella
        angolo_phi_rimanente : np.array di dimensione pari al numero di particelle che hanno superato il foro di collimazione che ha in sè l'angolo compreso nel piano xy usato per definire x ed y della particella
        angolo_teta_rimanente : np.array di dimensione pari al numero di particelle che hanno superato il foro di collimazione che ha in sè l'angolo compreso tra z e il vettore posizione che individua la particella
    
    """

    #particelle che cadono dentro l'angolo solido che sottende il foro circolare.
    
    angolo_phi_rimanente = [] 
    angolo_teta_rimanente = []
    
    y = []
    z = []

    #qui stabilisco quali particelle sopravvivono una volta attraversato il foro

    for i in range( 0 , numero , 1 ) :
        
        confronto = ( ( direzioney[i] ** 2 ) + ( direzionez[i] ** 2 ) ) ** 0.5
        if  raggio > confronto :

            angolo_phi_rimanente.append( angolo_phi[ i ] )
            angolo_teta_rimanente.append( angolo_teta[ i ] )

            
            #print( 1/np.cos(angolo_phi[i]) , "\n") #tutti all'incirca confrontabili con 1--->va bene e non fa esplodere z all'infinito
            

            y.append( direzioney[ i ] )
            z.append( direzionez[ i ] )

    #converto le liste in np.array

    z = np.array(z)
    y = np.array(y)
    angolo_phi_rimanente = np.array( angolo_phi_rimanente )
    angolo_teta_rimanente = np.array( angolo_teta_rimanente )
  
    return  z , y , angolo_phi_rimanente , angolo_teta_rimanente


def calcolo_coordinate_cartesiane_nota_x_e_angoli( lunghezza_x , numero , angolo_phi , angolo_teta ) :
    
    """
    Descrizione
    -----------

        funzione che in input vuole il valore della coordinata x delle particelle sulla lamina, il numero delle particelle che si tiene in considerazione(numero) 
        e gli angoli delle particelle varie.
        mi restituisce le coordinate cartesiane delle componenti y e z quando la particella si trova sulla lamina

    Parametri
    -----------

        lunghezza_x : parametro che è uguale per tutte le particelle e che corrisponde alla posizione di una lamina generica per quelle che si hanno a disposizione 
        numero : è il numero di particelle 
        angolo_phi : np.array di dimensione pari al numero di particelle che ha in sè l'angolo compreso nel piano xy usato per definire x ed y della particella
        angolo_teta: np.array di dimensione pari al numero di particelle che ha in sè l'angolo compreso tra z e il vettore posizione che individua la particella
    
        
    Restituisce
    -----------

        direzionez : np.array di dimensione pari al numero di particelle alfa con in sè le coordinate lungo z delle particelle
        direzioney : np.array di dimensione pari al numero di particelle alfa con in sè le coordinate lungo y delle particelle

    """

    direzioney = []
    direzionez = []


    for i in range( 0 , numero , 1 ) :

        #problema per y

        mask1 = ( ( abs(angolo_phi[i] - np.pi/2) < 1e-8 ) or ( abs(angolo_phi[i] - np.pi*(3/2) < 1e-8 ) ) )

        #problema per z

        mask2 =(( ( angolo_teta[i] == 0 ) or ( np.abs(angolo_teta[i] - np.pi )) < 1e-8 ) and ( ( np.abs(angolo_phi[i] - np.pi/2 )) < 1e-8 or ( np.abs(angolo_phi[i] - (3/2)*np.pi)) < 1e-8))
   
        
        if mask1 or mask2 :

            pass
            
        else :

            y = lunghezza_x * math.tan( angolo_teta[i] )
            z = lunghezza_x / ( math.tan( angolo_teta[i] ) * math.cos( angolo_phi[i] ) )
            direzionez.append( z )
            direzioney.append( y )

    direzioney = np.array( direzioney )
    direzionez = np.array( direzionez )

    return direzionez , direzioney



""" CREAZIONE LAMINE """

def posizione_lamine_lungo_x( ) :

    """
    Descrizione
    -----------

        funzione che in input non ha nulla e che restituisce il numero di lamine utilizzato e un np.array costituito dalle distanze
        di tutte le lamine dal foro di collimazione.
        dentro a tale funzione ci sono controlli nell'eventualità l'utente metta per due lamine diverse la stessa distanza e 
        implementazioni che permettono di ordinare le lamine in ordine crescente se l'utente si sbaglia ad ordinare le lamine stesse.
        

    Parametri
    -----------

        nessun parametro
        
    Restituisce
    -----------

        array_che_definisce_la_distanza_di_tutte_le_lamine : np.array con dimensione pari al numero lamine che ha in sè la distanza di ogni lamina dal foro di collimazione.
        numero_lamine : parametro intero che definisce il numero di lamine scelto per l'esperimento e che corrisponde alla dimensione dell'array sopradefinito
    
    """
    numero_lamine = 1
    array_che_definisce_la_distanza_di_tutte_le_lamine = []

    #creo l'array che ha per elementi la distanza di ogni lamina dal foro

    
    for i in range( 0 , numero_lamine , 1 ) :
        
        distanza = input(f"\nSi inserisca la distanza in centimetri della lamina {i + 1} dal foro, avendo cura che le lamine rientrino tutte in un range compreso in 50cm: ")
        distanza = float(distanza)

        while( distanza > 50  or distanza < 0 ) :

            distanza = input("\nil valore scelto per la lamina non va bene poichè fuori range.Si inserisca la distanza in centimetri della lamina {i + 1} dal foro, avendo cura che le lamine rientrino tutte in un range compreso in 50cm: ")
        
        distanza = distanza/100

        array_che_definisce_la_distanza_di_tutte_le_lamine.append( distanza )
        print(f"\nla distanza scelta per la lamina  { i + 1 }   è: { distanza } metri\n")

    #converto ora la lista in array

    array_che_definisce_la_distanza_di_tutte_le_lamine = np.array( array_che_definisce_la_distanza_di_tutte_le_lamine )

    #tolgo eventuali doppioni

    array_che_definisce_la_distanza_di_tutte_le_lamine = np.unique(array_che_definisce_la_distanza_di_tutte_le_lamine)
    numero_lamine = len(array_che_definisce_la_distanza_di_tutte_le_lamine)

    #così sono sicuro che le lamine siano in ordine crescente

    print("\nNOTA-->se ad esempio la lamina 3 è posta prima della lamina 2, l'array con le distanze delle lamine verrà ordinato in ordine crescente per le stesse.\n")

    array_che_definisce_la_distanza_di_tutte_le_lamine.sort()

    #rifaccio vedere l'array ordinato con tutte le relative distanze

    for i in range( 0 , numero_lamine , 1 ) :
        
        print(f"\nla distanza scelta per la lamina  { i + 1 }   è: { array_che_definisce_la_distanza_di_tutte_le_lamine[i] } metri\n")

    return array_che_definisce_la_distanza_di_tutte_le_lamine , numero_lamine

"""PRE-DEFLESSIONE""" 


def oro_o_argento( ) :

    """
    Descrizione
    -----------

        funzione che in input riceve gli array con la composizione in percentuale delle lamine in oro o argento e restituisce un array
        di elementi pari al numero di lamine che rappresentano il numero atomico dell'oro o argento dell'atomo con il quale avviene la deflessione.

    Parametri
    -----------
        
    Restituisce
    -----------

        numero_atomico : array con dimensione pari a numero_lamine che ha come elementi il numero atomico dell'atomo con il quale la particella alfa ha l'interazione.
    
    """

    #inizializzo l'array che poi sarà restituito come output della funzione.

    numero_atomico = 0
    percentuale_oro = 55
    

    #creo un array per sorteggiare i numeri che poi sfrutterò per stabilire se sarà oro o argento

    numeri = list(range(1, 101))
   
    

    numero_estratto = random.choice(numeri)
    

    if numero_estratto < np.max( percentuale_oro ) :

        numero_atomico = z_oro

    else :

        numero_atomico = z_argento

    

    return numero_atomico 

    
 
def angolo_deflessione( numero_lamine , energia_in_joule , numero_atomico , energia_mev) : #per ogni particella ho un angolo di deflessione valido per tutte le lamine.

    """
    Descrizione
    -----------

        funzione che, data una particella, restituisce l'angolo di deflessione che essa avrà dopo l'interazione con ogni lamina
    
    Parametri
    -----------

        numero_lamine : parametro che serve per definire il numero di lamine dell'esperimento
        energia_joule : energia in joule delle particelle della sorgente 
        numero_atomico : array con dimensione pari a numero_lamine che ha come elementi il numero atomico dell'atomo con il quale la particella alfa ha l'interazione.
        energia_mev : energia in Mev delle particelle della sorgente
        
    Restituisce
    -----------

        deflessione : np.array con la dimensione pari a numero_lamine che ha per elementi l'angolo di deflessione che una particella ha con tutte le lamine.
    
    """


    #creo un array con tutti i possibili valori dell'angolo theta che può assumere, non considerando lo 0 perchè il parametro d'impatto divergerebbe
    

    costante = cost / energia_in_joule
    deflessione = []
    numero_atomico = z_oro

    # Determina il range del parametro d'impatto b in base all'energia

    if 10 <= energia_mev <= 50:

        b_min, b_max = 1e-13, 1e-9

    else:

        b_min, b_max = 1e-14, 1e-10
    
    for i in range( 0 , numero_lamine , 1 ):

        # Campiona b con distribuzione uniforme nello spazio (p(b) ∝ b)

        u = np.random.uniform(0, 1)
        b = np.sqrt(u * (b_max**2 - b_min**2) + b_min**2)
        
        # Calcolo angolo di deflessione (formula di Rutherford)

        valore = costante * numero_atomico  / b
        theta = 2 * np.arctan(valore)
        
        deflessione.append( theta )

    

    deflessione = np.array(deflessione)
    
    return deflessione

"""DEFLESSIONE E SCHERMO SENSIBILE"""

def creazione_schermo_sensibile_circolare( array_che_definisce_la_distanza_di_tutte_le_lamine , numero_lamine ) :

    """
    Descrizione
    -----------

        funzione che mi permette di costruire le grandezze principali per lo schermo sensibile circolare sul quale verranno rivelate eventualmente
        le particelle.
        tale funzione inoltre controlla che tutte le lamine si trovino dentro il foro circolare, altrimenti se tale condizione non è soddisfatta, 
        verrà richiesto di reinserire i vari dati.
    
    Parametri
    -----------

        array_che_definisce_la_distanza_di_tutte_le_lamine : np.array con dimensione pari al numero lamine che ha in sè la distanza di ogni lamina dalla sorgente.
        numero_lamine : parametro che serve per definire il numero di lamine dell'esperimento.
        
    Restituisce
    -----------

        raggio_schermo : numero che definisce il raggio dello schermo sensibile
        numero_divisioni_circonferenza : numero che definisce in quante parti si è suddivisa la circonferenza dello schermo sensibile
        base_pixel : numero che definisce la grandezza della base del pixel
        altezza_pixel : numero che definisce la grandezza dell'altezza del pixel
        divisione_altezza : numero che definisce in quante parti si è suddivisa l'altezza dello schermo sensibile
        altezza_schermo : numero che definisce l'altezza dello schermo sensibile

    """
    
    modifica = "si"

    distanza_di_riferimento = array_che_definisce_la_distanza_di_tutte_le_lamine[numero_lamine - 1]
    raggio_schermo = 0
    altezza_pixel = 0
    base_pixel = 0
    divisione_altezza = 0
    altezza_schermo = 0
    numero_divisioni_circonferenza = 0

    while modifica == "si" :

        #input utente
        altezza_pixel = float(input("\nInserisci l'altezza (lunghezza lungo z) in cm per ogni pixel dello schermo sensibile avendo cura che sia maggiore a 5 cm: "))
        print(f"\nScelta altezza pixel (lungo x): {altezza_pixel} cm")

        base_pixel = float(input("\nInserisci la base (lunghezza lungo circonferenza in yz) in cm per ogni pixel dello schermo sensibile avendo cura che sia maggiore a 5 cm: "))
        print(f"\nScelta base pixel (lungo circonferenza): {base_pixel} cm")

        while (altezza_pixel < 5 and base_pixel < 5 ):

            print("\ni valori scelti non vanno bene poichè inferiori al limite inferiore richiesto.reinserire i valori.\n")
            
            altezza_pixel = float(input("\nInserisci l'altezza (lunghezza lungo z) in cm per ogni pixel dello schermo sensibile: "))
            print(f"\nScelta altezza pixel (lungo x): {altezza_pixel} cm")

            base_pixel = float(input("\nInserisci la base (lunghezza lungo circonferenza in yz) in cm per ogni pixel dello schermo sensibile: "))
            print(f"\nScelta base pixel (lungo circonferenza): {base_pixel} cm")


        #converto in metri
        altezza_pixel = altezza_pixel / 100 
        base_pixel = base_pixel / 100

        #parametri schermo sensibile circolare

        divisione_altezza = 100  # numero di pixel lungo z
        altezza_schermo = divisione_altezza * altezza_pixel

        numero_divisioni_circonferenza = 100
        raggio_schermo = base_pixel / (2 * np.pi / numero_divisioni_circonferenza)


        while distanza_di_riferimento >= raggio_schermo :

            print( f"\nmi spiace, ma i valori scelti non sono consoni al setup sperimentale poichè l'ultima lamina si trova fuori allo schermo sensibile.\nreinserire i dati:\n")
            print( f"\nsi mette qua per sicurezza tutte le distanze delle lamine dalla sorgente: {array_che_definisce_la_distanza_di_tutte_le_lamine}")
            print( f"\nil valore scelto limite è {raggio_schermo} che è uguale ad {base_pixel} / ({2*np.pi} x {numero_divisioni_circonferenza}).\n")

            base_pixel = float(input("\nInserisci la base (lunghezza lungo circonferenza in xy) in cm per ogni pixel dello schermo sensibile: "))
            print(f"\nScelta base pixel (lungo circonferenza): {base_pixel} cm")

            #converto in metri
            altezza_pixel = altezza_pixel / 100 
            base_pixel = base_pixel / 100

            
            numero_divisioni_circonferenza = 100
            raggio_schermo = base_pixel / (2 * np.pi / numero_divisioni_circonferenza)

            
        print(f"\nscrivere 'si' se si vuole modificare i parametri scelti.\nscrivere 'no' o qualsiasi altra cosa se vanno bene i valori scelti:")
        modifica = input()
    
    print(f"\ni valori scelti vanno bene per il setup sperimentale.\n")

    return raggio_schermo , numero_divisioni_circonferenza , base_pixel , altezza_pixel , divisione_altezza , altezza_schermo 
    


def ultima_interazione( x0 , y0 , z0 , angolo_deflesso , numero_lamine, raggio_schermo, altezza_schermo ) :

    """
    Descrizione
    -----------

        funzione che mi permette di definire l'ultima interazione delle particelle con l'ultima lamina.
        mi restituisce la posizione delle particelle sullo schermo sensibile in coordinate cartesiane.
    
    Parametri
    -----------

        x0 : numero che definisce la posizione della particella lungo x sull'ultima lamina prima che avvenga l'interazione.
        y0 : numero che definisce la posizione della particella lungo y sull'ultima lamina prima che avvenga l'interazione.
        z0 : numero che definisce la posizione della particella lungo z sull'ultima lamina prima che avvenga l'interazione.
        angolo_deflesso : angolo di deflessione che la particella ha dopo l'ultima lamina.
        numero_lamine : parametro che serve per definire il numero di lamine dell'esperimento.
        raggio_schermo : numero che definisce il raggio dello schermo sensibile.
        altezza_schermo : numero che definisce l'altezza dello schermo sensibile.

    Restituisce
    -----------

        x : parametro che mi definisce la posizione lungo x della particella quando si trova sullo schermo sensibile
        y : parametro che mi definisce la posizione lungo y della particella quando si trova sullo schermo sensibile
        z : parametro che mi definisce la posizione lungo z della particella quando si trova sullo schermo sensibile

    """
    angolo_teta_f = 0

    if numero_lamine > 1 :

        angolo_teta_f = angolo_deflesso[numero_lamine-1]
    
    if numero_lamine == 1 :

        angolo_teta_f = angolo_deflesso

    #inizializzo dei valori per le coordinate

    x = 0
    y = 0 
    z = 0
    xf = 0 
    yf = 0
    zf = 0

    angolo_phi = np.random.uniform( 0 , 2*np.pi )

    #problema y
    
    mask_yf = ( ( np.abs(angolo_phi - np.pi/2) < 1e-8 ) or ( np.abs(angolo_phi - (3/2)*np.pi) < 1e-8 ) )
    
    
    #problema z
    
    mask_zf = ( ( angolo_teta_f == 0 ) or ( np.abs(angolo_teta_f - np.pi )) < 1e-8 ) 
    
    #con questa condizione, le particelle vengono comunque rilevate

    if( not(mask_yf ) and not(mask_zf )) :
        
        #equazione per trovare xf, ossia la posizione x della particella sullo schermo circolare rispetto all'ultima lamina.
        
        a = 1 + (math.tan(angolo_teta_f) * math.sin(angolo_phi ))**2
        b = 2* (x0 + math.tan(angolo_teta_f) * math.sin(angolo_phi *y0 ))
        c = x0**2 + y0**2 - raggio_schermo**2 
       
        coefficienti = [ a , b , c ]
        soluzioni = np.roots( coefficienti )
        
        for soluzione_positiva in soluzioni :
            
            discriminante = b**2 - 4*a*c
          
            #prendo la soluzione positiva perchè lo schermo sensibile è posto dopo le lamine--->la soluzione negativa è per lo schermo sensibile posto prima delle lamine.
            
            if soluzione_positiva > 0 and discriminante >= 0 :
                
                xf = soluzione_positiva
            
                #ho il modulo finale delle particelle, ossia raggio_schermo, così impongo che debbano stare su tale schermo
                
                yf = xf*math.tan(angolo_teta_f)*math.sin(angolo_phi)
                zf = xf*math.tan(angolo_teta_f)*math.cos(angolo_phi)
                x = xf + x0
                y = yf + y0
                z = zf + z0 
    
                
                if np.abs(z) > altezza_schermo/2 : 
                   
                    #mettendo questi valori alti, ho che le particelle non vengono rilevate perchè sparate via.
                   
                    x = 10000
                    y = 10000
                    z = 10000
                
                else :
                    
                    #conosco quindi la posizione delle particelle sullo schermo sensibile
                    
                    pass
            else :
                
                #se non ho soluzioni positive, allora significa che la particella non viene rivelata.
                
                x = 100000
                y = 100000
                z = 100000
            
    else:
        
        x = 10000
        y = 10000
        z = 10000
    
    return x , y , z
   

"""RILEVAZIONE PARTICELLE"""

def rilevazione_particelle ( posizione_x , posizione_y , posizione_z , raggio_schermo , numero_divisioni_circonferenza , altezza_pixel , divisione_altezza , posizione_lamine , foro_sorgente, raggio_foro_collimazione , numero_lamine  ) :
    

    """
    Descrizione
    -----------

        funzione che mi permette visualizzare le particelle sullo schermo sensibile, lo schermo sensibile stesso con le varie griglie scelte dall'utente, le lamine, la sorgente
        e il foro di collimazione.
    
    Parametri
    -----------
    
        posizione_x : np.array che ha come elementi tutte le coordinate cartesiane lungo x delle particelle sullo schermo sensibile.
        posizione_y : np.array che ha come elementi tutte le coordinate cartesiane lungo y delle particelle sullo schermo sensibile.
        posizione_z : np.array che ha come elementi tutte le coordinate cartesiane lungo z delle particelle sullo schermo sensibile.
        raggio_schermo : numero che definisce il raggio dello schermo sensibile
        numero_divisioni_circonferenza : numero che definisce in quante parti si è suddivisa la circonferenza dello schermo sensibile
        altezza_pixel : numero che definisce la grandezza dell'altezza del pixel
        divisione_altezza : numero che definisce in quante parti si è suddivisa l'altezza dello schermo sensibile
        posizione_lamine : np.array che ha come elementi la posizione di tutte le lamine lungo x.
        foro_sorgente : numero che definisce la distanza tra il foro di collimazione e la sorgente.
        raggio_foro_collimazione : numero che definisce il raggio del foro di collimazione.
        numero_lamine : parametro che serve per definire il numero di lamine dell'esperimento.
    
    Restituisce
    -----------

       restituisce una visualizzazione tridimensionale di tutto l'apparato sperimentale con le varie particelle sopravvissute fino allo schermo circolare.

    """

    #Setup figura
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #Disegno circonferenze (nel piano xy ), per ogni z( voglio uno schermo sensibile che non parte da zero )

    num_punti = 1000
    theta = np.linspace(0, 2 * np.pi, num_punti)
    altezza = altezza_pixel * divisione_altezza

    for i in range( 0 , divisione_altezza + 1 , 1 ) :

        segmento_z = ( - altezza / 2 ) + (  i * altezza_pixel )
        x_circ = raggio_schermo * np.cos(theta)
        y_circ = raggio_schermo * np.sin(theta)

        #creo un array da plottare della dimensione di x_circ o y_circ con tutti valori pari a segmento_z

        z_per_costruzione = np.full_like( y_circ, segmento_z )

        #plotto i punti sul grafico con la funzione plt.plot() che unisce con linee tutti i punti degli array.

        ax.plot(x_circ, y_circ, z_per_costruzione , color='black' )
    
    ax.plot([], [], [], color='black', label='griglia dello schermo sensibile')

    #linee longitudinali lungo z

    z_l = np.linspace( - altezza / 2 , altezza / 2 , num_punti )
    theta_l = np.linspace( 0 , 2 * np.pi , numero_divisioni_circonferenza )

    for i in range( 0 , numero_divisioni_circonferenza , 1 ) :

        #creo i valori fissi per x ed y sui quali poi costruisco le linee longitudinali
        x_c = raggio_schermo * np.cos(theta_l[i])
        y_c = raggio_schermo * np.sin(theta_l[i])


        #creo gli array da plottare
        x_l = np.full_like( z_l , x_c )
        y_l = np.full_like( z_l , y_c )

        ax.plot( x_l , y_l , z_l , color = "black")

    #aggiungo la sorgente
    ax.scatter( [0] , [0] , [0] , color = "yellow" , s = 250 , marker ='.' , label = "sorgente")

    
    #aggiungo le varie lamine come rettangoli blu

    larghezza_lamina = altezza_pixel * 5
    altezza_lamina = altezza_pixel *10

    for i in range( 0 , numero_lamine , 1 ) :

        # Coordinate dei 4 vertici del rettangolo piano in yz (a x costante)
        y_lamina = np.array([-larghezza_lamina/2, larghezza_lamina/2, larghezza_lamina/2, -larghezza_lamina/2, -larghezza_lamina/2])
        z_lamina = np.array([-altezza_lamina/2, -altezza_lamina/2, altezza_lamina/2, altezza_lamina/2, -altezza_lamina/2])
        x_lamina = np.full_like(y_lamina, posizione_lamine[i] )
    
        ax.plot( x_lamina , y_lamina , z_lamina , color="blue")

    ax.plot( [] , [] , [] , color="blue" , label = "lamina")






    #aggiungo il foro circolare
    
    theta_foro = np.linspace(0, 2 * np.pi, num_punti )

    y_foro = raggio_foro_collimazione * np.cos(theta_foro)
    z_foro = raggio_foro_collimazione * np.sin(theta_foro)
    x_foro = np.full_like(y_foro, foro_sorgente)

    ax.plot(x_foro, y_foro, z_foro, color="green", label="foro circolare")

    #aggiungo le sole particelle rilevate
    ax.scatter( posizione_x , posizione_y , posizione_z , color = "red" , label = "particelle sopravvissute fino all'ultima interazione")
    


    #Etichette
    ax.set_xlabel('Asse X (lunghezza del cilindro)')
    ax.set_ylabel('Asse Y (raggio/circonferenza)')
    ax.set_zlabel('Asse Z (raggio/circonferenza)')
    ax.set_title('Schermo sensibile cilindrico con asse parallelo a Z')
    ax.legend()

    return plt.show()


