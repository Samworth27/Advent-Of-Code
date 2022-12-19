import ast
from functools import cmp_to_key
import copy

def buildList(string):
    return ast.literal_eval(string) 
    
def evalPair(pair0, pair1):
    result = compareList(pair0,pair1)
    if result == True:
        return 1
    if result == False:
        return -1
    if result == None:
        return 0

def compareList(list0, list1):
    list0 = copy.copy(list0)
    list1 = copy.copy(list1)
    while True:
        if len(list0) == 0 and len(list1) > 0:
            return True
        if len(list0) >0 and len(list1) == 0:
            return False
        if len(list0) == 0 and len(list1) == 0:
            return None
        
        item0 = list0.pop(0)
        item1 = list1.pop(0)
        
        result = compareItems(item0, item1)
        
        if result != None:
            return result

def compareInts(int0, int1):
    if int0 == int1:
        return None
    else:
        return int0 < int1
   
def compareItems(item0,item1):
    if type(item0) is list:
        if type(item1) is list:
            return compareList(item0,item1)
        else:
            return compareList(item0,[item1])
    else:
        if type(item1) is list:
            return compareList([item0], item1)
        else:
            return compareInts(item0, item1) 
    
def insertPacket(packet, packet_list):
    packet_list.append(packet)
    packet_list.sort(key = cmp_to_key(evalPair), reverse=True)
    return packet_list

file = open('day13.txt')

index = 1
count = 0
score = 0
packets = [buildList('[[2]]'), buildList('[[6]]')]

for line in [i.strip() for i in file]:
    match count:
        case 0:
            line0 = buildList(line)
            packet_list = insertPacket(line0, packets)
        case 1:
            line1 = buildList(line)
            packet_list = insertPacket(line1, packets)
        case 2:
            
            if compareList(line0,line1):
                score += index
            
            print("end pair")
            index += 1
            count = -1
    count += 1

key1 = packets.index([[2]])+1
key2 = packets.index([[6]])+1
print(key1*key2)