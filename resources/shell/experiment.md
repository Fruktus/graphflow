# Radnom Shell Graph
![random_shell_graph_](random_shell_graph_.png)

## SIR algorytm _fast_

Zmniejszałem parametr `transmission_rate` aż do momentu gdy zostały jakieś niezarażone węzły po wygaśnięciu infekcji

`transmission_rate = 1.0`  
`recovery_rate = 1.0`  
![sir_fast_1-0_1-0](sir_fast_1-0_1-0.gif)

`transmission_rate = 1.0`  
`recovery_rate = 0.8`  
![sir_fast_0-8_1-0](sir_fast_0-8_1-0.gif)

`transmission_rate = 1.0`  
`recovery_rate = 0.5`  
![sir_fast_0-5_1-0](sir_fast_0-5_1-0.gif)

Można zaobserwować bardzo szybkie zarażanie dużych zbiorowisk węzłów, po tym jak jeden z nich zostanie zainfekowany. 
Choroba dużo trudniej przenosi się na sąsiednie grupy.

## SIS, algorytm _fast_

Podobny eksperyment dla SIS

`transmission_rate = 1.0`  
`recovery_rate = 0.5`  
![sis_fast_0-5_1-0](sis_fast_0-5_1-0.gif)

## SIR, algorytm _discrete_

I dla algorytmu dyskretnego

`transmission_probability = 0.35`  
![sir_discrete_0-35](sir_discrete_0-35.gif)