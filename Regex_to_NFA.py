# -*- coding: utf-8 -*-
"""
Created on Thu May 20 02:23:42 2021

@author: Administrator
"""
import json
from PySimpleAutomata import automata_IO

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def checkIfValid(regex):
    if (regex[0] == "*") | (regex[-1] == "|") | (regex[-1] == "+") | (regex[0] == ")") | (regex[-1] == "("):
        print("Invalid Regex")
        return False

    l = len(regex) - 1
    occurences_of_char = findOccurrences(regex, '|');
    for i in occurences_of_char:
        if(i!=0 and i<l):
            if(regex[i-1]=="|" )| (regex[i-1]=="+" )|( regex[i+1]=="*") |(regex[i+1]=="|" )|(regex[i+1]=="+" ) |(regex[i+1]==")" ):
                print("Invalid Regex")
                return False
    
    occurences_of_char = findOccurrences(regex, '+');
    for i in occurences_of_char:
        if(i!=0) and (i<l):
            if(regex[i-1]=="|" )| (regex[i-1]=="+" )| (regex[i+1]=="*") |(regex[i+1]=="|" )|(regex[i+1]=="+" ):
                print("Invalid Regex")
                return False
    
    occurences_of_char = findOccurrences(regex, '*');
    for i in occurences_of_char:
        if(i!=0) and (i<l):
            if(regex[i-1]=="|") | (regex[i-1]=="+" )| (regex[i-1]=="*" )|(regex[i+1]=="*" ):
                print("Invalid Regex")
                return False
    
    occurences_of_char = findOccurrences(regex, '(');
    for i in occurences_of_char:
        if(i<l):
            if(regex[i+1]==")" ):
                print("Invalid Regex")
                return False
    
    stack = []
    count = 0
    for char in regex:
        if char == "(":
            stack.append(char)
            count = count + 1
        elif (char == ")") and (not (count == 0)):
            stack.pop()
            count = count - 1
        elif (char == ")") and (count == 0):
            print("Invalid Regex")
            return False
    return True
        
class state:   
    def __init__(self):
        self.transitions = {}
        self.isTerminatingState = False
 
nfa = []
initialState = state()
GlobalStack = []
nfa_size = 0

def InsertDots(regex):
    result = []
    for i in range(len(regex)):
        if i+1 < len(regex):
            result.append(regex[i])
            if (regex[i] != '(') and (regex[i+1] != ')') and (regex[i] != '+') and (regex[i] != '|') and (regex[i+1] != '+') and (regex[i+1] != '|') and (regex[i+1] != '*'):
                result.append('.')
    result.append(regex[-1])
    return result

def prior(c):
    if c == '*':
        return 3
    elif c == '.':
        return 2
    elif (c == '+') or (c == '|'):
        return 1
    else :
        return 0
       
def regex2postfix(exp):
    postfix = []
    stack = []
    for i in range(len(exp)):
        if exp[i] == '(':
            stack.append(exp[i])
        elif exp[i] == ')':
            while stack[-1] != '(':
                postfix.append(stack[-1])
                stack.pop()
            stack.pop()
        elif (exp[i] == '*') or (exp[i] == '+') or (exp[i] == '|') or (exp[i] == '.'):
            while len(stack)!=0:
                if prior(stack[-1]) >= prior(exp[i]):
                    postfix.append(stack[-1])
                    stack.pop()
                else : break
            stack.append(exp[i])
        else:
            postfix.append(exp[i])
    while len(stack)!=0:
        postfix.append(stack[-1])
        stack.pop()
    return postfix           
            
def character(i):
    global nfa_size
    global nfa
    global GlobalStack
    global initialState
    s1 =state()
    s2 =state()
    nfa.append(s1)
    nfa.append(s2)
    
    if i in list(nfa[nfa_size].transitions.keys()):
        nfa[nfa_size].transitions[i].append(nfa_size+1)
    else :
        nfa[nfa_size].transitions[i]= [nfa_size+1]
    GlobalStack.append(nfa_size)
    nfa_size += 1
    GlobalStack.append(nfa_size)
    nfa_size+=1
    
    
    

def concatenation():
    global nfa
    global GlobalStack
    d = GlobalStack[-1]
    GlobalStack.pop()
    c = GlobalStack[-1]
    GlobalStack.pop()
    b = GlobalStack[-1]
    GlobalStack.pop()
    a = GlobalStack[-1]
    GlobalStack.pop()
    if 'epsilon' in list(nfa[b].transitions.keys()) :
        nfa[b].transitions['epsilon'].append(c)
    else :
        nfa[b].transitions['epsilon']= [c]
    GlobalStack.append(a)
    GlobalStack.append(d)
    

    
