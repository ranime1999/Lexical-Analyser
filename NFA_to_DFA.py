# -*- coding: utf-8 -*-
"""
Created on Sun May 30 21:25:35 2021

@author: Administrator
"""
import json

class state:   
    def __init__(self):
        self.transitions = {}
        self.isTerminatingState = False
 
nfa = {}
dfa = []
initialState_dfa = state()
Start = ''
initialState = state()
GlobalStack = []
nfa_size = 0

def Create_nfa(data):
    global Start
    global nfa
    global initialState
    Start = data["startingState"]
    nfa[Start] = initialState
    data.pop("startingState")
    for key, value in data.items():
        if(key == Start):
            initialState.isTerminatingState = value["isTerminatingState"]
            initialState.transitions = value
        nfa[key] = state()
        nfa[key].isTerminatingState = value["isTerminatingState"]
        data[key].pop("isTerminatingState")
        nfa[key].transitions = value
        

def epsilon_closure(curr, Set):
    if curr not in Set:
        Set.add(curr)
    if "Epsilon" in list(nfa[curr].transitions.keys()):
        for s in nfa[curr].transitions["Epsilon"]:
            if s not in Set:
                Set.add(s)
                epsilon_closure(s, Set)
   
def state_change(action,Set):
    temp = set()
    for s in Set:
        if action in list(nfa[s].transitions.keys()):
            for dst in nfa[s].transitions[action]:
                if dst not in temp:
                    temp.add(dst)
    return temp

def getAlphabet():
    Aplhabet = []
    for stateID in nfa:
        for key, value in nfa[stateID].transitions.items():
            if key != "Epsilon":
                if key not in Aplhabet:
                    Aplhabet.append(key)
    return Aplhabet

def nfa_to_dfa(Set,Queue,Start):
    global dfa
    global initialState_dfa
    Collection = []
    Counts = []
    #Collection.append(Set)
    #Counts.append(-1)
    c = 0
    epsilon_closure(Start, Set)
    if Set not in list(Collection):
        Collection.append(Set.copy())
        Counts.append(c)
        c = c + 1
        Queue.append(Set.copy())
    index = 0
    
    while (len(Queue)!=0):
        ss = state()
        dfa.append(ss)
        Set.clear()
        Set = Queue[0].copy()
        terminate = False
        
        for s in Set:
            if nfa[s].isTerminatingState == True:
                terminate = True
        
        dfa[index].isTerminatingState = terminate
        
        for action in getAlphabet():
            temp = state_change(action, Set)
            Set = temp.copy()
            for s in temp:
                epsilon_closure(s, Set)
            if len(Set) != 0:
                if Set not in list(Collection): 
                    Collection.append(Set.copy())
                    Counts.append(c)
                    c = c + 1
                    Queue.append(Set.copy())
                    dfa[index].transitions[action] = 'S'+ (c - 1).__str__()
                else:
                    pos = list(Collection).index(Set)
                    dfa[index].transitions[action] = 'S'+Counts[pos].__str__()
                
            temp.clear()
            Set = Queue[0]
        Queue.pop(0)
        index=index+1
                

def main():
    f = open('nfa.json')
    data = json.load(f)
    Create_nfa(data)
    Set = set()
    Queue = []
    
    nfa_to_dfa(Set,Queue,Start)
    for i in range(len(dfa)):
        print(i)
        print(dfa[i].transitions)
        print(dfa[i].isTerminatingState)
    
    dic = {"Starting State":'S0'}
    for i in range(len(dfa)):
        dfa[i].transitions["isTerminatingState"] = dfa[i].isTerminatingState
        for key, value in dfa[i].transitions.items():
            dic['S'+i.__str__()] = dfa[i].transitions
    json_object = json.dumps(dic, indent = 2)
    with open("DFA11.json", "w") as outfile:
        outfile.write(json_object)
    
    
if __name__ == '__main__':
    main()

