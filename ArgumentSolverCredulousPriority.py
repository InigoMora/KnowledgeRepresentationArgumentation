#! /usr/bin/python

from ast import arg
from operator import truediv
from re import T
import sys
import json

import time



start_time = time.time()

#print("--- %s seconds ---" % (time.time() - start_time))



# arguments:
# INPUT: PROGRAMM_NAME ARGUMENTATION_FRAMEEWORK
# i.e.: main.py example-argumentation-framework.json
    # default values
claim_argument = 'a'
json_file = "1_work_life_balance.json"
if len(sys.argv) >= 2:  #CGHECK THIUS PART*******
    json_file = sys.argv[1]
    if len(sys.argv) >= 3:  #CGHECK THIUS PART*******
        claim_argument = sys.argv[2]


print("FILE: ", json_file)  #********
print("Argument: ", claim_argument)
print()

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


cred_prefered_cred_adm_cred_comp=False

if claim_argument not in argument_map:
    print("WARNING:")
    print("Faild to locate suggested argument in the argument map")
    print()
    
    print("      CREDULOUS")
    print("Argument not in argument map, thus")
    print("Credulous Preferred: ", cred_prefered_cred_adm_cred_comp)    #I could just repeat the same cred_prefered for all three
    print("Credulous Admissible: ", cred_prefered_cred_adm_cred_comp)
    print("Credulous Complete: ", cred_prefered_cred_adm_cred_comp)
    print("Runtime", "--- %s seconds ---" % (time.time() - start_time))
#else-  #The rest of the code can be moved here to avoid an argument that  was not found

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

    #This should not be needed, as the 'Skeptical' label assignment that follows should also handle it. Just here for notes
#If there are nodes that are not attacked by any other, assigned as In / True

"""
for argument in argument_map:
    if bool(argument_map[argument][1]) == False:    #Then the list of atttacking nodes is empty, the boolean will result in False
        argument_labelling[argument] = in_
"""

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
                        if argument_labelling_[argument] != out_:   # If the attepmted labelling is different from that from which we would be assigning now (out)
                            return argument_labelling_, passing  #Then it means this cannot hold, we would be in a loop, so we return the prvious dictionary
                    argument_labelling[argument]=out_
                    change = True
            # We can assume here that there was no parent In
            elif undef_ in parents_labels:  #***This might not be needed, because we label all arguments Undefined to begin with
                prev_label = argument_labelling[argument]
                if prev_label != undef_: # If the label has changed, replace it and note the change
                    if argument in unchageable_arguments:     # If the argument is in the list of arguments we have opted to try (unchageable_arguments_)
                        if argument_labelling_[argument] != undef_:   # If the attepmted labelling is different from that from which we would be assigning now (undef_)
                            return argument_labelling_, passing  #Then it means this cannot hold, we would be in a loop, so we return the prvious dictionary
                    argument_labelling[argument]=undef_   
                    change = True
            # Here we can assume that the parent list does not contain In or Undefined, meaning only Out or not parents / attackers
            else:
                #print("MAde it here")
                if argument in unchageable_arguments:     # If the argument is in the list of arguments we have opted to try (unchageable_arguments_)
                    if argument_labelling_[argument] != in_:   # If the attepmted labelling is different from that from which we would be assigning now (in_)
                        return argument_labelling_, passing  #Then it means this cannot hold, we would be in a loop, so we return the prvious dictionary
                prev_label = argument_labelling[argument]
                if prev_label != in_: # If the label has changed, replace it and note the change
                    argument_labelling[argument]=in_
                    change = True
                    #print("SECOND PASSING")
                    #print("change", change)

        passing=True
        return argument_labelling, passing









    #IMPLEMENT FULL GROUND LABELLING
"""
grounded_labelling, passing = proposed_argument_labelling(argument_map, argument_labelling)

#building first labelling
change = True
argument_labelling = grounded_labelling.copy()
old_labelling = grounded_labelling.copy()
while change:
    print('·HEEERE')
    argument_labelling, passing = proposed_argument_labelling(argument_map, argument_labelling)

    print(argument_labelling.values())
    print(old_labelling.values())
    if argument_labelling == old_labelling:
        print('SAMEEEEEE')
        change = False
    old_labelling = argument_labelling.copy()
print('argument_labelling')
print(argument_labelling)
"""

    # With no unchageable_arguments_, resultts in grouded Labelling
