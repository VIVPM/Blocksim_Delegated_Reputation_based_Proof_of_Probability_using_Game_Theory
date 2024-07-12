from InputsConfig import InputsConfig as p
from Event import Event, Queue
from Scheduler import Scheduler
import random
import time
from math import factorial
from Statistics import Statistics

if p.model == 3:
    from Models.AppendableBlock.BlockCommit import BlockCommit
    from Models.Consensus import Consensus
    from Models.AppendableBlock.Transaction import FullTransaction as FT
    from Models.AppendableBlock.Node import Node
    from Models.Incentives import Incentives
    from Models.AppendableBlock.Statistics import Statistics
    from Models.AppendableBlock.Verification import Verification

elif p.model == 2:
    from Models.Ethereum.BlockCommit import BlockCommit
    from Models.Ethereum.Consensus import Consensus
    from Models.Ethereum.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Ethereum.Node import Node
    from Models.Ethereum.Incentives import Incentives

elif p.model == 1:
    from Models.Bitcoin.BlockCommit import BlockCommit
    from Models.Bitcoin.Consensus import Consensus
    from Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Bitcoin.Node import Node
    from Models.Incentives import Incentives

elif p.model == 0:
    from Models.BlockCommit import BlockCommit
    from Models.Consensus import Consensus
    from Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Node import Node
    from Models.Incentives import Incentives

########################################################## Start Simulation ##############################################################
count4 = 0
count5 = 0
list = []
list1 = []

def StageTwo(count3):
    #Every miner node plays the game with every other miner node. This stage game is used to filter the miner nodes who behave maliciously. These miner nodes will be eligible for mining process.
    for i in range(p.Nn):
        for j in range(i + 1,p.Nn):
            if p.NODES[i].miner == False:
                break
            #Assuming ((Stakes / Total Stakes) + (blocks generated / Total blocks)) = 0.4 
            elif p.NODES[i].miner == True and p.NODES[j].miner == True:
                x = random.randint(0,1)
                y = random.randint(0,1)
                if x == 0: #0 - non-broadcast, 1 - broadcast
                    #Penalty is imposed for miner node which behaves maliciously. Here the miner node uses non-broadcast strayegy and block is not broadcasted to the system.
                    p.NODES[i].reputation = p.NODES[i].reputation - (p.NODES[i].reputation * 0.4 * (p.NODES[i].count_non_broadcast/p.NODES[i].games_non_broadcast))
                    if len(list1) < 40:
                        list1.append((p.NODES[i].reputation * 0.4 * (p.NODES[i].count_non_broadcast/p.NODES[i].games_non_broadcast)))
                    # print(list1[len(list1)-1])
                    p.NODES[i].count_non_broadcast = p.NODES[i].count_non_broadcast + 1 #count the number of blocks that are not broadcasted.
                    p.NODES[i].games_non_broadcast += 1
                    p.NODES[i].current_non_broadcast_strategy_game += 1 
                if y == 0:
                    p.NODES[j].reputation = p.NODES[j].reputation - (p.NODES[j].reputation * 0.4 * (p.NODES[j].count_non_broadcast/p.NODES[j].games_non_broadcast))
                    if len(list1) < 40:
                        list1.append((p.NODES[j].reputation * 0.4 * (p.NODES[j].count_non_broadcast/p.NODES[j].games_non_broadcast)))
                    # print(list1[len(list1)-1])
                    p.NODES[j].count_non_broadcast = p.NODES[j].count_non_broadcast + 1
                    p.NODES[j].games_non_broadcast = p.NODES[j].games_non_broadcast + 1
                    p.NODES[j].current_non_broadcast_strategy_game += 1
                    
                if x == 1 and y == 1: 
                    p.NODES[i].games_non_broadcast += 1
                    p.NODES[j].games_non_broadcast += 1
                             
    
    count5 = 0
    if count3 > 1:
        for i in range(p.Nn):
            if p.NODES[i].miner == True:
                #After completing second stage game, the miner node is checked if the node behaved maliciously or not by find Malicious Broadcast ratio. If the ratio is 
                if (p.NODES[i].current_non_broadcast_strategy_game / (count3 - 1)) > 0.4:
                    #If the ratio is not within the threshold, then the miner node is removed from Miner node set.
                    p.NODES[i].miner = False
                    p.NODES[i].delegated = False
                    if p.NODES[i].id not in p.malicious:
                        p.malicious.append(p.NODES[i].id)
            else:
                count5 = count5 + 1 #count the eligible number of miner nodes
            p.NODES[i].current_non_broadcast_strategy_game = 0
    
    if count5 > 1 and p.l != 3: #To check if the number of eligible miner nodes are more than 1 and the number of times the two-stage game is played within three times. If either condition is not satisfied, then two-stage game is played again by eligible miner nodes.
        p.l = p.l + 1
        StageOne(count5)
    minimum = 999
    ind = -1
    if count5 == 0: #Number of eligible miner nodes are 0, then the miner node with highest reputation is selected as miner. The rewards is provided to that miner node. 
        for i in range(p.Nn):
            x = (p.NODES[i].count_invalid/p.NODES[i].games_blocks) + (p.NODES[i].count_non_broadcast/p.NODES[i].games_blocks)
            if x < minimum:
                minimum = x
                ind = i
        p.NODES[ind].Stakes += 25
        p.NODES[ind].reputation += 0.05

