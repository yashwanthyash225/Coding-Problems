class Tree():
    def __init__(self, is_tree = False, x_position = None, y_position = None, height = None, width = None, weight = None, price = None):
        self.is_tree = is_tree
        self.x_pos = x_position
        self.y_pos = y_position
        self.height = height
        self.width = width
        self.weight = weight
        self.price = price
        self.is_cut = False
        
    def get_price(self):
        return self.height * self.width * self.price
    
    def get_weight(self):
        return self.height * self.width * self.weight
    
    
class Details:
    def __init__(self, time, cost, cut_direction = None):
        self.time_needed = time
        self.cost = cost
        self.cut_extra_trees = []
        self.cut_direction = cut_direction
        self.x_loc = None
        self.y_loc = None

class Forest:
    def __init__(self, size):
        self.size = size           
        self.grid = []
        for _ in range(self.size):
            each_row = []
            for _ in range(self.size):
                each_row.append(Tree())
            self.grid.append(each_row)
        self.directions = ["up", "down", "right", "left"]
            
    def construct_forest(self, trees):
        self.trees = []
        for tree in trees:
            x_pos = tree[0]
            y_pos = self.size - 1 - tree[1]
            tree_obj = Tree(True, x_pos, y_pos, tree[2], tree[3], tree[4], tree[5]) 
            self.trees.append(tree_obj)
            self.grid[y_pos][x_pos] = tree_obj 
            
    def get_cut_info(self, current_x, current_y, remaining_time, tree):
        if tree.is_cut == True:
            return Details(remaining_time, 0)
        
        time_needed = abs(current_x - tree.x_pos) + abs(current_y - tree.y_pos) + tree.width
        if time_needed > remaining_time:
            return Details(remaining_time, 0)
        
        tree_cost = tree.get_price()
        
        # Calculating total cost when cutting the tree in RIGHT direction
        x_location = current_x + 1
        prev_tree = tree
        prev_weight = tree.get_weight()
        details_right = Details(time_needed, tree_cost, "right")
        
        while x_location <= min(self.size - 1, prev_tree.x_loc + prev_tree.height):
            next_tree = self.grid[current_y][x_location]
            if next_tree.is_tree == True and next_tree.is_cut == False and prev_weight > next_tree.get_weight:
                details_right.cost += next_tree.get_price()
                details_right.cut_extra_trees.append([next_tree.x_loc, next_tree.y_loc])
                prev_tree = next_tree
            x_location += 1
        
        #Calculating total cost when cutting the tree in LEFT direction
        x_location = current_x - 1
        prev_tree = tree
        prev_weight = tree.get_weight()
        details_left = Details(time_needed, tree_cost, "left")
        
        while x_location >= max(0, prev_tree.xloc - prev_tree.height):
            next_tree = self.grid[current_y][x_location]
            if next_tree.is_tree == True and next_tree.is_cut == False and prev_weight > next_tree.get_weight:
                details_left.cost += next_tree.get_price()
                details_left.cut_extra_trees.append([next_tree.x_loc, next_tree.y_loc])
                prev_tree = next_tree
            x_location -= 1

        #Calculating total cost when cutting the tree in DOWN direction
        y_location = current_y - 1
        prev_tree = tree
        prev_weight = tree.get_weight()
        details_up = Details(time_needed, tree_cost, "up")
        
        while y_location >= max(0, prev_tree.yloc - prev_tree.height):
            next_tree = self.grid[y_location][current_x]
            if next_tree.is_tree == True and next_tree.is_cut == False and prev_weight > next_tree.get_weight:
                details_up.cost += next_tree.get_price()
                details_up.cut_extra_trees.append([next_tree.x_loc, next_tree.y_loc])
                prev_tree = next_tree
            y_location -= 1 
        
        # Calculating total cost when cutting the tree in DOWN direction
        y_location = current_y + 1
        prev_tree = tree
        prev_weight = tree.get_weight()
        details_down = Details(time_needed, tree_cost, "down")
        
        while y_location <= min(self.size - 1, prev_tree.x_loc + prev_tree.height):
            next_tree = self.grid[y_location][current_x]
            if next_tree.is_tree == True and next_tree.is_cut == False and prev_weight > next_tree.get_weight:
                details_down.cost += next_tree.get_price()
                details_down.cut_extra_trees.append([next_tree.x_loc, next_tree.y_loc])
                prev_tree = next_tree
            y_location += 1 
        
        # Return maximum cost of 4 directions
        return max(details_down, details_left, details_up, details_right, key = lambda x : x.cost)
        
                    
    
    def solve(self, remaining_time):
        # Starting position
        current_x = 0
        current_y = self.size - 1
        
        while remaining_time > 0:
            max_criteria = 0
            cut_tree = None
            
            for tree in self.trees:
                if tree.is_cut == False:
                    details = self.get_cut_info(current_x, current_y, remaining_time, tree)
                    details.x_loc = tree.x_loc
                    details.y_loc = tree.y_loc
                    criteria = details.cost / details.time_needed
                    if max_criteria < criteria:
                        max_criteria = criteria
                        cut_tree = details
                        
            if cut_tree == None:
                break
            
            self.print_path(current_x, current_y, cut_tree)
            
            current_x = cut_tree.x_loc
            current_y = cut_tree.y_loc
            remaining_time -= cut_tree.time_needed
    
    def print_path(self, current_x, current_y, details):
        target_x = details.x_loc
        target_y = details.y_loc
        
        horizontal_direction = "right" if target_x > current_x else "left"
        vertical_direction = "down" if target_y > current_y else "up"
        
        # Printing the path from current position to target position
        for _ in range(abs(target_x - current_x)):
            print("move " + horizontal_direction)
        for _ in range(abs(target_y - current_y)):
            print("move " + vertical_direction)
        print("cut " + details.cut_direction)
        
                                
time, grid_size, ntrees = map(int, input().split())
trees = []
for _ in range(ntrees):
    trees.append(list(map(int, input().split())))
    
forest_obj = Forest(grid_size)
forest_obj.insert_trees(trees)
forest_obj.solve(time)