argument_labelling, passing = proposed_argument_labelling(argument_map, argument_labelling)

    #NOTE: THere is a bug in proposed. run 
            #  argument_labelling, passing = proposed_argument_labelling(argument_map, argument_labelling)
    # repetedly until the full vesion of grounded can be achieved 
    # Run code as described above, making sure to adjust the necesaries grounded_labelling use when checking for argument labels

def admissibility(argument_map, argument_labelling, claim_argument_):
    #This loops through the different cyclical argument chains, until all have been resolved
    #NOTE: to improve, different attempts in every chain should be recorded, to minimize uncertainty

    #simple attempt ******
    proposed_argument_labels = argument_labelling.copy()    #creates a copy of argument_labelling to edit, keeps the old for comparing and creating other ones ***needs to implement***
    prev__argument_labels = argument_labelling.copy()
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
    
    new_proposed_argument_labels, passing = proposed_argument_labelling(argument_map, proposed_argument_labels, unchageable_arguments)

    if passing == False:    #The proposed assumtion did not work********
            #print("Initial admissiblility test has been Failed")
            return argument_labelling, False
    # If the previous statemnt is true (new_proposed_argument_labels did not pass), the following if statement will not hold
    if (passing == True) and (new_proposed_argument_labels != prev__argument_labels):   #The new_proposed_argument_labels, which passed the test, is different from prev__argument_labels, and thus an extention***
        proposed_argument_labels = new_proposed_argument_labels.copy()  #We update the proposed to match the new mapping
        prev__argument_labels = new_proposed_argument_labels.copy()     #And also the prev__argument_labels, as we will use it to default to it if proposed_argument_labels fails the labelling in the future
        change=True
        #print("Initial admissiblility test has been passed")

    while change==True:
        change = False
        for argument in argument_map:
            #print("argument: ", argument, proposed_argument_labels[argument])  #********
            if (proposed_argument_labels[argument] == undef_):   #If the node is labeled as undefined
                for parent in argument_map[argument][1]:
                    if (proposed_argument_labels[parent] == undef_) and (parent != argument): #If the parent node is labeled as undefined, and the parent node is not the original node (no self attacking argument)
                        proposed_argument_labels[argument] = in_
                        unchageable_arguments.append(argument)
                        proposed_argument_labels[parent] = out_
                        unchageable_arguments.append(parent)
                        break
                    #print("PASS 1") #This does NOT run
                    break
                #print("PASS 2") #This runs
                break
            #print("PASS 3") #This runs
            #break
        
        #print("THis STILL RUNS")
        new_proposed_argument_labels, passing = proposed_argument_labelling(argument_map, proposed_argument_labels, unchageable_arguments)
        if passing == False:    #The proposed assumtion did not work********
            proposed_argument_labels = prev__argument_labels.copy()    #If if failed, we default the proposed to the previous labelling, as it is no longer proposed
        # If the previous statemnt is true (new_proposed_argument_labels did not pass), the following if statement will not hold
        if (passing == True) and (new_proposed_argument_labels != prev__argument_labels):   #The new_proposed_argument_labels, which passed the test, is different from prev__argument_labels, and thus an extention***
            proposed_argument_labels = new_proposed_argument_labels.copy()  #We update the proposed to match the new mapping
            prev__argument_labels = new_proposed_argument_labels.copy()     #And also the prev__argument_labels, as we will use it to default to it if proposed_argument_labels fails the labelling in the future
            change=True

    if argument_labelling != proposed_argument_labels:  #Meaening the accepted proposed labelling has changed, and approved of the claim_argument as in_
        return proposed_argument_labels, True
    else:
        return proposed_argument_labels, False


grounded = False

if claim_argument in argument_map:
    if argument_labelling[claim_argument] == in_:
        cred_prefered_cred_adm_cred_comp  = True
        print("      CREDULOUS")
        print("Argument",claim_argument)
        print("With principle Cred_adm(a,F)=Cred_pref(a,F)=Cred_comp(a,F)")
        print("Credulous Preferred: ", cred_prefered_cred_adm_cred_comp)    #I could just repeat the same cred_prefered for all three
        print("Credulous Admissible: ", cred_prefered_cred_adm_cred_comp)
        print("Credulous Complete: ", cred_prefered_cred_adm_cred_comp)
        print("Runtime", "--- %s seconds ---" % (time.time() - start_time))
        print("Argument found in grounded labelling")
        grounded = True
        


#All Mappings - Not really******
all_arg_admiss = []
for argument in argument_map:
    labeling, passing = admissibility(argument_map, argument_labelling, argument)
    if passing == True:
        if labeling not in all_arg_admiss:  #Avoid duplicates
            all_arg_admiss.append(labeling)


