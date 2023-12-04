#! /usr/bin/python

from ast import arg
from symbol import arglist
import sys
import json
 


# arguments:
# INPUT: PROGRAMM_NAME ARGUMENTATION_FRAMEEWORK
# i.e.: main.py example-argumentation-framework.json
if len(sys.argv) >= 2:  #CGHECK THIUS PART*******
    json_file = sys.argv[1]
    if len(sys.argv) >= 3:  #CGHECK THIUS PART*******
        claim_argument = sys.argv[2]
else:
    json_file = "1_work_life_balance.json"

print("FILE: ", json_file)  #********

    # LOADING JSON FILE
 
# Opening JSON file
file = open(json_file)

data = json.load(file)

    # BUILDING ARGUMENT MAP

argument_map = {}
for argument in data['Arguments']:
    #argument_map[argument]= [[attacking],[attacked by]]
    argument_map[argument]= [[],[]]
    for attack in data['Attack Relations']:
        if attack[0] == argument:
            #If the argument is an attacker (attack[0]), add the argument it attacks to the list
            argument_map[argument][0].append(attack[1])
        if attack[1] == argument:
            #If the argument is being attacked by another argumen (attack[1]), note this agression
            argument_map[argument][1].append(attack[0])

print()
print('argument_map')
print(argument_map)

if claim_argument not in argument_map:
    print()
    print("WARNING:")
    print("Faild to locate suggested argument in the argument map")

print()
print('These arguments have no attaackers (are free argumeents):')
for argument in argument_map:
    if bool(argument_map[argument][1]) == False:    #Then the list of atttacking nodes is empty, the boolean will result in False
        print(argument)


    # LABELLING

#LABELS / TAGS
    #Undefined, In, Out
undef_ = 'Undefined'
in_ = 'In'
out_ = 'Out'

# Tag all nodes as Undefined
argument_labelling = {}
for argument in argument_map:
    argument_labelling[argument] = undef_
print()
print("Initial argument_labelling")
print(argument_labelling)

    #This should not be needed, as the 'Skeptical' label assignment that follows should also handle it. Just here for notes
#If there are nodes that are not attacked by any other, assigned as In / True
for argument in argument_map:
    if bool(argument_map[argument][1]) == False:    #Then the list of atttacking nodes is empty, the boolean will result in False
        argument_labelling[argument] = in_

def proposed_argument_labelling(argument_map, argument_labelling_, unchageable_arguments_=[]):
    argument_labelling=argument_labelling_.copy()
    unchageable_arguments=unchageable_arguments_
    passing=False
    change = True
    while change:
        change = False
        for argument in argument_map:
            parents_labels=[]
            for parent in argument_map[argument][1]:
                parents_labels.append(argument_labelling[parent])
        #IMPORTANT NOTE: #Diferent from normal skeptical argument labelling #Prevents the assumed arguments to be re-labelled (and possibly go into loop)
            if in_ in parents_labels:   #Label node Out
                prev_label = argument_labelling[argument]
                if prev_label != out_: # If the label has changed, replace it and note the change
                    if argument in unchageable_arguments:     # If the argument is in the list of arguments we have opted to try (unchageable_arguments_)
                        print('argument ', argument, ' found in unchangeable - OUT')
                        if argument_labelling_[argument] != out_:   # If the attepmted labelling is different from that from which we would be assigning now (out)
                            print('Proposition failed, returning to previous model')
                            return argument_labelling_, passing  #Then it means this cannot hold, we would be in a loop, so we return the prvious dictionary
                    argument_labelling[argument]=out_
                    change = True
            # We can assume here that there was no parent In
            elif undef_ in parents_labels:  #***This might not be needed, because we label all arguments Undefined to begin with
                prev_label = argument_labelling[argument]
                if prev_label != undef_: # If the label has changed, replace it and note the change
                    if argument in unchageable_arguments:     # If the argument is in the list of arguments we have opted to try (unchageable_arguments_)
                        print('argument ', argument, ' found in unchangeable - UNDEF')
                        if argument_labelling_[argument] != undef_:   # If the attepmted labelling is different from that from which we would be assigning now (undef_)
                            print('Proposition failed, returning to previous model')
                            return argument_labelling_, passing  #Then it means this cannot hold, we would be in a loop, so we return the prvious dictionary
                    argument_labelling[argument]=undef_   #***CHECK LABEL*****
                    change = True
            # Here we can assume that the parent list does not contain In or Undefined, meaning only Out or not parents / attackers
            #CHECK***** I might not need initial is_there_anchor label assignment***********
            else:
                if argument in unchageable_arguments:     # If the argument is in the list of arguments we have opted to try (unchageable_arguments_)
                        print('argument ', argument, ' found in unchangeable - IN')
                        if argument_labelling_[argument] != in_:   # If the attepmted labelling is different from that from which we would be assigning now (in_)
                            print('Proposition failed, returning to previous model')
                            return argument_labelling_, passing  #Then it means this cannot hold, we would be in a loop, so we return the prvious dictionary
                prev_label = argument_labelling[argument]
                if prev_label != in_: # If the label has changed, replace it and note the change
                    argument_labelling[argument]=in_
                    change = True

        passing=True
        return argument_labelling, passing





