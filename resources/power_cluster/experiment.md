# Powerlaw Cluster
![powerlaw_cluster_graph_300_1_0-30](powerlaw_cluster_graph_300_1_0-30.png)

## SIR, algorytm _fast_
Test dla bardzo niskiego parametru `recovery_rate`
`transmission_rate = 2.0`  
`recovery_rate = 0.2`  
![sir_fast_2-0_0-2](sir_fast_2-0_0-2.gif)

Infekcja zaczyna rozprzestrzeniać się szybko dopiero po zarażeniu jednego z centralnych wirzchołków

Dla znacznie wyższego `recovery_rate`

`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![sir_fast_2-0_0-2](sir_fast_2-0_1-0(1).gif)

`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![sir_fast_2-0_0-2](sir_fast_2-0_1-0(2).gif)

Powyższe dwa zostały wykonane dla dokładnie tego samego zestawu parametrów. Ilość jaką węzłów jaką infekcaja
 jest w stanie zarazić przed wygaśnięciem zależy od tego jak szbko zainfekuje centralny węzeł.

## SIS, algorytm _fast_
`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![sis_fast_2-0_1-0](sis_fast_2-0_1-0.gif)
 
# Większy graf
![powerlaw_cluster_graph_800_1_0-10](powerlaw_cluster_graph_800_1_0-10.png)

Podobne eksperymenty wykonane dla grafu tego samego typu z większą ilością węzłów (800)

## SIR, algorytm _fast_
`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![big_sir_fast_2-0_1-0](big_sir_fast_2-0_1-0.gif)

## SIS, algorytm _fast_
`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![big_sis_fast_2-0_1-0](big_sis_fast_2-0_1-0.gif)

Wnioski podobne jak dla grafu mniejszego