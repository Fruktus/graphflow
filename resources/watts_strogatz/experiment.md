# Watts-Strogatz Graph
![watts_strogatz_graph_300_4_0-20](watts_strogatz_graph_300_4_0-20.png)

## SIR, algorytm _fast_
`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![sir_fast_2-0_1-0](sir_fast_2-0_1-0.gif)

Infekcja się nie rozprzestrzenia, za mało połączeń z zainfekowanymi

`transmission_rate = 2.5`  
`recovery_rate = 1.0`  
![sir_fast_2-5_1-0](sir_fast_2-5_1-0.gif)

Po zwiększeniu `trasmission_rate` infekcja dochodzi do węzłów o dużym stopniu, następuje gwałtowny wzrost ilości
 zarażonych. Prawie cała sieć zotaje zainfekowana

## SIS, algorytm _fast_
`tranmission_rate = 2.5`  
`recovery_rate = 1.0`  
![sis_fast_2-5_1-0](sis_fast_2-5_1-0.gif)

## SIR, algorytm _discrete_
`transmission_probability = 0.5`  
![sir_discrete_0-5](sir_discrete_0-5.gif)

# Większy graf
![watts_strogatz_graph_1000_4_0-10](watts_strogatz_graph_1000_4_0-10.png)

Podobne eksperymenty wykonane dla grafu tego samego typu z większą ilością węzłów (1000)

## SIR, algorytm _fast_
`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![big_sir_fast_2-0_1-0](big_sir_fast_2-0_1-0.gif)

`transmission_rate = 2.5`  
`recovery_rate = 1.0`  
![big_sir_fast_2-5_1-0](big_sir_fast_2-5_1-0.gif)

## SIS, algorytm _fast_
`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![big_sis_fast_2-0_1-0](big_sis_fast_2-0_1-0.gif)

## SIR, algorytm _discrete_
`transmission_probability = 0.5`  
![big_sir_discrete_0-5](big_sir_discrete_0-5.gif)

Infekcja zachowuje się podobnie jak w mniejszej sieci