#Grounded
ground = []
for argument in argument_labelling:
    if argument_labelling[argument] == in_:
        ground.append(argument)

#Already assigned previously
# if claim_argument in ground:
#    grounded = True


#Admissibility
admissible = False

if claim_argument in argument_map:  #Make sure hte argument searched for is in the list, else the directory will complain
    for arg_labelling in all_arg_admiss:
        if arg_labelling[claim_argument] == in_:
            if cred_prefered_cred_adm_cred_comp == False:
                cred_prefered_cred_adm_cred_comp = True
                print("      CREDULOUS")
                print("Argument",claim_argument)
                print("With principle Cred_adm(a,F)=Cred_pref(a,F)=Cred_comp(a,F)")
                print("Credulous Preferred: ", cred_prefered_cred_adm_cred_comp)    #I could just repeat the same cred_prefered for all three
                print("Credulous Admissible: ", cred_prefered_cred_adm_cred_comp)
                print("Credulous Complete: ", cred_prefered_cred_adm_cred_comp)
                print("Runtime", "--- %s seconds ---" % (time.time() - start_time))
                print("Argument found in admissible labelling")
            admissible = True

# Prefered labelling
pref = []
for arg_labelling in all_arg_admiss:
    pref_group = []
    for argument in arg_labelling:
        if arg_labelling[argument] == in_:
            pref_group.append(argument)
    pref.append(pref_group)


prefered = False
if [claim_argument] in pref:
    if cred_prefered_cred_adm_cred_comp == False:
        cred_prefered_cred_adm_cred_comp = True
        print("      CREDULOUS")
        print("Argument",claim_argument)
        print("With principle Cred_adm(a,F)=Cred_pref(a,F)=Cred_comp(a,F)")
        print("Credulous Preferred: ", cred_prefered_cred_adm_cred_comp)    #I could just repeat the same cred_prefered for all three
        print("Credulous Admissible: ", cred_prefered_cred_adm_cred_comp)
        print("Credulous Complete: ", cred_prefered_cred_adm_cred_comp)
        print("Runtime", "--- %s seconds ---" % (time.time() - start_time))
        print("Argument found in Preferred labelling")
    prefered = True


# Results
print()
if claim_argument not in argument_map:
    print("argument", claim_argument, "is not contained in the argument map")
else:
    if cred_prefered_cred_adm_cred_comp == False:
        
        print("      CREDULOUS")
        print("Argument",claim_argument)
        print("With principle Cred_adm(a,F)=Cred_pref(a,F)=Cred_comp(a,F)")
        print("Credulous Preferred: ", cred_prefered_cred_adm_cred_comp)    #I could just repeat the same cred_prefered for all three
        print("Credulous Admissible: ", cred_prefered_cred_adm_cred_comp)
        print("Credulous Complete: ", cred_prefered_cred_adm_cred_comp)
        print("Runtime", "--- %s seconds ---" % (time.time() - start_time))
        print()
        
    print("Argument",claim_argument, "in the calculated labellings")
    print("Grounded: ", grounded)
    print("Admissible: ", admissible)
    print("Preferred: ", prefered)




print()
print('argument_map')
print(argument_map)

print()
print('These arguments have no attackers (are free arguments):')
free_arg=[]
for argument in argument_map:
    if bool(argument_map[argument][1]) == False:    #Then the list of atttacking nodes is empty, the boolean will result in False
        free_arg.append(argument)
print(free_arg)

    #IMPLEMENT FULL GROUND LABELLING -- Placeholder
#Updating the grounded labelling to full coverage
change = True
old_labelling = argument_labelling.copy()
while change:
    argument_labelling, passing = proposed_argument_labelling(argument_map, argument_labelling)
    if argument_labelling == old_labelling:
        change = False
    old_labelling = argument_labelling.copy()

print()
print('Grounded labelling map')
print(argument_labelling)

print()
print("Grounded labellings")
print(ground)

print()
print("Admissible labelling map")
print(all_arg_admiss)


print()
print("Preferred labellings")
print(pref)


















#NOTE:
    # *********IGNORE*********
#Stable --> conflict free, and attacks all other arguments not in list
#Complete --> if Tf(S)={a, c} --> {a, c}


#CHANGE******** Credulous means that if in admissible, it is in preferred 
#****ADD Credulous assumption


#********
"""
Complete - Union between skeptical preferred and grounded
 YESSSS

Complete always include empty set (?) and admissible(?)
"""

#******+ Add Credulous admissible *******
#****+*check Admissible *****

#******change Skeptical argument_labelling tittle



# fix grounding
# fix print sttaetmtstn 

