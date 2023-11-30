#! /usr/bin/python

import sys
import json
 


# arguments:
# INPUT: PROGRAMM_NAME ONTOLOGY_FILE CLASS_NAME #CHANGE*********
# i.e.: el_reasoner.py SushiOntology.rdf Maki
# i.e.: main.py example-argumentation-framework.json
if len(sys.argv) >= 2:  #CGHECK THIUS PART*******
    json_file = sys.argv[1]
    #class_name = sys.argv[2]   #******
else:
    json_file = "example-argumentation-framework.json"
    #class_name = "Maki"    #******

print("FILE: ", json_file)  #********


    # LOADING JSON FILE
 
# Opening JSON file
file = open(json_file)

data = json.load(file)

#This is how you access all arguments keys
print()
print("Arguments")
for i in data['Arguments']:
    print(i)

#This is how you access all attack relations
print()
print("Attack Relations")
for i in data['Attack Relations']:
    print(i)

#Complete dictionary
    #These are dictionaries within dictionaries
print()
print(type(data))
print(data)

#This is how you access individual argument definition
print()
print("Individual Argument")
print(data['Arguments']['0'])   #Notice that '0' is a character, not an interger, and as dictionary, you need to call it as so


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
print(argument_labelling)

    #This should not be needed, as the 'Skeptical' label assignment that follows should also handle it. Just here for notes
#If there are nodes that are not attacked by any other, assigned as In / True
is_there_anchor = False
for argument in argument_map:
    if bool(argument_map[argument][1]) == False:    #Then the list of atttacking nodes is empty, the boolean will result in False
        argument_labelling[argument] = in_
        is_there_anchor = True

#****** If there is a node tagged as in (is_there_anchor==True), then we can start there #Not in use


    #This results in a 'Skeptical' label assignment
change = True
while change:
    change = False
    for argument in argument_map:
        parents_labels=[]
        for parent in argument_map[argument][1]:
            parents_labels.append(argument_labelling[parent])
        if in_ in parents_labels:   #Label node Out
            prev_label = argument_labelling[argument]
            if prev_label != out_: # If the label has changed, replace it and note the change
                argument_labelling[argument]=out_
                change = True
        # We can assume here that there was no parent In
        elif undef_ in parents_labels:  #***This might not be needed, because we label all arguments Undefined to begin with
            prev_label = argument_labelling[argument]
            if prev_label != undef_: # If the label has changed, replace it and note the change
                argument_labelling[argument]=undef_   #***CHECK LABEL*****
                change = True
        # Here we can assume that the parent list does not contain In or Undefined, meaning only Out or not parents / attackers
        #CHECK***** I might not need initial is_there_anchor label assignment***********
        else:
            prev_label = argument_labelling[argument]
            if prev_label != in_: # If the label has changed, replace it and note the change
                argument_labelling[argument]=in_
                change = True


#***** We have to have ways to find loops   <-- needs to implement, to assign valuese when there areen't any ancher points



print()
print('argument_labelling')
print(argument_labelling)