grounded = False

    # WIth no unchageable_arguments_, resultts in skepticall Labelling
argument_labelling, passing = proposed_argument_labelling(argument_map, argument_labelling)
print()
print('skeptical argument_labelling')
print(argument_labelling)

if claim_argument in argument_map:
    if argument_labelling[claim_argument] == in_:
        grounded = True






#This loops through the different cyclical argument chains, until all have been resolved
#NOTE: to improve, different attempts in every chain should be recorded, to minimize uncertainty
if undef_ in list(argument_labelling.values()):
    print()
    print("Attempting mapping to decrease undefined nodes")
    print()

    #simple attempt ******
    proposed_argument_labels = argument_labelling.copy()    #creates a copy of argument_labelling to edit, keeps the old for comparing and creating other ones ***needs to implement***
    prev__argument_labels = argument_labelling.copy()
    proposed_in = None
    proposed_out = None
    change = True
    unchageable_arguments = []

    #Is this needed?********** SHould uit be handeled as normal****
    """
    #Arguments that attack themselves must always be undef_
    for argument in argument_map:
        if argument in argument_map[argument][0]:   #If the argument attacks itself
            unchageable_arguments.append(argument)  #Thus should not be changed
    """
    
    while change==True:
        change = False
        for argument in argument_map:
            #print("argument: ", argument, proposed_argument_labels[argument])  #********
            if (proposed_argument_labels[argument] == undef_):   #If the node is labeled as undefined
                for parent in argument_map[argument][1]:
                    if (proposed_argument_labels[parent] == undef_) and (parent != argument): #If the parent node is labeled as undefined, and the parent node is not the original node (no self attacking argument)
                        print("argument: ", argument, proposed_argument_labels[argument])
                        proposed_in = argument  #***not in use?*****
                        proposed_out = parent  #***not in use?*****
                        proposed_argument_labels[argument] = in_
                        unchageable_arguments.append(argument)
                        print("proposed IN: ",argument)
                        proposed_argument_labels[parent] = out_
                        unchageable_arguments.append(parent)
                        print("proposed OUT: ",parent)
                        break
                    #print("PASS 1") #This does NOT run
                    break
                #print("PASS 2") #This runs
                break
            #print("PASS 3") #This runs
            #break
        
        #print("THis STILL RUNS")
        print()        
        new_proposed_argument_labels, passing = proposed_argument_labelling(argument_map, proposed_argument_labels, unchageable_arguments)
        if passing == False:    #The proposed assumtion did not work********
            proposed_argument_labels = prev__argument_labels.copy()    #If if failed, we default the proposed to the previous labelling, as it is no longer proposed
        # If the previous statemnt is true (new_proposed_argument_labels did not pass), the following if statement will not hold
        if (passing == True) and (new_proposed_argument_labels != prev__argument_labels):   #The new_proposed_argument_labels, which passed the test, is different from prev__argument_labels, and thus an extention***
            proposed_argument_labels = new_proposed_argument_labels.copy()  #We update the proposed to match the new mapping
            prev__argument_labels = new_proposed_argument_labels.copy()     #And also the prev__argument_labels, as we will use it to default to it if proposed_argument_labels fails the labelling in the future
            change=True
            print("CHANGE IS PROPOSED")

print("Proposed argument label")
print(proposed_argument_labels)

#*****SHOULD PRINT TRUE-FALSE-TRUE WHich is wrong***

















