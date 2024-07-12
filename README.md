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

## Delegated Reputation-based Proof of Probability using Game Theory (DRPoP-GT)

## Overview

This project focuses on applying game theory to blockchain technology. The goal is to analyze and optimize the behavior and interactions of various participants within the blockchain ecosystem. By modeling actions of miners, validators, and other stakeholders as strategic games, we incentivize honest behavior and deter malicious activities. This ensures consensus, security, and efficiency in blockchain operations, particularly in Proof of Stake and Proof of Work systems. The DRPoP-GT consensus algorithm is evaluated using performance metrics across various scenarios and experimental parameters.

## Implementation Details

### Main.py

The `Main.py` file handles the initial filtering of nodes based on stakes. Eligible nodes are selected as delegated nodes, which then participate in a two-stage game:

1. **First-Stage Game**
2. **Second-Stage Game**

The results of the first-stage game are utilized in the second-stage game. After completing the two-stage game, an eligible node is selected as the miner and receives rewards. A penalty is imposed at each stage if a node behaves maliciously. Detailed comments are provided in the `Main.py` file.

### Models/Ethereum

DRPoP-GT operates within the Ethereum Blockchain. The code for setting transactions, blocks, and nodes can be found in the `Models/Ethereum` folder. The model is specified as model 2 in the `InputsConfig.py` file.

## Statistics and Results

Simulation results are printed in an Excel file at the end of the simulation. The Excel sheets, generated from the `Statistics.py` file, include:

- Blockchain ledger
- Number of blocks mined
- Number of stale (uncle) blocks
- Rewards gained by each miner

Results are stored in the `results` folder, which contains three subfolders:

1. **Nodes**: Shows the number of nodes used in the simulation.
2. **Simulation**: Shows the varying simulation times used in the simulation.
3. **Transactions**: Shows the number of transactions completed in the simulation.

All results are tabulated in Excel sheets, varying parameters across nodes, transactions, and simulation time.

### drpopgt_images Folder

The `drpopgt_images` folder contains images of the results, including:

- Computational overhead
- Number of malicious nodes
- Payoff matrix for both stage games

This folder has three subfolders:

1. **Load** (varies from 10000 to 50000)
2. **Nodes** (varies from 1000 to 5000)
3. **Simulation** (varies from 60 minutes to 300 minutes)

### REU.ipynb

The `REU.ipynb` file provides calculations regarding transaction time, block creation time, computational overhead, number of malicious nodes, and fairness. Import the Excel sheets from the `results` folder and run all cells to get the final output. Graphs are plotted using Matplotlib to analyze the DRPoP-GT consensus algorithm compared to existing algorithms.

## Usage

1. Run `Main.py` to perform the simulation.
2. Check the `results` folder for Excel files containing the simulation data.
3. Use the `REU.ipynb` notebook for further analysis and visualization.
