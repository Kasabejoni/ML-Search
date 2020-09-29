import random
import copy
import numpy as nump


def main():
    array = generate_basic_board();
    array1 = random_board();
    print(FindPlayPath(array, array1, 3, True))
def listmoves(board,goal): #generate list of node with posible moves
    listmoves=optional_moves(board,goal)
    listnodes=[]
    new_node = Node()
    for n in listmoves:
        print("aaa")
        new_node = Node(board, n)
        listnodes.append(new_node)
    return listnodes
class Node():

    def __init__(self, parent=None, board=None):
        self.parent = parent
        self.board = board

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.board == other
def a_search(board, goal, counter, detail):
    start_node = Node(None, board)
    start_node.g = start_node.f = start_node.h = 0
    end_node = Node(None, goal)
    end_node.g = end_node.f = end_node.h = 0

    openset = []
    closedset = []

    openset.append(start_node)

    while openset:
        print("iteration:", counter)
        current_node =  min(openset, key=lambda o:o.g + o.h)
        current_index = 0
        for index, node in enumerate(openset):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        openset.pop(current_index)
        closedset.append(current_node)

        if current_node.board == end_node.board: #foundebord
            path = []
            c = current_node

            while c is not None:
                path.append(c.board)
                c = c.parent
            path.reverse()
            i = 0
            for p in path:
                print("Move number :", i)
                if detail:
                    print("h :", huristic(p, goal))
                    print("g  :", i)
                    print("f :", i + huristic(p, goal))
                printA(p)
                i += 1
            print("Goal :")
            printA(goal)
            return "Path is found"
        possible_nodes =listmoves(current_node.board,end_node.board)
        for node in possible_nodes:
            for closed_node in closedset:
                if node == closed_node:
                    continue
            node = node_v(node, current_node, goal)
            for open_node in openset:
                if node == open_node and node.g > open_node.g:
                    continue
            openset.append(node)
        counter += 1
        if detail:
            print("huristic: ", current_node.h)

        if counter == 1000:
            return "no path found"
def ismaxvalue(value):
    if value ==36:
        return True
    return False
class Node_T:
    def __init__(self,a, b, id, father):
        self.board =a
        self.value = b
        self.id = id
        self.father = father

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value
def huristic(board, goal):
    h = 36 - value_curr(board, goal)
    return h
def node_v(node, current_node, goal):
    node.h = huristic(node.board, goal)
    node.g = current_node.g + 1
    node.f = node.g + node.h
    return node
def local_beam(board, goal, counter, k, detail):
    current_value = value_curr(board, goal)
    print("value: ", current_value)
    if current_value == 36:
        print("goal:  ")
        printA(goal)
        return "found"
    else:
        moves1 = []
        op = []
        moves = optional_moves( board, goal)
        print("//////////////////////")
        for i in moves:
            Node = Node_T(i, value_curr(board, goal), 0, 0)
            moves1.append(Node)
            random.shuffle(moves1)
        moves.clear()
        for i in range(k):
             if not(arr_isempty(moves1)):
                random_path = moves1.pop(len(moves1) - 1)
                random_path.id = i
                op.append(random_path)
        while True:
                moves1.clear()
                print("iteration :   ", counter)
                for s in op:
                    if s.value == 36:
                        print("goal:  ")
                        printA(goal)
                        return "Path found"
                    moves1 = optional_moves( s.board, goal)
                    for m in moves1:
                        curr=value_curr(m, goal)
                        move = Node_T(m, curr, 0, s.father)
                        if len(moves) > 0:
                            if not board_exists(move.board, moves):
                                moves.append(move)  
                        else:
                            moves.append(move)  

                if counter > 50 or arr_isempty(moves):
                        print("No more moves")
                        print("best path : ")
                        if not arr_isempty(op):
                         printA(max(op).board)
                         print("state value :", max(op).value)
                        print("goal:  ")
                        printA(goal)
                        return "No path found"
                else:
                        print("")
                if detail:
                         print("details:")

                         for m in moves:
                            printA(m.board)
                            print("value :", m.value)
                            print("")
                         print("End")

                         op.clear()
                         moves.sort()
                for i in range(k):
                    if i<=len(moves)-1:
                        best = moves.pop(len(moves) - 1)
                        op.append(best)
                counter += 1
        return ""
def arr_isempty(arr):
    if len(arr)==0:
        return True
def pathisfound (value):
    if value == 36:  #  found
        print("Path found")
def printgoal(arr):
    print("goal:  ")
    printA(arr)

