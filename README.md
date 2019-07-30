# GraphFlow
Projekt pozwala na symulacje przypływu w różnych typach sieci reprezentowanych jako grafy.
Obsługiwane typy sieci:
- sieci wodociągowe
- sieci epidemiczne

Głównym obszarem naszego zainteresowania były sieci epidemiczne. Poniżej znajudje sie opis różnych eksperymetów
 przeprowadzonych na tych sieciach.

## Przykład
Przykładaowe działanie programu dla grafu Tutte'a:
![tutte](resources/tutte_graph/tutte_graph_.png)

### Model SIR:
- algorytm _fast_:  
    parametry:
    - `transmission_rate = 2.0`
    - `recovery_rate = 1.0`
![tutte_sir_fast](resources/tutte_graph/sir_fast.gif)
- algorytm _discrete_:  
    parametry:
    - `transmission_probability = 0.7`
![tutte_sis_discrete](resources/tutte_graph/sir_discrete.gif)
### Model SIS:
- algorytm _fast_:  
    parametry:
    - `transmission_rate = 2.0`
    - `recovery_rate = 1.0`
![tutte_sis_fast](resources/tutte_graph/sis_fast.gif)
- algorytm _discrete_:  
    parametry:
    - `transmission_probability = 0.7`
![tutte_sis_discrete](resources/tutte_graph/sis_discrete.gif)

Algorytmy _fast_ sa dużo bardziej precyzyjne, więc będą częściej używane do eksperymetów. Algorytm _discrete_ dla 
 modelu SIS działa znacznie gorzej niż jego odpowiednik _fast_, nie będzie więc używany do testów.
 
## Eksperymenty:
