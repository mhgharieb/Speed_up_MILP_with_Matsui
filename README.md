# Automatic-Cryptanalysis 
Codes for article "Speeding up MILP Aided Differential Characteristic Search with Mastui's Strategy".

To make the program run normally, CryptoMIP need to be imported. However, CryptoMIP is unable to be public for the sake of patent. To verify the correctness of results in our essay, you may use .lp documents.

All of the models presented in this paper are solved by the MILP optimizer Gurobi (version 7.0.2) running at 16 threads on a server with Intel Xeon E5-2637V3 CPU 3.50GHz.

## PRESENT
MILP Model 1~8 for present. The time for Model 7 and Model 8 is obvious less than Model 1. New models are really effective for present.

## SIMON
MILP Model 1~8 for SIMON32, SIMON48 and SIMON64. However, only SIMON32 and SIMON48 could get optimal results in a limited time. And the time for Model 7 and Model 8 is less than Model 1, which is the original MILP based model.

## SPECK
MILP Model 1~8 for SPECK32 and SPECK64. New models are useless for SPECK.

## Speeding up MILP Aided Differential Characteristic Search with Mastui's Strategy
The article accepted by ISC2018.