def S_A(start_board, goal_board, original_board, t, Temp):
    current_value = value_curr(start_board, goal_board)
    TO=Temp
    if pathisfound(current_value):  #  found
        printgoal(goal_board)
        return "Path found"
    else:
        while t <= 100 :
            Temp = TO /(1+t)
            if pathisfound(current_value):   #  found
                printgoal(goal_board)
                return "Path found"
            moves = optional_moves(start_board, goal_board)
            if arr_isempty(moves):
                board = original_board
                break
            print("iteration: ", t)
            print("current value: ", current_value)
            random_move = random.choice(moves)
            n_value = value_curr(random_move, goal_board)
            delta = n_value - current_value
            Probability= nump.exp(delta / Temp)
            if Probability > 1:
                Probability= 1
            print("p is:  ",Probability)
            r = random.random()
            if Probability > r:
                board = random_move
                current_value = n_value
                print("////////////////")
                print("selected move: ")
                printA(board)
            print("Temp is: ", Temp)
            t += 1

    return "No path found"
def board_exists(board, list_of_plays):
    for i in list_of_plays:
        if board == i.board:
            return True
    return False
def board_is_valid(arr):
    for i in range(0, 5):
        for j in range(0, 5):
            if(arr[i][j]==1 and not ((i+j)%2 ==0)):
                return False
def hill_climbing(board, goal, original_board, counter, temp_count):
    current_value = value_curr(board, goal)
    if current_value == 36:  #  found
        print("goal:  ")
        printA(goal)
        return "Path found "
    elif temp_count == 500:  
        print("goal:")
        printA(goal)
        return "No path found :("
    if not current_value == 36:
        print("attempt mumber =   ", counter)
        print("iteration mumber =   ", temp_count)
        better_moves = []
        equal_moves = []
        moves =optional_moves(board, goal)
        print("current value: ", current_value)
        for move in moves:
            value = value_curr(move, goal)
            if value > current_value:
                better_moves.append(move)
            elif value == current_value:
                equal_moves.append(move)
        print("number of equal moves: ", len(equal_moves))
        print("number of better moves: ", len(better_moves))
        if len(better_moves) > 0:
            selected_move = max(better_moves)
            print("selected move:")
            printA(selected_move)
            print("goal move")
            printA(goal)

            return hill_climbing(selected_move, goal, original_board, counter, temp_count + 1)
        elif len(equal_moves) > 0:
            selected_move = max(equal_moves)
            print("selected move:")
            printA(selected_move)
            print("goal move")
            printA(goal)
            return hill_climbing(selected_move, goal, original_board, counter, temp_count + 1)
    else:
        return hill_climbing(random_board(), goal, original_board, counter + 1, 0, )
    return "No Path"
def not_pina(x, y):
    return not (x==5 or x==0 or y==6)
def optional_moves(a, b):
    moves = []
    for i in range(0, 5):
        for j in range(0, 5):
            if not_pina(i,j):
              if a[i][j] == 1 and not b[i][j]==1:
                    if a[i + 1][j + 1] == 0 :
                        temp=copy.deepcopy(a)
                        temp[i][j] = 0;
                        temp[i+1][j+1]=1;
                        moves.append(temp)
                    if a[i + 1][j - 1] == 0:
                        temp = copy.deepcopy(a)
                        temp[i][j] = 0;
                        temp[i + 1][j -1] = 1;
                        moves.append(temp)
            elif j == 0 :
                    if a[i+1][j + 1] == 0:
                        temp = copy.deepcopy(a)
                        temp[i][j] = 0;
                        temp[i+1 ][j +1] = 1;
                        moves.append(temp)
            elif j==5:
                    if a[i+1][j - 1] == 0:
                        temp = copy.deepcopy(a)
                        temp[i][j] = 0;
                        temp[i+1 ][j -1] = 1;
                        moves.append(temp)


    return moves
def value_curr(a, b):
    value = 0
    for i in range(0, 6):
        for j in range(0, 6):
            if a[i][j]== b[i][j] :
                value += 1

    return value
def random_board():
    counter=0
    array = [
             [ 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0],
             ]
    counter=6
    while counter>0:
        i = random.randint(0, 5)
        j = random.randint(0, 5)
        if (i + j) % 2 == 0:
         array[i][j] = 1
         counter-=1
    return array
def printA(a):
    for row in a:
        for col in row:
            print(col, end=" ")
        print("")
def generate_basic_board():
    array = [
             [ 1, 0, 1, 0, 1, 0],
             [ 0, 1, 0, 1, 0, 1],
             [ 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0],
             [ 0, 0, 0, 0, 0, 0],
             ]
    return array
def FindPlayPath(board, goal, search_method, detail):
    if search_method == 1:
        print(hill_climbing(board, goal, board, 0, 0))

    elif search_method == 2:
        print(S_A(board, goal, board, 1, 10))

    elif search_method == 3:
        print(local_beam(board, goal, 1, 3, detail))

    #elif search_method == 4:


    elif search_method == 5:
        print(a_search(board, goal, 0, detail))







if __name__ == "__main__":
    main()