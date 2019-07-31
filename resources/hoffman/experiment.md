# Hoffman Singleton Graph
![hoffman_singleton_graph](hoffman_singleton_graph_.png)

## SIR, algorytm _fast_
`transmission_rate = 0.5`  
`recovery_rate = 1.0`  
![sir_fast_0-5_1-0](sir_fast_0-5_1-0.gif)

`transmission_rate = 0.3`  
`recovery_rate = 1.0`  
![sir_fast_0-3_1-0](sir_fast_0-3_1-0.gif)

## SIS, algorytm _fast_
`transmission_rate = 0.3`  
`recovery_rate = 1.0`  
![sis_fast_0-3_1-0](sis_fast_0-5_1-0.gif)

## SIR, algorytm _discrete_
Korzystając z własności grafu Hoffmana (każdy wierzchołek jest stopnia 7) można tak ustalić prawdopodobieństwo zarażnia
 sąsiada (`transmission_probability`), aby w każdym kroku była zarażna średnio taka sama ich ilość.  
W tym przypadku w każdym kroku jest zarażanych średnio 2 sąsiadów

`transmission_probability = 0.30`  
![sir_discrete_0-30](sir_discrete_0-30.gif)