def OR():
    global nfa_size
    global nfa
    global GlobalStack
    global initialState
    s1 =state()
    s2 =state()
    nfa.append(s1)
    nfa.append(s2)
    
    d = GlobalStack[-1]
    GlobalStack.pop()
    c = GlobalStack[-1]
    GlobalStack.pop()
    b = GlobalStack[-1]
    GlobalStack.pop()
    a = GlobalStack[-1]
    GlobalStack.pop()
    if 'epsilon' in list(nfa[nfa_size].transitions.keys()) :
        nfa[nfa_size].transitions['epsilon'].append(a)
    else :
        nfa[nfa_size].transitions['epsilon']= [a]
    nfa[nfa_size].transitions['epsilon'].append(c)  
    if 'epsilon' in list(nfa[b].transitions.keys()) :
        nfa[b].transitions['epsilon'].append(nfa_size+1)
    else :
        nfa[b].transitions['epsilon']= [nfa_size+1]
    if 'epsilon' in list(nfa[d].transitions.keys()) :
        nfa[d].transitions['epsilon'].append(nfa_size+1)
    else :
        nfa[d].transitions['epsilon']= [nfa_size+1]   
    
    GlobalStack.append(nfa_size)
    nfa_size+=1
    GlobalStack.append(nfa_size)
    nfa_size+=1
    
def asterisk():
    global nfa_size
    global nfa
    global GlobalStack
    global initialState
    s1 =state()
    s2 =state()
    nfa.append(s1)
    nfa.append(s2)
    b = GlobalStack[-1]
    GlobalStack.pop()
    a = GlobalStack[-1]
    GlobalStack.pop()
    if 'epsilon' in list(nfa[nfa_size].transitions.keys()):
        nfa[nfa_size].transitions['epsilon'].append(a)
    else :
        nfa[nfa_size].transitions['epsilon']= [a]
    nfa[nfa_size].transitions['epsilon'].append(nfa_size+1) 
    if 'epsilon' in list(nfa[b].transitions.keys()) :
        nfa[b].transitions['epsilon'].append(nfa_size)
    else :
        nfa[b].transitions['epsilon']= [nfa_size]
    nfa[b].transitions['epsilon'].append(nfa_size+1)
    GlobalStack.append(nfa_size)
    nfa_size+=1
    GlobalStack.append(nfa_size)
    nfa_size+=1

def ConstructNFA(postfix):
    for i in range(len(postfix)):
        if postfix[i] == '*':
            asterisk()
        elif postfix[i] == '.':
            concatenation()
        elif (postfix[i] == '+') or (postfix[i] == '|'):
            OR()
        else:
            character(postfix[i])

def drawJson():
    temp = automata_IO.nfa_json_importer("DrawNFA.json") 
    automata_IO.nfa_to_dot(temp,"image","./")
    
def main():
    regex = input("Enter exp: ")
    if checkIfValid(regex):
        regexp = InsertDots(regex)
        postfix = regex2postfix(regexp);
        ConstructNFA(postfix)
        final_state = GlobalStack[-1]
        GlobalStack.pop()
        start_state = GlobalStack[-1]
        GlobalStack.pop()
        nfa[final_state].isTerminatingState = True
        
        DrawingJson = {'alphabet':[],'states':[],'initial_states':[],'accepting_states':[],'transitions':[]}
        DrawingJson['initial_states'].append('S'+start_state.__str__())
        DrawingJson['accepting_states'].append('S'+final_state.__str__())
        for i in range(len(nfa)):
            DrawingJson['states'].append('S'+i.__str__())
            for key, value in nfa[i].transitions.items():
                if key not in DrawingJson["alphabet"]:
                    DrawingJson["alphabet"].append(key.__str__())
                for k in range(len(value)):
                    DrawingJson['transitions'].append(['S'+i.__str__(),key.__str__(),'S'+value[k].__str__()])
        json_object1 = json.dumps(DrawingJson, indent = 2)
        with open("DrawNFA.json", "w") as outfile:
            outfile.write(json_object1)
        
        drawJson()
        
        dic = {"Starting State":'S'+start_state.__str__() }
        for i in range(len(nfa)):
            nfa[i].transitions["isTerminatingState"] = nfa[i].isTerminatingState
            for key, value in nfa[i].transitions.items():
                dic['S'+i.__str__()] = nfa[i].transitions
        json_object = json.dumps(dic, indent = 2)
        with open("NFA.json", "w") as outfile:
            outfile.write(json_object)
    
    
            
            
    
if __name__ == '__main__':
    main()