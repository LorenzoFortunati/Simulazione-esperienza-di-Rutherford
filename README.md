# Simulazione dell’esperienza di Rutherford

Questo progetto implementa una simulazione numerica dell’esperienza di scattering di particelle alfa sul bersaglio d’oro, come nell’esperimento storico di Rutherford.

Utilizzando tecniche Monte Carlo, il programma modella il comportamento casuale delle particelle alfa durante la loro interazione con le lamine metalliche, tenendo conto dei processi fisici coinvolti nella diffusione coloumbiana.

La simulazione calcola e restituisce la distribuzione delle particelle rivelate su uno schermo sensibile di forma circolare che avvolge tutto l'apparato sperimentale, fornendo una rappresentazione grafica 3D della posizione finale delle particelle sullo schermo circolare.

---
## Semplificazioni e assunzioni fisiche

Per semplificare il modello fisico e rendere la simulazione più gestibile, sono state fatte le seguenti assunzioni e approssimazioni:

- L’angolo nel piano xy, cioè l’angolo azimutale, viene generato secondo una distribuzione gaussiana centrata in zero e con una deviazione ridotta, per tenere conto del fatto che nella realtà la maggior parte delle particelle non viene deflessa.

- La deflessione è considerata solo per l’angolo compreso tra l’asse z e il vettore posizione della particella, evitando di dover calcolare per ogni particella il piano esatto in cui si conserva il momento angolare. Questo semplifica notevolmente i calcoli.

- Per includere le deflessioni rare, cioè quelle intorno a 90° o 270°, nel codice è stato implementato un meccanismo che, dopo la deflessione con l’ultima lamina, con probabilità 1 su 100 genera l’angolo azimutale φ secondo una distribuzione gaussiana centrata su 90° o 270°.

Queste semplificazioni servono a mantenere il modello computazionalmente efficiente e a catturare qualitativamente il comportamento sperimentale, senza la complessità di un trattamento completo del momento angolare e della dinamica tridimensionale.



---
## Tecniche e librerie utilizzate

- **Metodi Monte Carlo** per la generazione statistica delle traiettorie delle particelle.  
- **Coordinate sferiche** per descrivere la posizione e la direzione delle particelle nello spazio.  
- **Visualizzazione grafica** tramite Matplotlib (2D e 3D).  
- Uso di librerie Python standard e di terze parti: `random`, `numpy`, `math`, `matplotlib` e `mpl_toolkits.mplot3d`.

---

## Requisiti di sistema e dipendenze

- Python 3.x  
- Librerie Python necessarie:

```bash
pip install numpy matplotlib
