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
                if x == 1 and y == 1: #1 - non-attack, 0 - attack
                    p.NODES[i].count_non_attack = p.NODES[i].count_non_attack + 1
                    p.NODES[j].count_non_attack = p.NODES[j].count_non_attack + 1
                    p.NODES[i].games_attack += 1
                    p.NODES[j].games_attack += 1
                elif x == 0 and y == 1:
                    p.NODES[j].count_non_attack = p.NODES[j].count_non_attack + 1
                    # if len(list1) < 400:
                        # if p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_attack/p.NODES[i].games_attack) > 0 and (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_attack/p.NODES[i].games_attack)) < 0.5:
                    p.NODES[i].reputation = p.NODES[i].reputation - (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes*10**19) * (p.NODES[i].count_attack/p.NODES[i].games_attack))
                    list1.append((p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes*10**19) * (p.NODES[i].count_attack/p.NODES[i].games_attack)))
                    # else:
                    #     p.NODES[i].reputation = p.NODES[i].reputation - (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_attack/p.NODES[i].games_attack))
                    p.NODES[i].count_attack = p.NODES[i].count_attack + 1
                    p.NODES[i].games_attack += 1
                    p.NODES[j].games_attack += 1
        
                elif x == 1 and y == 0:
                    p.NODES[i].count_non_attack = p.NODES[i].count_non_attack + 1
                    # if len(list1) < 400:
                        # if (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes) * (p.NODES[j].count_attack/p.NODES[j].games_attack)) > 0 and (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes) * (p.NODES[j].count_attack/p.NODES[j].games_attack)) < 0.2:
                    p.NODES[j].reputation = p.NODES[j].reputation - (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes*10**19) * (p.NODES[j].count_attack/p.NODES[j].games_attack))
                    list1.append((p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes*10**19) * (p.NODES[j].count_attack/p.NODES[j].games_attack)))
                    # else:
                    p.NODES[j].reputation = p.NODES[j].reputation - (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes*10**19) * (p.NODES[j].count_attack/p.NODES[j].games_attack))
                    p.NODES[j].count_attack = p.NODES[j].count_attack + 1
                    p.NODES[i].games_attack += 1
                    p.NODES[j].games_attack += 1
            
                else:
                    # if len(list1) < 400:
                        # if (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_attack/p.NODES[i].games_attack)) > 0 and (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes) * (p.NODES[i].count_attack/p.NODES[i].games_attack)) < 0.2:
                    p.NODES[i].reputation = p.NODES[i].reputation - (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes*10**19) * (p.NODES[i].count_attack/p.NODES[i].games_attack))
                    list1.append((p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes*10**19) * (p.NODES[i].count_attack/p.NODES[i].games_attack)))
                
                        # if (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes) * (p.NODES[j].count_attack/p.NODES[j].games_attack)) > 0 and (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes) * (p.NODES[j].count_attack/p.NODES[j].games_attack)) < 0.2:
                    p.NODES[j].reputation = p.NODES[j].reputation - (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes*10**19) * (p.NODES[j].count_attack/p.NODES[j].games_attack))
                    list1.append((p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes*10**19) * (p.NODES[j].count_attack/p.NODES[j].games_attack)))
                    # else:
                    p.NODES[i].reputation = p.NODES[i].reputation - (p.NODES[i].reputation * (p.NODES[i].Stakes/TOTAL_Stakes*10**19) * (p.NODES[i].count_attack/p.NODES[i].games_attack))
                    p.NODES[j].reputation = p.NODES[j].reputation - (p.NODES[j].reputation * (p.NODES[j].Stakes/TOTAL_Stakes*10**19) * (p.NODES[j].count_attack/p.NODES[j].games_attack))
                    p.NODES[i].count_attack = p.NODES[i].count_attack + 1
                    p.NODES[j].count_attack = p.NODES[j].count_attack + 1
                    p.NODES[i].games_attack += 1
                    p.NODES[j].games_attack += 1
               
    
    count5 = 0
    if count3 > 1:
        for i in range(p.Nn):
            if p.NODES[i].miner == True:
                if (p.NODES[i].count_attack / (count3 - 1)) > 0.4:
                    p.NODES[i].miner = False
                    if p.NODES[i].id not in p.malicious:
                        p.malicious.append(p.NODES[i].id)
            else:
                count5 = count5 + 1
            p.NODES[i].current_attack_strategy_game = 0
    # if len(p.l) > 2:
    #     return 
    if count5 > 2 and p.l != 2:
        p.l = p.l + 1
        StageThree(count5,p.TOTAL_Stakes)

