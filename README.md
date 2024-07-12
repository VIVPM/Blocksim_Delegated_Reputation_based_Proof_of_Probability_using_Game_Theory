# BlockSim Simultor

## What is BlockSim Simulator?
**BlockSim** is an open source blockchain simulator, capturing network, consensus and incentives layers of blockchain systems. BlockSim aims to provide simulation constructs that are intuitive, hide unnecessary detail and can be easily manipulated to be applied to a large set of blockchains design and deployment questions (related to performance, reliability, security or other properties of interest). At the core of BlockSim is a Base Model, which contains a number of functional blocks (e.g., blocks, transactions and nodes) common across blockchains, that can be extended and configured as suited for the system and study of interest. BlockSim is implemented in **Python**.

## Installation and Requirements

Before you can use BlockSim  simulator, you need to have **Python version 3 or above** installed in your machine as well as have the following packages installed:

- pandas 
>pip install pandas
- numpy 
>pip install numpy
- sklearn 
>pip install sklearn
- xlsxwriter
>pip install xlsxwriter

## Running the simulator

Before you run the simulator, you can access the configuration file *InputsConfig.py* to choose the model of interest (Base Model 0, Bitcoin Model 1 and Ethereum Model 2) and to set up the related parameters.
The parameters include the number of nodes (and their fraction of hash power), the block interval time, the block propagation delays, the block and transaction sizes, the block rewards, the tranaction fees etc.
Each model has a slightly different (or additional) parameters to capture it.

To run the simulator, one needs to trigger the main class *Main.py* either from the command line
> python Main.py

or using any Python editor such as Spyder.

## Game theory in Blockchain
Game theory in blockchain involves applying mathematical models to analyze and optimize the behavior and interactions of various participants within the blockchain ecosystem. It focuses on incentivizing honest behavior and deterring malicious activities by modeling the actions of miners, validators, and other stakeholders as strategic games. By designing protocols that align individual incentives with the overall network's health, game theory helps ensure consensus, security, and efficiency in blockchain operations. This approach is particularly crucial in Proof of Stake and Proof of Work systems, where the goal is to maintain a decentralized, robust, and scalable network. My design is focused on creating game theoretic model for stake based consensus algorithm which is known as "Delegated Reputation based Proof of Probability using Game Theory" (DRPoP-GT) and it is evaluated using performance metrics across various scenarios and experimental parameters.

In Main.py file, Initially the nodes are filtered based on stakes, the eligible nodes will be selected as Delegated nodes and these nodes will play two-satge game. In the two-stage game, there are two stages: first stage game and second stage game. Both stage games have separate functions. Furthermore, DRPoP-GT will be running in Ethereum Blockchain. The code for setting transactions, blocks, nodes can be found in Models/Ethereum folder. Since the model is Ethereum, model is chosen as 2 in InputsConfig.py. In this algorithm, the results of first stage game is utilized in the second stage game. After completion of two-stage game, the eligible node is selected as miner and it receives the rewards. In every stage, there will be a penalty imposed after node behaves malicious in any stage in the game. The comments are written in Main.py file.

## Statistics and Results

The results of the simulator is printed in an excel file at the end of the simulation. The results include the blockchain ledger, number of blocks mined, number of stale (uncles) blocks and the rewards gained by each miner etc. The results can be found in results folder. There are three folders: Nodes, Simulation, Transactions. 
The Nodes folder shows the number of nodes used in simulation.
The Simulation folder shows the varying simulation time used in simulation.
The Transaction folder shows the number of transactions completed in simulation.
All the results are tabulated in Excel sheets varying parameters across nodes, transactions and simulation time.
The drpopgt images folder show all the results in images which include computational time, number of malicious nodes, payoff matrix for both stage games.
In this folder, there are three folders: load, nodes, simulation.
The nodes vary from 1000 to 5000. The transactions vary from 10000 to 50000. The simulation vary from 60 minutes to 300 minutes.
