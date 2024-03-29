# GraphFlow
Projekt pozwala na symulacje przypływu w różnych typach sieci reprezentowanych jako grafy.
Obsługiwane typy sieci:
- sieci wodociągowe
- sieci epidemiczne

Głównym obszarem naszego zainteresowania były sieci epidemiczne. Poniżej znajduje sie opis różnych eksperymentów
 przeprowadzonych na tych sieciach.
 
## Instalacja
Projekt używa języka Python 3.7. Dodatkowo do eksportu danych w formacie mp4 potrzebna będzie biblioteka ImageMagick.
Po pobraniu projektu, w katalogu głównym wystarczy wywołać polecenie

```bash
pip3 install ./graph-flow
```
Pełne informacje dostępne są w [Wiki projektu](https://github.com/Fruktus/graphflow/wiki)

## Uruchomienie

```bash
python3 -m graphflow
```

Uruchomienie aplikacji bez dodatkowych parametrów wyświetli interfejs graficzny.
Można skorzystać z konsolowej pomocy poprzez komendę
```bash
python3 -m graphflow -h
```

Parametry można podać bezpośrednio z konsoli lub zapisać je w pliku, po jednym w każdej linii,
a następnie uruchomić program z jednym parametrem będącym ścieżką do tego pliku poprzedzoną znakiem @.
Przykład:
```bash
python3 -m graphflow @"./sample_config.txt"
```

Pełny opis dostępny jest w dokumentacji projektu.

## Przykład
Przykładowe działanie programu dla grafu Tutte'a:  
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
- [Barabasi Albert](resources/barabasi_albert_graph/experiment.md)  
![barabasi_albert](resources/barabasi_albert_graph/barabasi_albert_graph_500_3.png)
- [Circullar Ladder](resources/circular_ladder_graph/experiment.md)  
![circular_ladder](resources/circular_ladder_graph/circular_ladder_graph300.png)
- [Power Cluster](resources/power_cluster/experiment.md)  
![power_cluster](resources/power_cluster/powerlaw_cluster_graph_300_1_0-30.png)
- [Random Shell Graph](resources/shell/experiment.md)  
![random_shell](resources/shell/random_shell_graph_.png)
- [Lobster Graph](resources/lobster/experiment.md)  
![lobster](resources/lobster/random_lobster_300_0-80_0-80.png)  
- [Hoffman Singleton Graph](resources/hoffman/experiment.md)  
![hoffman](resources/hoffman/hoffman_singleton_graph_.png)  
- [Watts Strogatz Graph](resources/watts_strogatz/experiment.md)  
![watts_strogatz](resources/watts_strogatz/watts_strogatz_graph_300_4_0-20.png)