def StageTwo(count):
    for i in range(p.Nn):
        for j in range(i + 1,p.Nn):
            if p.NODES[i].delegated == False:
                break
            
            elif p.NODES[i].delegated == True and p.NODES[j].delegated == True:
                x = random.randint(0,1)    
                y = random.randint(0,1)
        
                if x == 1: #valid
                    p.NODES[i].count_valid = p.NODES[i].count_valid + 1
                    p.NODES[i].games_blocks += 1

                elif x == 0: #invalid
                    if len(list) < 20:
                        # if ((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks)) > 5 and ((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks)) < 400:
                        p.NODES[i].Stakes = p.NODES[i].Stakes - ((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks))
                        list.append((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks))
                # else:
                #     p.NODES[i].Stakes = p.NODES[i].Stakes - ((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks))
                    else:
                        p.NODES[i].Stakes = p.NODES[i].Stakes - ((0.4 * p.NODES[i].Stakes) * (p.NODES[i].count_invalid/p.NODES[i].games_blocks))
                    p.NODES[i].count_invalid = p.NODES[i].count_invalid + 1
                    p.NODES[i].current_block_invalid_game = p.NODES[i].current_block_invalid_game + 1
                    p.NODES[i].games_blocks += 1
      
                if y == 1:
                    p.NODES[j].count_valid = p.NODES[j].count_valid + 1
                    p.NODES[j].games_blocks += 1
                elif y == 0:
                    if len(list) < 20:
                        # if ((0.4 * p.NODES[j].Stakes) * (p.NODES[i].count_invalid/p.NODES[j].games_blocks)) > 5 and ((0.4 * p.NODES[j].Stakes) * (p.NODES[i].count_invalid/p.NODES[j].games_blocks)) < 400:
                        p.NODES[j].Stakes = p.NODES[j].Stakes - ((0.4 * p.NODES[j].Stakes) * (p.NODES[j].count_invalid/p.NODES[j].games_blocks))
                        list.append((0.4 * p.NODES[j].Stakes) * (p.NODES[i].count_invalid/p.NODES[j].games_blocks))
                    else:
                        p.NODES[j].Stakes = p.NODES[j].Stakes - ((0.4 * p.NODES[j].Stakes) * (p.NODES[j].count_invalid/p.NODES[j].games_blocks))
                #     p.NODES[j].Stakes = p.NODES[j].Stakes - ((0.4 * p.NODES[j].Stakes) * (p.NODES[j].count_invalid/p.NODES[j].games_blocks))
                    p.NODES[j].count_invalid = p.NODES[j].count_invalid + 1
                    p.NODES[j].current_block_invalid_game = p.NODES[j].current_block_invalid_game + 1
                    p.NODES[j].games_blocks += 1
     
        
    count3 = 0
    # TOTAL_Stakes = sum([miner.Stakes for miner in p.NODES])
    # print("Total stakes = ",p.TOTAL_Stakes)
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
            
    elif count == 1:
        for i in range(p.Nn):
                p.NODES[i].miner = True
                break
    
    if count > 1:
        StageThree(count3,p.TOTAL_Stakes)

def StageOne():
    count = 0
    max1 = -1
    for i in p.NODES:
        if i.Stakes > max1:
            max1 = i.Stakes
    X = (32 + max1)/2
    for i in p.NODES:
        if i.Stakes >= 32 and i.Stakes <= X:
            i.delegated = True
            i.count_delegated += 1
            count = count + 1
    StageTwo(count)        
    
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
        BlockCommit.generate_initial_events()
        NoofRounds = 0
        while not Queue.isEmpty() and clock <= p.simTime:
            GameTheory()
            next_event = Queue.get_next_event()
            clock = next_event.time  # move clock to the time of the event
            BlockCommit.handle_event(next_event)
            Queue.remove_event(next_event)
            for i in p.NODES:
                if i.delegated == True:
                    i.delegated = False
                    i.miner = False
                # if i.miner == True:
                i.game_rounds += 1 
            NoofRounds += 1
            print("Round ",NoofRounds," completed")
            print("Clock time right now = ",clock)
        end = time.time()
        print("The time of execution of playing games among nodes is :", (end-start)*10**3, "ms for" , p.Nn, "Nodes")
        list.sort()
        list1.sort()
        print("Number of malicious nodes = ",len(p.malicious), "among",p.Nn,"Nodes")
        print(list)
        print(list1)
        x = list[len(list)-1]
        y = list1[len(list1)-1]
        # for i in range(len(list)):
        #     if list[i] > 15 and list[i] < 400:
        #         x = list[i]
        #         break
        print("Payoff Matrix for Stage Two Game")
        # Define the matrix
        # print(x)
        
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
            ["0, 0", "0, " + "{:.4f}".format(-y)],
            ["{:.4f}".format(-y)+ ", 0" , "{:.4f}, {:.4f}".format(-y, -y)]
        ]

        # Print the header
        header = ["", "Non Attack", "Attack"]
        print("{:<15} {:<15} {:<15}".format(*header))


        # Print the rows of the matrix
        rows = ["Non Attack", "Attack"]
        for i, row in enumerate(payoff_matrix):
            print("{:<15} {:<15} {:<15}".format(rows[i], *row))
        # for the AppendableBlock process transactions and
        # optionally verify the model implementation
        if p.model == 3:
            BlockCommit.process_gateway_transaction_pools()

            if i == 0 and p.VerifyImplemetation:
                Verification.perform_checks()

        Consensus.fork_resolution()  # apply the longest chain to resolve the forks
        # distribute the rewards between the particiapting nodes
        Incentives.distribute_rewards()
        # calculate the simulation results (e.g., block statstics and miners' rewards)
        Statistics.calculate()
        for i in range(p.Nn):
            print(p.NODES[i].Stakes,p.NODES[i].reputation)

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