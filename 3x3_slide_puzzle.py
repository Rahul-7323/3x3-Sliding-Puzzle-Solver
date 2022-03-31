class PQueue:
    def __init__(self):
      self.size=0
      # The below is a list of tuples. In every tuple one value 
      # is the element from list and the second value identifies the list.
      self.arr = []

    def isempty(self):
      return True if (self.size == 0) else False
    
    # Heapify element at index i
    def heapify_down(self, i):
      n = self.size
      a = self.arr
      while (i<n):
        ss = l = 2 * i + 1
        r = 2 * i + 2  
        # ss is smaller of left and right child
        if (l<n and r<n and a[l][0] > a[r][0]):
          ss = r 
        if (ss<n and a[ss][0]<a[i][0]):
          a[i], a[ss] = a[ss], a[i]
          i = ss
        else:
          break

    def delete_min(self):
      min = self.arr[0]
      last = self.arr.pop()
      #size of heap after pop operation will reduce by 1
      self.size -= 1
      if (self.size > 0):
        self.arr[0] = last
        self.heapify_down(0)
      return min
    
    # Heapify last element in the heap 
    def heapify_up(self):
      i = self.size - 1
      while (i>0):
        parent = (i-1)//2
        if (self.arr[i][0] < self.arr[parent][0]):
          self.arr[i], self.arr[parent] = self.arr[parent], self.arr[i]
          i = parent
        else:
          break
    
    # Insert to min heap
    def insert_min_heap(self, x):
      self.arr.append(x)
      self.size += 1
      self.heapify_up()


class Board3x3:
    actions = {
        0:[1,3],
        1:[0,2,4],
        2:[1,5],
        3:[0,4,6],
        4:[1,3,5,7],
        5:[2,4,8],
        6:[3,7],
        7:[4,6,8],
        8:[5,7]
    }

    coords = {
        1:(0,0),
        2:(1,0),
        3:(2,0),
        4:(0,1),
        5:(1,1),
        6:(2,1),
        7:(0,2),
        8:(1,2),
        0:(2,2)
    }
    
    solved_state = [1,2,3,4,5,6,7,8,0]

    def __init__(self, board = []):
        if not self.isValidBoard(board):
            raise Exception("Not a valid board")
        self.board = board
        self.position = self.currPos()

    def __str__(self):
        res = '+---+---+---+\n|'
        b = []
        for x in self.board:
            b.append(x) if x != 0 else b.append(" ")
        for i in range(0,3):
            res += ' ' + str(b[i]) + ' |'
        res += '\n+---+---+---+\n|'
        for i in range(3,6):
            res += ' ' + str(b[i]) + ' |'
        res += '\n+---+---+---+\n|'
        for i in range(6,9):
            res += ' ' + str(b[i]) + ' |'
        res += '\n+---+---+---+'
        return res

    def isValidBoard(self,board):
        if (not board) or (len(board) != 9) or (board.count(0) != 1):
            return False
        return True

    def currPos(self):
        return self.board.index(0)

    def validStates(self):
        valid_states = []
        pos = self.position
        for i in self.actions[pos]:
            board_copy = self.board[:]
            (board_copy[i],board_copy[pos]) = (board_copy[pos],board_copy[i])
            valid_states.append(Board3x3(board_copy))
        return valid_states

    def stringify(self):
        return str(self.board)

    def fromString(self,str_board):
        res = list(map(int,str_board.strip('][').split(', ')))
        return Board3x3(res)

    def heuristic(self):
        dist_sum = 0
        c = self.coords
        b = self.board
        for i in range(1,9):
            dist_sum += abs(c[i][0]-c[b[i-1]][0])+abs(c[i][1]-c[b[i-1]][1])
        dist_sum += abs(c[0][0]-c[b[8]][0])+abs(c[0][1]-c[b[8]][1])
        return dist_sum

    def solve_best_first_search(self):
        visited = set()
        parent = {}
        q = PQueue()

        q.insert_min_heap((self.heuristic(),self))
        
        while q:
            curr = q.delete_min()[1]
            print(curr)
            visited.add(curr.stringify())
            if curr.board == self.solved_state:
                break

            for state in curr.validStates():
                if state.stringify() not in visited:
                    parent[state.stringify()] = curr.stringify()
                    q.insert_min_heap((state.heuristic(),state))
        print("Number of visited states:",len(visited))
        current = str(self.solved_state)
        path = []
        start = self.stringify()

        if current in parent.keys():
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            
            print("\n\nThe path:")
            for state in path:
                print(self.fromString(state))
                print()
    
            print("Number of visited states:",len(visited))
            print("Number of moves:",len(path)-1)
        else:
            print("Invalid Board, No solution exists")

    def solve_breadth_first_search(self):
        visited = set()
        parent = {}
        q = []

        q.append(self)
        
        while q:
            curr = q.pop(0)
            print(curr)
            visited.add(curr.stringify())
            if curr.board == self.solved_state:
                break

            for state in curr.validStates():
                if state.stringify() not in visited:
                    parent[state.stringify()] = curr.stringify()
                    q.append(state)
        current = str(self.solved_state)
        path = []
        start = self.stringify()

        if current in parent.keys():
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            
            print("\n\nThe path:")
            for state in path:
                print(self.fromString(state))
                print()
    
            print("Number of visited states:",len(visited))
            print("Number of moves:",len(path)-1)
        else:
            print("Invalid Board, No solution exists")


    def solve_A_star(self):
        visited = set()
        tree = {}
        parent = {}
        q = PQueue()

        q.insert_min_heap((self.heuristic(),0,self))
        
        while q:
            f,g,curr = q.delete_min()
            print(curr)
            curr_str = curr.stringify()
            visited.add(curr_str)
            tree[curr_str] = []
            if curr.board == self.solved_state:
                break

            for state in curr.validStates():
                state_str = state.stringify()
                if state_str not in visited:
                    parent[state_str] = curr_str
                    tree[curr_str].append(state_str)
                    q.insert_min_heap((state.heuristic()+g+1,g+1,state))
        print("Number of visited states:",len(visited))
        current = str(self.solved_state)
        path = []
        start = self.stringify()

        if current in parent.keys():
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            
            print("\n\nThe path:")
            for state in path:
                print(self.fromString(state))
                print()
    
            print("Number of visited states:",len(visited))
            print("Number of moves:",len(path)-1)
        else:
            print("Invalid Board, No solution exists")

board = Board3x3([7,8,1,4,6,2,5,3,0])
#board=Board3x3([3,8,1,4,0,2,6,5,7])

#board.solve_breadth_first_search()
#board.solve_best_first_search()
board.solve_A_star()

