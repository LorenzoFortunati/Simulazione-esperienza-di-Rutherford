# Simulazione dell’esperienza di Rutherford

Questo progetto implementa una simulazione numerica dell’esperienza di scattering di particelle alfa su una o più lamine, come nell’esperimento storico di Rutherford.
Tali lamine saranno composte da una percentuale di oro o argento(o una lega delle due) in misura voluta dall'utente stesso.

Utilizzando tecniche Monte Carlo, il programma modella il comportamento casuale delle particelle alfa durante la loro interazione con le lamine metalliche, tenendo conto dei processi fisici coinvolti nella diffusione coloumbiana.

La simulazione calcola e restituisce la distribuzione delle particelle rivelate su uno schermo sensibile di forma circolare che avvolge tutto l'apparato sperimentale, fornendo una rappresentazione grafica 3D della posizione finale delle particelle sullo schermo circolare.

---
## Semplificazioni e Assunzioni Fisiche

Per mantenere la simulazione computazionalmente efficiente e al contempo fisicamente significativa, sono state adottate alcune semplificazioni fondamentali:

- **Lamine come piani bidimensionali:**  
  Ogni lamina è modellata come un piano geometrico privo di spessore. Questo implica che **ogni particella interagisce al massimo una sola volta per lamina**, subendo una deflessione netta per ciascun passaggio. L'effetto del multi-scattering è quindi descritto come l'accumulo delle deflessioni provenienti da lamine distinte, anziché da collisioni multiple all'interno di una singola lamina.

- **Singola interazione per lamina:**  
  Non viene simulata l'interazione con molteplici nuclei all'interno della stessa lamina. Si assume che, qualora avvenga una deviazione, essa sia rappresentativa dell'interazione dominante e sufficiente a descrivere la traiettoria complessiva.

- **Campionamento corretto del parametro d'impatto \( b \):**  
  Il parametro d'impatto, ovvero la distanza minima tra la traiettoria della particella e il centro del nucleo bersaglio, è stato **campionato in modo da garantire una distribuzione uniforme in area**, coerente con la fisica dello scattering.  
  La formula adottata è:
  
  ```python
  u = np.random.uniform(0, 1)
  b = np.sqrt(u * (b_max**2 - b_min**2) + b_min**2)


---
## Tecniche e librerie utilizzate

- **Metodi Monte Carlo** per la generazione statistica delle traiettorie delle particelle.  
- **Coordinate sferiche** per descrivere la posizione e la direzione delle particelle nello spazio.  
- **Visualizzazione grafica** tramite Matplotlib (2D e 3D).  
- Uso di librerie Python standard e di terze parti: `random`, `numpy`, `math`, `matplotlib` e `mpl_toolkits.mplot3d`.

---
## Spiegazione dei codici presenti

Nella cartella **progetti_python** sono contenuti diversi script organizzati in due sezioni principali:

- **Caso generale:** codice flessibile che consente all’utente di configurare liberamente parametri come il numero di lamine, la distanza delle lamine dalla sorgente e la loro composizione.  
- **Esempi simulazione:** simulazioni preimpostate dove molti parametri, come il numero e la posizione delle lamine, sono definiti di default per facilitare l’utilizzo e l’esecuzione rapida.  


## Requisiti di sistema e dipendenze

- Python 3.x  
- Librerie Python necessarie:

```bash
pip install numpy matplotlib


