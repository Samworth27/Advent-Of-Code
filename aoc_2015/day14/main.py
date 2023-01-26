from aoc_util.inputs import parse_input, fields

DAY = 14
YEAR = 2015


class Reindeer:
    def __init__(self, fly_speed, fly_time, rest_time):
        self.fly_speed = fly_speed
        self.fly_time = fly_time
        self.rest_time = rest_time
        self.cycle_time = fly_time + rest_time
        self.cycle_distance = fly_time * fly_speed

    def distance_in_time(self, time):
        # First calculate the distance travelled in completed cycles of flying and resting
        distance_travelled = (time // self.cycle_time) * self.cycle_distance
        # print(f"{self.cycle_time}s per cycle in {time}s is {time // self.cycle_time} full cycles at {self.cycle_distance}km per cycle = {distance_travelled}")
        
        # Now add any distance travelled in the remaining time
        remaining_time = time % self.cycle_time
        # print(f"{remaining_time}s left over at {self.fly_speed}km/s is {remaining_time * self.fly_speed}km travelled")
        if remaining_time < self.fly_time:
            distance_travelled += remaining_time * self.fly_speed
        else:
            distance_travelled += self.cycle_distance
        # print(f"Total distance travelled is {distance_travelled}")
        return distance_travelled
    
    def distance_at_time(self,time):
        return min(self.fly_time,time % self.cycle_time)*self.fly_speed + self.cycle_distance * (time//self.cycle_time)


def test():
    comet = Reindeer(14, 10, 127)
    dancer = Reindeer(16, 11, 162)
    print(f"Part1: Comet travelled {comet.distance_in_time(1000)}km in 1000s")
    print(f"Part1: Dancer travelled {dancer.distance_in_time(1000)}km in 1000s")
    print(f"Part2: Comet travelled {comet.distance_at_time(1000)}km in 1000s")
    print(f"Part2: Dancer travelled {dancer.distance_at_time(1000)}km in 1000s")


def fields_function(field):
    try:
        return int(field)
    except ValueError:
        return field


def parse_function(row):
    return fields(row, [0, 3, 6, 13], field_func=fields_function)


def part1():
    time = 2503
    reindeer = {name: Reindeer(*values).distance_at_time(time)
                for name, *values in parse_input((DAY, YEAR), parse_function)}
    reindeer = sorted(reindeer.items(), key=lambda x: x[1], reverse=True)
    for name, distance in reindeer:
        print(f"{name} travelled {distance}km")
    print(
        f"The winner is {reindeer[0][0]} at a distance of {reindeer[0][1]}km.")

def part2():
    time = 2503
    reindeer = {name: [Reindeer(*values), 0] for name, *values in parse_input((DAY, YEAR), parse_function)}
    for i in range(1,time+1):
        leader = sorted([(name,racer.distance_at_time(i)) for (name, [racer,score]) in reindeer.items()], key=lambda x: x[1], reverse=True)[0]
        reindeer[leader[0]][1] += 1
    winner = sorted([(name,score) for (name, [racer,score]) in reindeer.items()], key=lambda x: x[1], reverse=True)
    print(winner)
    
if __name__ == '__main__':
    # test()
    # part1()
    part2()
