file = open("day15.txt")


def manDist(object1, object2):
    return abs(object1.x - object2.x) + abs(object1.y - object2.y)


def sensorFromArray(input):
    return Sensor(input[0], input[1])


class Range():
    def __init__(self, covered_range):
        self.start = covered_range[0]
        self.finish = covered_range[1]

    def intersect(self, other_range):
        if self.start <= other_range.start:
            lower = self
            higher = other_range
        else:
            lower = other_range
            higher = self
            
        if lower.finish >= higher.start:
            return True
        
        return False
    
    def join(self, other_range):
        self.start = min(self.start,other_range.start)
        self.finish = max(self.finish,other_range.finish)
        
    def limit(self):
        self.start = max(self.start, 0)
        self.finish = min(self.finish, 4000000)
        
    def __repr__(self) -> str:
        return f"{self.start,self.finish}"


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Beacon():
    def __init__(self, own_loc):
        self.x = own_loc[0]
        self.y = own_loc[1]


class Sensor():
    count = 0
    def __init__(self, own_loc, beacon_loc):
        self.id = Sensor.count
        Sensor.count += 1
        
        self.x = own_loc[0]
        self.y = own_loc[1]
        self.nearest_beacon = Beacon(beacon_loc)
        self.calcMinMax()

    def calcMinMax(self):
        self.nearest_distance = manDist(self, self.nearest_beacon)
        self.xmin = self.x - self.nearest_distance
        self.xmax = self.x + self.nearest_distance
        self.ymin = self.y - self.nearest_distance
        self.ymax = self.y + self.nearest_distance

    def pointInRange(self, point):
        return manDist(self, point) <= self.nearest_distance

    def pointsAtRow(self, row):
        y_dist = abs(self.y - row)
        # print(f"sensor {self.id} {y_dist}/{self.nearest_distance} from row {row}")
        if y_dist > self.nearest_distance:
            return None
        remainder = self.nearest_distance - y_dist
        # print(f"{self.x = }  {remainder = }")
        start = self.x - remainder
        end = self.x + remainder
        return (start, end)


class SensorMap():
    def __init__(self):
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.sensors = []
        self.sensor_points = set()
        self.beacons = []
        self.beacon_points = set()

    def addSensor(self, new_sensor):
        self.xmin = min(self.xmin, new_sensor.xmin)
        self.xmax = max(self.xmax, new_sensor.xmax)
        self.ymin = min(self.ymin, new_sensor.ymin)
        self.ymax = max(self.ymax, new_sensor.ymax)
        self.addBeacon(new_sensor.nearest_beacon)
        self.sensors.append(new_sensor)
        self.sensor_points.add((new_sensor.x, new_sensor.y))

    def addBeacon(self, new_beacon):
        if (new_beacon.x, new_beacon.y) not in self.beacon_points:
            self.beacons.append(new_beacon)
            self.beacon_points.add((new_beacon.x, new_beacon.y))

    def notABeacon(self, point):
        if (point.x, point.y) in self.beacon_points:
            return False
        for sensor in self.sensors:
            if sensor.pointInRange(point):
                return True
        return False

    def checkRow(self, row, restricted_range = False, return_ranges=False):
        # count = 0
        # for x in range(self.xmin,self.xmax+1):
        #     print(f"{x-self.xmin}/ {(self.xmax+1)-self.xmin}")
        #     if self.notABeacon(Point(x,row)):
        #         count += 1
        # return count
        ranges = []
        
        def addRange(new_range):
            for r in ranges:
                if r.intersect(new_range):
                    r.join(new_range)
                    joinExistingRanges()
                    break
            else:
                ranges.append(new_range)
        
        def joinExistingRanges():

            for i in range(len(ranges)):
                for j in range(i+1, len(ranges)):
                    # print(ranges,i,j)
                    if len(ranges) < 2:
                        return False
                    if ranges[i].intersect(ranges[j]):
                        ranges[i].join(ranges[j])
                        ranges.pop(j)
                        joinExistingRanges()
                        break
        
        for sensor in self.sensors:
            covered_range = sensor.pointsAtRow(row)
            if covered_range == None:
                continue
            new_range = Range(covered_range)
            if restricted_range:
                new_range.limit()
            if len(ranges) == 0:
                ranges.append(new_range)
                continue
            addRange(new_range)
           
        if return_ranges:
            return ranges
        
        count = 0
        for row_range in ranges:
            count += (row_range.finish+1) - row_range.start
        
        if not restricted_range:
            for beacon in self.beacons:
                if beacon.y == row:
                    count -= 1
        return count

def findBeacon():
    y = findBeaconRow()
    # y = 3186981
    row = sensors.checkRow(y, True, True)
    x = findBeaconX(row)
    return x * 4000000 + y

def findBeaconRow():
    for y in range(0,40000001):
        if y%100000 == 0:
            print(y)
        row = sensors.checkRow(y, True) 
        if row != 4000001:
            return y

def findBeaconX(row):
    if len(row) == 1:
        if min(row) != 0:
            return 0
        if max(row) != 4000000:
            return 4000000
    if len(row) == 2:
        if row[0].start == 0:
            low = row[0]
            high = row[1]
        else:
            low = row[1]
            high = low[0]
        return(high.start - 1)

sensors = SensorMap()

for line in file:
    sensors.addSensor(sensorFromArray([[int(coord.strip().split(
        '=')[-1]) for coord in part.strip().split('at')[-1].split(',')] for part in line.strip().split(':')]))

# print(sensors.checkRow(2000000))
# print(sensors.checkRow(3186981, True, True))
print(findBeacon())