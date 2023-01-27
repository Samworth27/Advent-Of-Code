from aoc_util.inputs import parse_input
import re 

DAY = 21
YEAR = 2015

class Character:
    def __init__(self,hp,attack,armour):
        self.hp = hp
        self.attack = attack
        self.armour = armour
        
    def receive_damage(self,damage):
        damage = max(1,damage - self.armour)
        self.hp -= damage
        
    @property
    def alive(self):
        return self.hp > 0

class Loadout:
    def __init__(self,weapon,armour = None,ring1 = None,ring2 = None):
        self.weapon = weapon
        self.armour = armour
        self.ring1 = ring1
        self.ring2 = ring2
    
    @property
    def stats(self):
        stats_ = {'damage':0,'armour':0} 
        for item in [x for x in [self.weapon,self.armour,self.ring1, self.ring2] if x]:
            stats_['damage'] += item.damage
            stats_['armour'] += item.armour
        return stats_
    
    @property
    def cost(self):
        cost_ = 0
        for item in [x for x in [self.weapon,self.armour,self.ring1, self.ring2] if x]:
            cost_ += item.cost
        return cost_
        
    
class Item:
    def __init__(self,cost,damage,armour):
        self.cost = cost
        self.damage = damage
        self.armour = armour
        
    def __str__(self):
        return f"Cost: {self.cost} Damage: {self.damage} Armour: {self.armour}"
    
    def __repr__(self):
        return f"<Item {str(self)} >"

def viable_build(player,boss):    
    while player.alive and boss.alive:
        if player.alive:
            boss.receive_damage(player.attack)
        if boss.alive:
            player.receive_damage(boss.attack)
    return player.alive



def all_builds():
    item_data = parse_input('items',lambda x: [int(i) for i in re.findall(r'\d+',x)])
    weapons = [Item(*stats[-3:]) for stats in item_data[1:5]]
    armours = [Item(*stats[-3:]) for stats in item_data[8:12]]
    armours.append(Item(0,0,0))
    rings = [Item(*stats[-3:]) for stats in item_data[16:21]]
    rings.append(Item(0,0,0))
    rings.append(Item(0,0,0))
    for weapon in weapons:
        for armour in armours:
            for ring1 in rings:
                for ring2 in rings:
                    if ring1 == ring2:
                        continue
                    yield weapon,armour,ring1,ring2

def part1():
    boss_stats = parse_input((DAY,YEAR),lambda x: int(x.split(':')[-1]))
    viable_builds = []
    for weapon,armour,ring1,ring2 in all_builds():
        player_loadout = Loadout(weapon,armour,ring1,ring2)
        player = Character(100,*player_loadout.stats.values())
        boss = Character(*boss_stats)
        if viable_build(player,boss):
            viable_builds.append(player_loadout)
            
    print(sorted(viable_builds, key=lambda x: x.cost)[0].cost)

def part2():
    boss_stats = parse_input((DAY,YEAR),lambda x: int(x.split(':')[-1]))
    non_viable_builds = []
    for weapon,armour,ring1,ring2 in all_builds():
        player_loadout = Loadout(weapon,armour,ring1,ring2)
        player = Character(100,*player_loadout.stats.values())
        boss = Character(*boss_stats)
        if not viable_build(player,boss):
            non_viable_builds.append(player_loadout)
    
    print(sorted(non_viable_builds, key=lambda x: x.cost, reverse=True)[0].cost)   
    
if __name__ == '__main__':
    part1()
    part2()