def admissibility(argument_map, argument_labelling, claim_argument_):
    #This loops through the different cyclical argument chains, until all have been resolved
    #NOTE: to improve, different attempts in every chain should be recorded, to minimize uncertainty

    #simple attempt ******
    proposed_argument_labels = argument_labelling.copy()    #creates a copy of argument_labelling to edit, keeps the old for comparing and creating other ones ***needs to implement***
    prev__argument_labels = argument_labelling.copy()
    proposed_in = None
    proposed_out = None
    change = True
    unchageable_arguments = []

    unchageable_arguments.append(claim_argument_)
    proposed_argument_labels[claim_argument_] = in_ # Attemptong in_ assumption
    for parent in argument_map[claim_argument_][1]: #Make all attackers out_ to sustain the in_
        proposed_argument_labels[parent] = out_ #This is required by definition of in_
        unchageable_arguments.append(parent)
    for child in argument_map[claim_argument_][0]: #Make all attacked arguments out_ to sustain the in_
        proposed_argument_labels[child] = out_ #This is required by definition of in_
        unchageable_arguments.append(child)
    
    print("HEREEEEEE: ", proposed_argument_labels)
    new_proposed_argument_labels, passing = proposed_argument_labelling(argument_map, proposed_argument_labels, unchageable_arguments)

    if passing == False:    #The proposed assumtion did not work********
            print("Initial admissiblility test has been Failed")
            return argument_labelling, False
    # If the previous statemnt is true (new_proposed_argument_labels did not pass), the following if statement will not hold
    if (passing == True) and (new_proposed_argument_labels != prev__argument_labels):   #The new_proposed_argument_labels, which passed the test, is different from prev__argument_labels, and thus an extention***
        proposed_argument_labels = new_proposed_argument_labels.copy()  #We update the proposed to match the new mapping
        prev__argument_labels = new_proposed_argument_labels.copy()     #And also the prev__argument_labels, as we will use it to default to it if proposed_argument_labels fails the labelling in the future
        change=True
        print("Initial admissiblility test has been passed")

    while change==True:
        change = False
        for argument in argument_map:
            #print("argument: ", argument, proposed_argument_labels[argument])  #********
            if (proposed_argument_labels[argument] == undef_):   #If the node is labeled as undefined
                for parent in argument_map[argument][1]:
                    if (proposed_argument_labels[parent] == undef_) and (parent != argument): #If the parent node is labeled as undefined, and the parent node is not the original node (no self attacking argument)
                        print("argument: ", argument, proposed_argument_labels[argument])
                        proposed_in = argument  #***not in use?*****
                        proposed_out = parent  #***not in use?*****
                        proposed_argument_labels[argument] = in_
                        unchageable_arguments.append(argument)
                        print("proposed IN: ",argument)
                        proposed_argument_labels[parent] = out_
                        unchageable_arguments.append(parent)
                        print("proposed OUT: ",parent)
                        break
                    #print("PASS 1") #This does NOT run
                    break
                #print("PASS 2") #This runs
                break
            #print("PASS 3") #This runs
            #break
        
        #print("THis STILL RUNS")
        print()        
        new_proposed_argument_labels, passing = proposed_argument_labelling(argument_map, proposed_argument_labels, unchageable_arguments)
        if passing == False:    #The proposed assumtion did not work********
            proposed_argument_labels = prev__argument_labels.copy()    #If if failed, we default the proposed to the previous labelling, as it is no longer proposed
        # If the previous statemnt is true (new_proposed_argument_labels did not pass), the following if statement will not hold
        if (passing == True) and (new_proposed_argument_labels != prev__argument_labels):   #The new_proposed_argument_labels, which passed the test, is different from prev__argument_labels, and thus an extention***
            proposed_argument_labels = new_proposed_argument_labels.copy()  #We update the proposed to match the new mapping
            prev__argument_labels = new_proposed_argument_labels.copy()     #And also the prev__argument_labels, as we will use it to default to it if proposed_argument_labels fails the labelling in the future
            change=True
            print("CHANGE IS PROPOSED")

    if argument_labelling != proposed_argument_labels:  #Meaening the accepted proposed labelling has changed, and approved of the claim_argument as in_
        return proposed_argument_labels, True
    else:
        return proposed_argument_labels, False



































#Prefered Semantics
    #Arguments that do not attack each other    #Working on it***********
"""
self_attacking_arguments = []
for argument in argument_map:
    if argument in argument_map[argument][0]:
        self_attacking_arguments.append(argument)
print("Self attacking arguments: ", self_attacking_arguments)

pref=[]

for argument in argument_map:    
    arg_compativility = []
    for second_argument in argument_map:  
        if (argument != second_argument) and (second_argument not in argument_map[argument][0]) and (second_argument not in argument_map[argument][1]):    #If second argument is not the same argument, and it is not in the list of arguments attacked by argument or attacking argument 
            if second_argument in self_attacking_arguments: #The argument attacks itself
                pass
            else:
                arg_compativility.append(second_argument)
    if bool(arg_compativility) == True: #If the list is not empty
        print("compatible arguments")
        arg_compativility.append(argument)
        pref.append(arg_compativility)

print('pref', pref)



used_arguments = []
for arg_set in pref:
    for argument in arg_set:
        if argument not in used_arguments:
            used_arguments.append(argument)


for argument in argument_map:
    if (argument not in used_arguments) and (argument not in self_attacking_arguments):
        pref.append([argument])


print('pref', pref)
"""


admissible = False
#Admissibility
print()
print("Atttempting admissible lable mapping")
print()
if claim_argument not in argument_map:
    print(claim_argument, "is not contained in the argument map")
else:
    #print('argument_labelling HWREEEEEE', argument_labelling)  #*******
    admissible_labelling, passing = admissibility(argument_map, argument_labelling, claim_argument)
    if passing == True:
        admissible = True
        print("Admissible Labelling: ")
        print(admissible_labelling)













#All Mappings - Not really******
all_arg_admiss = []
for argument in argument_map:
    labeling, passing = admissibility(argument_map, argument_labelling, argument)
    if passing == True:
        if labeling not in all_arg_admiss:  #Avoid duplicates
            all_arg_admiss.append(labeling)

print(all_arg_admiss)
for arg_labelling in all_arg_admiss:
    if arg_labelling[claim_argument] == in_:
        admissible = True




# Results
print()
if claim_argument not in argument_map:
    print(claim_argument, "is not contained in the argument map")
else:
    print("Argument ",claim_argument)
    print("Grounded: ", grounded)
    print("Admissible: ", admissible)