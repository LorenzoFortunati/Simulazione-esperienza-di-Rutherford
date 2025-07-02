
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import colors
import math
from mpl_toolkits.mplot3d import Axes3D 



#valori importanti
costante_dielettrica_vuoto = 8.9*10**(-12) #C2/(N·m2)
carica_elettrone =  1.602*10**(-19) #couloumb 
carica_particella_alfa = 2*carica_elettrone
massa_particella_alfa = 1.660539040*10**( -27 ) #kg
velocita_luce = 299792458 #m/s
carica_elettroni_oro = carica_elettrone * 79
carica_elettroni_argento = carica_elettrone * 47

z_oro = 79
z_argento = 47

raggio_atomico = 10**(-10) #metri


cost = ( carica_elettrone ** 2 ) / ( 2 * np.pi * costante_dielettrica_vuoto )

#aggiungo il pathname e il percorso alla cartella dove ci sono tutti i file

import funzioni

energia_mev = 7.7
energia_joule = funzioni.mev_joule( energia_mev )

print( "il corrispondente valore dell'energia in Joule scelto è di: " , energia_joule , " J" )

costante =  cost / energia_joule
#è piccolissimo il valore costante.

print(f"\nil valore che sarà sempre costante vale: {costante}\n")


#velocità particelle--->vedere se possa servire

velocita_particelle = ( ( 2 * energia_joule ) / massa_particella_alfa ) ** 0.5 

""" CREAZIONE FORO DI COLLIMAZIONE E DISTANZA SORGENTE-FORO"""

#scelgo la distanza del foro di collimazione dalla sorgente

distanza = input( "\nsi scriva in millimetri la distanza del foro di collimazione dalla sorgente, avendo cura che quest'ultima sia tra 1 mm e 10 mm:\n " )
distanza = float( distanza )

while ( distanza > 10 or distanza < 1 ) :
    
    print("\nil valore scelto non va bene.")
    distanza = input( "si scriva in millimetri la distanza del foro di collimazione dalla sorgente, avendo cura che quest'ultima sia tra 1 mm e 10 mm.\n" )
    distanza = float( distanza )


#converto in metri
distanza = distanza / 1000

#scelgo il raggio del foro di collimazione, in millimetri perchè devo avere un fascio collimato(addirittura anche micrometri andrebbero bene)

raggio = input( "\nsi inserisca la grandezza del raggio del foro di collimazione in micrometri, avendo cura che quest'ultimo sia tra 1micrometro e 1mm :\n " )
raggio = float( raggio )

while ( raggio > 10 or raggio < 1 ) :
    
    print("\nil valore scelto non va bene.\n")
    raggio = input( "\nsi scriva in micrometri la grandezza del raggio del foro di collimazione dalla sorgente, avendo cura che quest'ultima sia tra 1 mm e 10 micrometri:\n " )
    raggio = float( raggio )

#il raggio in metri è il raggio stesso diviso 1000

raggio = raggio / 1000

#metto per default il  numero delle particelle alfa

numero = 100000

#forse di default sarebbe meglio metterlo a 1000

#genero le posizioni delle particelle alfa

direzionez , direzioney , angolo_phii , angolo_tetaa = funzioni.generazione_particelle_alpha( distanza , numero )

numero = len( direzioney ) #importante!!! ho tolto tutte le particelle problematiche in y e z.

#vedo quali particelle sopravvivono dopo il foro

z , y , angolo_phi, angolo_teta  = funzioni.particelle_alfa_sopravvissute_fino_prima_lamina( numero , raggio , direzionez , direzioney , angolo_phii , angolo_tetaa ) 
x = np.full_like( y , distanza ) #posso modificare i 2 codici facendo si che x sia sono un valore e non un array/lista, così ottimizzo e salvo memoria.
dimensione = len( z )



print(f"\nil numero di particelle sopravvissute dopo il foro è di: { dimensione }\n")

""" CREAZIONE LAMINE """



#creo l'array che definisce la distanza di tutte le lamine

array_che_definisce_la_distanza_di_tutte_le_lamine , numero_lamine = funzioni.posizione_lamine_lungo_x( ) 

array_che_definisce_la_distanza_di_tutte_le_lamine = array_che_definisce_la_distanza_di_tutte_le_lamine + distanza #distanza delle lamine rispetto all'origine

distanza_ultima_lamina = array_che_definisce_la_distanza_di_tutte_le_lamine[ numero_lamine-1 ]

oro_array = np.array(z_oro)



"""DEFLESSIONE E SCHEMO SENSIBILE"""



posizione_x = []
posizione_y = []
posizione_z = []
posizione_lamina_finale = array_che_definisce_la_distanza_di_tutte_le_lamine[ numero_lamine-1 ]

zz , yy = funzioni.calcolo_coordinate_cartesiane_nota_x_e_angoli( posizione_lamina_finale , dimensione , angolo_phi , angolo_teta )
dimensione = len(yy)
#creazione valori dello schermo sensibile.

raggio_schermo , numero_divisioni_circonferenza , base_pixel , altezza_pixel , divisione_altezza , altezza_schermo = funzioni.creazione_schermo_sensibile_circolare( array_che_definisce_la_distanza_di_tutte_le_lamine , numero_lamine )

    
for i in range( 0 , dimensione , 1 ) :

    #atomo rispetto al quale avviene la deflessione per la particella i-esima
    numero_atomico = oro_array

    #deflessione particella i-esima
    angolo_deflesso = funzioni.angolo_deflessione( numero_lamine, energia_joule , numero_atomico )

    #print( angolo_deflesso , "\n" )

    
    # y0 , z0 saranno qui la posizione lungo y e z della particella sulla prima lamina e prima che avvenga l'interazione con quest'ultima.
    z0 = zz[i]
    y0 = yy[i]
    
    #print(f"\necco il valore di z0 nella funzione principale: {z0}")

    x , y , z = funzioni.ultima_interazione( posizione_lamina_finale , y0 ,  z0 , angolo_deflesso , numero_lamine , raggio_schermo, altezza_schermo )

    #print( x , y , z , "\n")
    
    maskx = ( np.abs(x) < raggio_schermo )
    masky = ( np.abs(y) < raggio_schermo )
    maskz = ( np.abs(z) < altezza_schermo/2 )

    #print(type(maskx), type(masky), type(maskz))

    
    masktot = bool(maskx) and bool(masky) and bool(maskz)

    if masktot == True :

        #salvo queste particelle

        posizione_x.append( x )
        posizione_y.append( y )
        posizione_z.append( z )

    else :

        pass


posizione_x = np.array( posizione_x )
posizione_y = np.array( posizione_y )
posizione_z = np.array( posizione_z )




dimensione = len(posizione_x)

#print(f"\nle coordinate delle particelle lungo x sono: { posizione_x }\nle coordinate delle particelle lungo y sono: { posizione_y }\nle coordinate delle particelle lungo z sono: { posizione_z } ")
print(f"\nil numero di particelle sopravvissute a fine esperimento è di: { dimensione }\n ")
"""RILEVAZIONE PARTICELLE"""

print( "ora verranno mostrate le particelle sullo schermo sensibile")

schermo = funzioni.rilevazione_particelle( posizione_x , posizione_y , posizione_z , raggio_schermo , numero_divisioni_circonferenza , altezza_pixel , divisione_altezza, array_che_definisce_la_distanza_di_tutte_le_lamine , distanza , raggio, numero_lamine )

schermo