def StageOne(count):
    #Every delegated node plays the game with every other delegated node. This stage game is used to filter the delegated nodes who behave maliciously. These delegated nodes will be eligible for second stage game. 
    for i in range(p.Nn):
        for j in range(i + 1,p.Nn):
            if p.NODES[i].delegated == False: 
                break
            
            elif p.NODES[i].delegated == True and p.NODES[j].delegated == True:
                x = random.randint(0,1)    #For ith Delegated node
                y = random.randint(0,1)    #For jth Delegated node
        
                if x == 1: #valid
                    p.NODES[i].games_blocks += 1

                elif x == 0: #invalid
                    if len(list) < 10:
                        #Penalty is imposed for node which behaves maliciously. Here the delegated node used invalid block strayegy and block which is created is invalid
                        list.append((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks))
                
                    p.NODES[i].Stakes = p.NODES[i].Stakes - ((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks))
                    p.NODES[i].count_invalid = p.NODES[i].count_invalid + 1 #Number of invalid blocks are counted
                    p.NODES[i].current_block_invalid_game = p.NODES[i].current_block_invalid_game + 1 
                    p.NODES[i].games_blocks += 1
      
                if y == 1:
                    p.NODES[j].games_blocks += 1
                elif y == 0:
                    if len(list) < 10:
                        list.append((0.4 * p.NODES[j].Stakes) * (p.NODES[i].count_invalid/p.NODES[j].games_blocks))
                
                    p.NODES[j].Stakes = p.NODES[j].Stakes - ((0.4 * p.NODES[j].Stakes) * (p.NODES[j].count_invalid/p.NODES[j].games_blocks))
                    p.NODES[j].count_invalid = p.NODES[j].count_invalid + 1
                    p.NODES[j].current_block_invalid_game = p.NODES[j].current_block_invalid_game + 1
                    p.NODES[j].games_blocks += 1
     
        
    count3 = 0

    if count > 1:
        for i in range(p.Nn):
            if p.NODES[i].delegated == True: #After completing first stage game, the delegated node is checked if the node behaved maliciously or not by find Malicious Block ratio. 
                #If the ratio is within the threshold, then the delegated node is appended to Miner node set.
                if (p.NODES[i].current_block_invalid_game / (count - 1)) < 0.5:
                    p.NODES[i].miner = True
                    count3 = count3 + 1 #count number of miner nodes
                else:
                    if p.NODES[i].id not in p.malicious:
                        p.malicious.append(p.NODES[i].id) #Malicious nodes are appended to malicious set.
            p.NODES[i].current_block_invalid_game = 0
        StageTwo(count3)
            
    elif count == 1:
        for i in range(p.Nn):
            if p.NODES[i].delegated == True:
                p.NODES[i].miner = True
                break 

def DelegatedNodeInitialisation():
    count = 0 # count number of delegated nodes
    max1 = -1
    min1 = 999
    for i in p.NODES: 
        if i.Stakes > max1:
            max1 = i.Stakes #find maximum stakes in the network
        if i.Stakes < min1 and i.Stakes >= 32: 
            min1 = i.Stakes #find minimum stakes in the network in which number of stakes are more than 32.
    # TOTAL_Stakes = sum([miner.Stakes for miner in p.NODES])  #Calculate total stakes in the network
    X = max1 - min1/2 #use this formula to filter the nodes
    for i in p.NODES: 
        #if the nodes are within the given condition, these nodes are selected as delegated nodes
        if i.Stakes >= min1 and i.Stakes <= X:
            i.delegated = True 
            i.count_delegated += 1 #count all delegated nodes
            count = count + 1
    StageOne(count)        
    
def GameTheory():
    DelegatedNodeInitialisation()    #Delegated nodes are initialized in this function
    
