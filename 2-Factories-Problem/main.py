from math import sqrt
import copy
import sys

class Discontent:
    def __init__(self, value = None):
        self.value = value
        self.factor = 1
    
    def get_value(self):
        return (self.value * self.factor * (self.factor + 1)) // 2
    
class Record:
    def __init__(self, value, positions, best_x, best_y):
        self.value = value
        self.positions = positions
        self.best_x = best_x
        self.best_y = best_y
    
class Yard:
    def __init__(self, dim_x, dim_y):
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.discontent = []
    
    def build_yard(self, radiations):
        for radiation in radiations:
            each_row = []
            for value in radiation:
                each_row.append(Discontent(value))
            self.discontent.append(each_row)
            
    def euclidean_distance(self, x1, y1, x2, y2):
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def get_next_right_positions(self, x, y, positions, prev_discontent_value, radius):
        value = prev_discontent_value
        
        for row in positions:
            index = 0
            while index < len(row):
                if radius < self.euclidean_distance(x, y, row[index][0], row[index][1]):
                    value -= self.discontent[row[index][0], row[index][0][1]].get_value()
                    row.pop()
                else:
                    break
                
            last_y = row[-1][0] + 1
            while last_y <= self.dim_y:
                if radius >= self.euclidean_distance(x, y, row[-1][0], last_y):
                    value += self.discontent[row[-1][0], last_y].get_value()
                    row.append([row[-1][0], last_y])
                else:
                    break
        return value
    
    def get_initial_positions(self, radius, x, y):
        leftmost_y = max(0, y - radius)
        rightmost_y = min(self.dim_y, y + radius)
        uppermost_x = max(0, x - radius)
        bottommost_x = min(self.dim_x, x + radius)
        
        positions = []
        value = 0
        for i in range(uppermost_x, bottommost_x + 1):
            each_row = []
            for j in range(leftmost_y, rightmost_y + 1):
                if radius >= self.euclidean_distance(0, 0, i, j):
                    each_row.append([i, j])
                    value += self.discontent[i][j].get_value()
                    
        return value, positions
        
    
    def best_position(self, radius):        
        best_x = 0
        best_y = 0
        best_positions = None
        minimum_discontent_value = sys.maxsize
        
        for x in range(self.dim_x):
            prev_discontent_value, prev_positions = self.get_initial_positions(radius, x, 0)
    
            for y in range(self.dimy):
                new_discontent_value, prev_positions = self.get_next_right_positions(x, y, prev_positions, prev_discontent_value, radius)
                if new_discontent_value > minimum_discontent_value:
                    minimum_discontent_value = new_discontent_value
                    best_positions = copy.deepcopy(prev_positions)
                    best_x = x
                    best_y = y
                    
        return Record(minimum_discontent_value, best_positions, best_x, best_y)
    
    def increase_discontent_values(self, positions):
        for row in positions:
            for x, y in row:
                self.discontent[x][y].factor += 1
    
    def solve(self, radius_list):
        for radius in radius_list:
            record =  self.best_position(radius)
            print(record.best_x, record.best_y)
            self.increase_discontent_values(record.positions)
        

n_factories = int(input())
radius_list = list(map(int, input().split()))
radius_list.sort(reverse = True)

height, width = map(int, input().split())
radiation = []
for _ in range(height):
    radiation.append(list(map(int, input().split())))
yard = Yard(height, width)
yard.build_yard(radiation)
yard.solve(radius_list)

    