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

def StageThree(count3,TOTAL_Stakes):
    # print("Stage 3")
    for i in range(p.Nn):
        for j in range(i + 1,p.Nn):
            if p.NODES[i].miner == False:
                break
            elif p.NODES[i].miner == True and p.NODES[j].miner == True:
                x = random.randint(0,1)
                y = random.randint(0,1)
                if x == 1 and y == 1: #0 - non-broadcast, 1 - broadcast
                    p.NODES[i].games_non_broadcast += 1
                    p.NODES[j].games_non_broadcast += 1
                elif x == 0 and y == 1:
                    p.NODES[j].games_non_broadcast = p.NODES[j].games_non_broadcast + 1
                    p.NODES[i].reputation = p.NODES[i].reputation - (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_non_broadcast/p.NODES[i].games_non_broadcast))
                    if len(list1) < 20:
                        list1.append((p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_non_broadcast/p.NODES[i].games_non_broadcast)))
                    p.NODES[i].count_non_broadcast = p.NODES[i].count_non_broadcast + 1
                    p.NODES[i].games_non_broadcast += 1
                    p.NODES[i].current_non_broadcast_strategy_game += 1
        
                elif x == 1 and y == 0:
                    p.NODES[j].games_non_broadcast = p.NODES[j].games_non_broadcast + 1
                    p.NODES[j].reputation = p.NODES[j].reputation - (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes) * (p.NODES[j].count_non_broadcast/p.NODES[j].games_non_broadcast))
                    if len(list1) < 20:
                        list1.append((p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes) * (p.NODES[j].count_non_broadcast/p.NODES[j].games_non_broadcast)))
                   
                    p.NODES[j].count_non_broadcast = p.NODES[j].count_non_broadcast + 1
                    p.NODES[i].games_non_broadcast += 1
                    p.NODES[j].current_non_broadcast_strategy_game += 1
                  
            
                else:
                    p.NODES[i].reputation = p.NODES[i].reputation - (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_non_broadcast/p.NODES[i].games_non_broadcast))
                    if len(list1) < 20:
                        list1.append((p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_non_broadcast/p.NODES[i].games_non_broadcast)))
                   
                    p.NODES[j].reputation = p.NODES[j].reputation - (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes) * (p.NODES[j].count_non_broadcast/p.NODES[j].games_non_broadcast))
                    if len(list1) < 20:    
                        list1.append((p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes) * (p.NODES[j].count_non_broadcast/p.NODES[j].games_non_broadcast)))
                    
                    p.NODES[i].count_non_broadcast = p.NODES[i].count_non_broadcast + 1
                    p.NODES[j].count_non_broadcast = p.NODES[j].count_non_broadcast + 1
                    p.NODES[i].games_non_broadcast += 1
                    p.NODES[j].games_non_broadcast += 1
                    p.NODES[i].current_non_broadcast_strategy_game += 1
                    p.NODES[j].current_non_broadcast_strategy_game += 1
               
    
    count5 = 0
    if count3 > 1:
        for i in range(p.Nn):
            if p.NODES[i].miner == True:
                if (p.NODES[i].current_non_broadcast_strategy_game / (count3 - 1)) > 0.4:
                    p.NODES[i].miner = False
                    p.NODES[i].delegated = False
                    if p.NODES[i].id not in p.malicious:
                        p.malicious.append(p.NODES[i].id)
            else:
                count5 = count5 + 1
            p.NODES[i].current_non_broadcast_strategy_game = 0
    
    if count5 > 2 and p.l != 3:
        p.l = p.l + 1
        StageTwo(count5,TOTAL_Stakes)

def StageTwo(count,TOTAL_Stakes):
    for i in range(p.Nn):
        for j in range(i + 1,p.Nn):
            if p.NODES[i].delegated == False:
                break
            
            elif p.NODES[i].delegated == True and p.NODES[j].delegated == True:
                x = random.randint(0,1)    
                y = random.randint(0,1)
        
                if x == 1: #valid
                    p.NODES[i].games_blocks += 1

                elif x == 0: #invalid
                    if len(list) < 10:
                        list.append((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks))
                
                    p.NODES[i].Stakes = p.NODES[i].Stakes - ((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks))
                    p.NODES[i].count_invalid = p.NODES[i].count_invalid + 1
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
            if p.NODES[i].delegated == True:
                if (p.NODES[i].current_block_invalid_game / (count - 1)) < 0.5:
                    p.NODES[i].miner = True
                    count3 = count3 + 1
                else:
                    if p.NODES[i].id not in p.malicious:
                        p.malicious.append(p.NODES[i].id)
            p.NODES[i].current_block_invalid_game = 0
        StageThree(count3,TOTAL_Stakes)
            
    elif count == 1:
        for i in range(p.Nn):
            if p.NODES[i].delegated == True:
                p.NODES[i].miner = True
                break 

def StageOne():
    count = 0
    max1 = -1
    min1 = 999
    for i in p.NODES:
        if i.Stakes > max1:
            max1 = i.Stakes
        if i.Stakes < min1 and i.Stakes >= 32:
            min1 = i.Stakes
    TOTAL_Stakes = sum([miner.Stakes for miner in p.NODES])
    X = max1 - min1/2
    for i in p.NODES:
        if i.Stakes >= min1 and i.Stakes <= X:
            i.delegated = True
            i.count_delegated += 1
            count = count + 1
    StageTwo(count,TOTAL_Stakes)        
    
def GameTheory():
    StageOne()    
    
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
            if i.miner == True:
                i.Stakes = i.Stakes + (i.count_delegated/i.game_rounds * i.Stakes) + ((1 - (i.count_delegated/i.game_rounds)) * i.Stakes)
                i.reputation = i.reputation + (i.count_delegated/i.game_rounds * i.reputation) + ((1 - (i.count_delegated/i.game_rounds)) * i.reputation)
            if i.delegated == True:
                i.delegated = False
                i.miner = False
            i.game_rounds += 1 
        while not Queue.isEmpty() and clock <= p.simTime:
            GameTheory()
            next_event = Queue.get_next_event()
            clock = next_event.time  # move clock to the time of the event
            BlockCommit.handle_event(next_event)
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
        print("Number of malicious nodes = ",len(p.malicious), "among",p.Nn,"Nodes")
        # for i in range(len(list1)):
        #     list1[i] *= 10 ** 20
        x = list[len(list)-1]
        y = list1[len(list1)-1]
        print("Payoff Matrix for Stage Two Game")
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
        for i, row in enumerate(payoff_matrix):
            print("{:<15} {:<15} {:<15}".format(rows[i], *row))
        
        print("Payoff Matrix for Stage Three Game")
     
        payoff_matrix = [
            ["0, 0", "0, " + "{:.4f}".format(-p.x)],
            ["{:.4f}".format(-p.x)+ ", 0" , "{:.4f}, {:.4f}".format(-p.x, -p.x)]
        ]

        # Print the header
        header = ["", "Broadcast", "Non Broadcast"]
        print("{:<15} {:<15} {:<15}".format(*header))


        # Print the rows of the matrix
        rows = ["Broadcast", "Non Broadcast"]
        for i, row in enumerate(payoff_matrix):
            print("{:<15} {:<15} {:<15}".format(rows[i], *row))
        print(list1)
        # print(list1)
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