def main():
    for i in range(p.Runs):
        clock = 0  # set clock to 0 at the start of the simulation
        if p.hasTrans:
            if p.Ttechnique == "Light":
                LT.create_transactions()  # generate pending transactions
            elif p.Ttechnique == "Full":
                FT.create_transactions()  # generate pending transactions
        start = time.time()
        Node.generate_gensis_block()  # generate the gensis block for all miners
        # initiate initial events >= 1 to start with
        GameTheory()
        BlockCommit.generate_initial_events()
        for i in p.NODES:
            if i.miner == True: #The eligible miner node is selected as miner and the rewards are provided to it.
                i.Stakes = i.Stakes + (i.count_delegated/i.game_rounds * i.Stakes) + ((1 - (i.count_delegated/i.game_rounds)) * i.Stakes)
                i.reputation = i.reputation + (i.count_delegated/i.game_rounds * i.reputation) + ((1 - (i.count_delegated/i.game_rounds)) * i.reputation)
            if i.delegated == True:
                i.delegated = False
                i.miner = False
            i.game_rounds += 1 #count number of games played by each node
        while not Queue.isEmpty() and clock <= p.simTime: #This loop is repeated until simulation time is met.
            GameTheory() 
            next_event = Queue.get_next_event()
            clock = next_event.time  # move clock to the time of the event
            BlockCommit.handle_event(next_event) #To create blocks
            Queue.remove_event(next_event) 
            for i in p.NODES:
                if i.miner == True:
                    i.Stakes = i.Stakes + (i.count_delegated/i.game_rounds * i.Stakes) + ((1 - (i.count_delegated/i.game_rounds)) * i.Stakes)
                    i.reputation = i.reputation + (i.count_delegated/i.game_rounds * i.reputation) + ((1 - (i.count_delegated/i.game_rounds)) * i.reputation)
                if i.delegated == True:
                    i.delegated = False
                    i.miner = False
                i.game_rounds += 1 
            print("Clock time right now = ",clock)
        end = time.time()
        print("The time of execution of playing games among nodes is :", (end-start)*10**3, "ms for" , p.Nn, "Nodes")
        list.sort()
        list1.sort()
        print("Number of malicious nodes = ",len(p.malicious), "among",p.Nn,"Nodes") #count number of malicious nodes
        # for i in range(len(list1)):
        #     list1[i] *= 10 ** 40
        x = list[len(list)-1]
        y = list1[11]
        print("Payoff Matrix for Stage First Game")
        # Define the matrix
        
        payoff_matrix = [
                ["0, 0", "0, " + "{:.2f}".format(-x)],
                ["{:.2f}".format(-x)+ ", 0" , "{:.2f}, {:.2f}".format(-x, -x)]
        ]

        # Print the header
        header = ["", "Valid Block", "Invalid Block"]
        print("{:<15} {:<15} {:<15}".format(*header))

        # Print the rows of the matrix
        rows = ["Valid Block", "Invalid Block"]
        # y = p.x
        for i, row in enumerate(payoff_matrix):
            print("{:<15} {:<15} {:<15}".format(rows[i], *row))
        
        print("Payoff Matrix for Stage Second Game")
     
        payoff_matrix = [
            ["0, 0", "0, " + "{:.4f}".format(-y)],
            ["{:.4f}".format(-y)+ ", 0" , "{:.4f}, {:.4f}".format(-y, -y)]
        ]

        # Print the header
        header = ["", "Broadcast", "Non Broadcast"]
        print("{:<15} {:<15} {:<15}".format(*header))
        
        print(list1)


        # Print the rows of the matrix
        rows = ["Broadcast", "Non Broadcast"]
        for i, row in enumerate(payoff_matrix):
            print("{:<15} {:<15} {:<15}".format(rows[i], *row))
        
        # for the AppendableBlock process transactions and
        # optionally verify the model implementation
        # print(list1)
        if p.model == 3:
            BlockCommit.process_gateway_transaction_pools()

            if i == 0 and p.VerifyImplemetation:
                Verification.perform_checks()

        Consensus.fork_resolution()  # apply the longest chain to resolve the forks
        # distribute the rewards between the particiapting nodes
        Incentives.distribute_rewards()
        # calculate the simulation results (e.g., block statstics and miners' rewards)
        Statistics.calculate()
        # print(list1)


        if p.model == 3:
            Statistics.print_to_excel(i, True)
            Statistics.reset()
        else:
            ########## reset all global variable before the next run #############
            Statistics.reset()  # reset all variables used to calculate the results
            Node.resetState()  # reset all the states (blockchains) for all nodes in the network
            fname = "(Allverify)1day_{0}M_{1}K.xlsx".format(
                p.Bsize/4000000, p.Tn/4000)
            # print all the simulation results in an excel file
            Statistics.print_to_excel(fname)
        fname = "(Allverify)1day_{0}M_{1}K.xlsx".format(
                p.Bsize/4000000, p.Tn/4000)
        # print all the simulation results in an excel file
        Statistics.print_to_excel(fname)
        Statistics.reset2()  # reset profit results


######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
