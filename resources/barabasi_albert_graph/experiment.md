# Barabási–Albert
![graph](barabasi_albert_graph_500_3.png)

## SIR, algorytm _fast_

Wyniki testów dla modelu SIR i algorytmu _fast_ dla różnych parametrów.   
Moim celem było znalezienie parametrów, które pozwolą na zarażnie jak największej ilości węzłów, 
 ale tak by jednocześnie było zarażonych jak najmniej

Domyślne ustawienia:  
`transmission_rate = 2.0`  
`recovery_rate = 1.0`  
![sir_fast_2-0_1-0](sir_fast_2-0_1-0.gif)

`transmission_rate = 0.5`  
`recovery_rate = 1.0`  
![sir_fast_0-5_1-0](sir_fast_0-5_1-0.gif)

`transmission_rate = 0.5`  
`recovery_rate = 2.0`  
![sir_fast_0-5_2-0](sir_fast_0-5_2-0.gif)  
**Najlepszy wynik**

`transmission_rate = 0.3`  
`recovery_rate = 0-8`  
![sir_fast_0-3_0-8](sir_fast_0-3_0-8.gif)

`transmission_rate = 0.2`  
`recovery_rate = 0-8`  
![sir_fast_0-2_0-8](sir_fast_0-2_0-8.gif)  
Również bardzo dobry wynik. Z powodu niższych wartości parametrów infekcja utrzymała się dłużej

## SIS, algorytm _fast_
Dla porównania wynik SIS (dla parametrów z ostatniego testu)
`transmission_rate = 0.2`  
`recovery_rate = 0-8`  
![sis_fast_0-2_0-8](sis_fast_0-2_0-8.gif)  
