import queue

def converting_initial_position_to_inital_cell(start_x,start_y, paths):
    """Takes the initial position and converts it into its current cell
    Args:
        start_x (integer): x position for robot
        start_y (integer): y position for robot
        paths (list): a list of available paths
    Returns:
        tuple: a tuple containing the initial cell
    """
    initial_cell = (0,0)    
    for x,y in paths:
        if start_x in range(x,x+21) and start_y in range(y-21,y):
            initial_cell = (x,y)
    return initial_cell


def search(start, paths):
    """Using the bfs algorithm, this function finds all
        the neighbours related to the starting position
    Args:
        start (tuple): containing the x and y coordinates
        paths (list): containng all (x,y) coordinates that
                        are not blocked.
    Returns:
        dictionary: a dictionary that contains the parent
                    child relationship between cells
    """    
    solution = {}
    fronteir = queue.Queue()
    visited = []
    x,y = start
    solution[(x,y)] = (x,y)
    fronteir.put((x,y))
    visited.append((x,y))
    
    while not fronteir.empty():
       (x,y) = fronteir.get()
       if (x-20, y) in paths and (x-20,y) not in visited:     # checks the cell on the left
            cell = (x-20, y)
            solution[cell] = (x,y)
            fronteir.put(cell)
            visited.append((x-20,y))
            
       if (x+20,y) in paths and (x+20,y) not in visited:      # checks the cell on the right
            cell = (x+20, y)
            solution[cell]= (x,y)
            fronteir.put(cell)
            visited.append((x+20,y))
            
       if (x,y-20) in paths and (x,y-20) not in visited:       # checks the cell at the bottom
            cell = (x, y-20)
            solution[cell] = (x,y)
            fronteir.put(cell)
            visited.append((x,y-20))
            
       if (x, y+20) in paths and (x,y+20) not in visited:       # checks the cell at the top
            cell = (x,y+20)
            solution[cell] = (x,y)
            fronteir.put(cell)
            visited.append((x,y+20))
            
    return solution
            

def backtracking(start,end,solution):
    """This funct

    Args:
        start (_type_): _description_
        end (_type_): _description_
        solution (_type_): _description_

    Returns:
        _type_: _description_
    """    
    path = []
    end_x, end_y = end
    # start_x,start_y = start
    while start != (end_x,end_y):
        end_value= solution[(end_x,end_y)]
        path.append((end_x,end_y))
        end_x,end_y =end_value 
    path.append(start)
    return path[::-1]
    



