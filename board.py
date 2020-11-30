import random
from robot import Robot
from child import Child

# (r, k, c, t, o)

class Board():
    def __init__(self, rows, cols, n_childs, dirt_per, obst_per):
        self.rows       = rows
        self.cols       = cols
        self.n_childs   = n_childs
        self.dirt_per   = dirt_per
        self.obst_per   = obst_per
        self.dirs       = [(-1,0), (0,-1), (0,1), (1,0)]

        cells = []
        for i in range(self.rows):
            cells.append([])
            for j in range(self.cols):
                cells[i].append([0,0,0,0,0])

        self.cells = cells

    ##################################
    #           PROPERTIES           #
    ##################################

    def update_trash_per(self):
        self.dirt_per = self.n_dirt * 100 / self.total_empty_spaces

    def is_corral(self, pos):
        return self.cells[pos[0]][pos[1]][2]
    
    def isObst(self, i, j):
        return self.cells[i][j][4] == 1

    def isCorf(self, i, j):
        return self.cells[i][j][2] == 2

    def isChild(self, i, j):
        return self.cells[i][j][1] == 1

    def isEmpty(self, i, j):
        return not any(self.cells[i][j])

    def childCond(self, i, j, carry_child):
        if self.isChild(i, j):
            return carry_child == False
        return True
    
    def get_corrals_full(self):
        n = 0
        for row in self.cells:
            for col in row:
                if col[2] == 2:
                    n += 1
        return n

    def get_rand_tuple(self):
        #c_srt = random.randint(0, self.rows * self.cols - 1)
        #i, j  = int(c_srt / self.rows), c_srt % self.cols
        i = random.randint(0, self.rows-1)
        j = random.randint(0, self.cols-1)
        return (i,j)                    

    def get_robot_pos(self):
        for i, row in enumerate(self.cells):
            for j, elem in enumerate(row):
                if elem[0]:
                    return (i, j)

    def get_empty_spaces(self):
        empty_cells = 0
        for i in self.cells:
            for j in i:
                if not j[4]:
                    empty_cells += 1
        return empty_cells

    def remain_childs(self):
        elem = [col for row in self.cells for col in row if col[1] == 1]
        return len(elem) > 0
    
    def isIn(self, i, j):
        return i >= 0 and j >= 0 and i < self.rows and j < self.cols

    def is_factible(self, start):
        q = []
        v = []
        q.append(start)
        v.append(start)
        empty_cells = self.get_empty_spaces()
        while len(q):
            (r, c) = q.pop(0)
            for dir in self.dirs:
                nr, nc = r + dir[0], c + dir[1]
                if self.isIn(nr, nc) and (nr, nc) not in v and not self.cells[nr][nc][4]:
                    v.append((nr, nc))
                    q.append((nr, nc))
        if len(v) == empty_cells:
            return True
        return False

    def drop_child_in_corral(self, pos):
        self.cells[pos[0]][pos[1]][2] = 2

    def get_cuadricule(self, center_pos):
        cuadricule = []
        for dir in self.dirs:
            nr, nc = center_pos[0] + dir[0], center_pos[1] + dir[1]
            if self.isIn(nr, nc):
                cuadricule.append((nr, nc))
        return cuadricule

    def get_obstacules(self, cuadricule):
        return [cell for cell in cuadricule if self.cells[cell[0]][cell[1]][4] == 1]

    def can_move_obstacule(self, obst_pos, dir):
        nr, nc = obst_pos[0] + dir[0], obst_pos[1] + dir[1] 
        if self.isIn(nr, nc):
            if not any(self.cells[nr][nc]):
                return True
            elif self.cells[nr][nc][4] == 1:
                return self.can_move_obstacule((nr, nc), dir)
            else:
                return False
        else:
            return False

    def get_movable_obstacules(self, obstacules, pos):
        m_obst = []
        for obst in obstacules:
            dir = (obst[0] - pos[0], obst[1] - pos[1])
            # print('DIR ' + str(dir))
            if self.can_move_obstacule(obst, dir):
                m_obst.append(obst)
        return m_obst         

    def get_emptys(self, cuadricule):
        return [cell for cell in cuadricule if not any(self.cells[cell[0]][cell[1]])]
    
    def get_childs(self, cuadricule):
        return [cell for cell in cuadricule if self.cells[cell[0]][cell[1]][1] == 1 and not self.cells[cell[0]][cell[1]][2] == 2]

    ###################################
    #           GENERATION            #
    ###################################

    def add_child_trash(self, pos):
        if not any(self.cells[pos[0]][pos[1]]):
            self.cells[pos[0]][pos[1]][3] = 1
            self.n_dirt += 1
            self.update_trash_per()

    def add_obstacules(self, start, n):
        while n:
            i, j = self.get_rand_tuple()
            if not any(self.cells[i][j]):
                self.cells[i][j][4] = 1
                if self.is_factible(start):
                    n -= 1
                else:
                    self.cells[i][j][4] = 0

    def add_dirt(self, n):
        while n:
            i, j = self.get_rand_tuple()
            if not any(self.cells[i][j]):
                self.cells[i][j][3] = 1
                n -= 1 

    def add_robot(self):
        while True:
            i, j = self.get_rand_tuple()
            if not any(self.cells[i][j]):
                self.cells[i][j][0] = 1
                break
        return Robot((i, j))

    def add_childs(self):
        childs = {}
        n = self.n_childs
        while n:
            i, j = self.get_rand_tuple()
            if not any(self.cells[i][j]):
                self.cells[i][j][1] = 1
                childs[n] = Child(n, (i, j))
                n -= 1
        return childs

    def add_corrals(self, start, n):
        v = []
        q = []
        q.append(start)
        v.append(start)
        while len(q):
            (r, c) = q.pop(0)
            self.cells[r][c][2] = 1
            n -= 1

            if n <= 0:
                break

            for dir in self.dirs:
                nr, nc = dir[0] + r, dir[1] + c
                if self.isIn(nr, nc) and (nr, nc) not in v:
                    q.append((nr, nc))
                    v.append((nr, nc))

    def adjust_child_corrals(self, n_cor_full):
        childs  = []
        corrals = []
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                if col[1]:
                    childs.append((i, j))
                elif col[2]:
                    corrals.append((i, j))

        idx_taken = []
        while True:
            if n_cor_full == 0:
                break

            r_idx = random.randint(0, len(childs)-1)
            if r_idx not in idx_taken:
                idx_taken.append(r_idx)
                child_pos  = childs[r_idx]
                corral_pos = corrals[r_idx]
                self.cells[child_pos[0]][child_pos[1]][1] = 0
                self.cells[corral_pos[0]][corral_pos[1]][2] = 2 
                n_cor_full -= 1

        n = 0
        n_childs = {}
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                if col[1]:
                    n_childs[n] = Child(n, (i, j))
                    n += 1
        self.childs = n_childs        

    def adjust_child_robot(self):
        childs = []
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                if col[1]:
                   childs.append((i,j))
        r = random.randint(0, len(childs)-1)
        child_pos = childs[r]
        self.cells[child_pos[0]][child_pos[1]][1] = 0
        self.robot.carry_child = True

        for i in self.childs.keys():
            if self.childs[i].pos == child_pos:
                self.childs[i].is_carry = True 

    @classmethod
    def gen_brd(cls, rows, cols, childs, dirt_per=30, obst_per=20):
        brd = cls(rows, cols, childs, dirt_per, obst_per)
        i, j = brd.get_rand_tuple()
        brd.add_corrals((i,j), brd.n_childs)
        brd.childs = brd.add_childs()
        n_obst = int(brd.obst_per * (brd.rows * brd.cols - brd.n_childs) / 100)
        # print(n_obst)
        brd.add_obstacules((i, j), n_obst)
        brd.total_empty_spaces = brd.rows * brd.cols - brd.n_childs - n_obst - 1 
        brd.n_dirt = int(brd.dirt_per * (brd.total_empty_spaces) / 100)
        # print(n_dirt)
        brd.add_dirt(brd.n_dirt)
        brd.robot = brd.add_robot()
        return brd

    ###################################
    #        CONTROL FUNCTIONS        #
    ###################################

    def move_obst(self, pos, dir):
        nr, nc = pos[0] + dir[0], pos[1] + dir[1]
        if self.isIn(nr, nc):
            if not any(self.cells[nr][nc]):
                self.cells[pos[0]][pos[1]][4] = 0
                self.cells[nr][nc][4] = 1
                return True
            elif self.cells[nr][nc][4]:
                if self.move_obst((nr, nc), dir):
                    self.cells[pos[0]][pos[1]][4] = 0
                    self.cells[nr][nc][4] = 1
                    return True
                return False
        return False

    def move_robot(self, old_pos, new_pos, carry_child):
        output = {
            'pickup_child' : False,
            'drop_child'   : False
        }
        opos = self.cells[old_pos[0]][old_pos[1]]
        npos = self.cells[new_pos[0]][new_pos[1]]
        
        opos[0] = 0
        npos[0] = 1

        # si hay basura la recojo
        if npos[3]:
            npos[3] = 0
            self.n_dirt -= 1
            self.update_trash_per()

        # si hay niño lo cargo
        elif not carry_child and npos[1]:
            npos[1] = 0
            output['pickup_child'] = True
            # el niño marcado no puede moverse
            for child in self.childs.keys():
                if self.childs[child].pos == new_pos:
                    self.childs[child].is_carry = True

        # si tenia un niño cargado y estoy en un corral vacio suelto al niño
        elif carry_child and npos[2] == 1:
            # poner el corral lleno
            npos[2] = 2
            # quitar el niño del env
            npos[1] = 0
            output['drop_child'] = True

        return output
    
    def move_child(self, old_pos, new_pos):
        opos = self.cells[old_pos[0]][old_pos[1]]
        npos = self.cells[new_pos[0]][new_pos[1]]
        dir  = (new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])

        # si se mueve hacia un objeto moverlo
        if npos[4]:
            self.move_obst(new_pos, dir)

        opos[1] = 0
        npos[1] = 1

    def get_path_to(self, start, targ_id, carry_child):
        cell = self.cells[start[0]][start[1]]
        if cell[0] and cell[1]:
            return [start]
        
        q  = []
        v  = []
        pi = []

        q.append(start)
        v.append(start)
        pi.append((-1, -1))
        while len(q):
            i, j = q.pop(0)
            for dir in self.dirs:
                nr, nc = i + dir[0], j + dir[1]
                if self.isIn(nr, nc) and not (nr, nc) in v:
                    if not self.isObst(nr, nc) and not self.isCorf(nr, nc) and self.childCond(nr, nc, carry_child):
                        q.append((nr, nc))
                        v.append((nr, nc))
                        pi.append((i,j))

                        if self.cells[nr][nc][targ_id] == 1:
                            path = []
                            path.append((nr, nc))
                            while True:
                                row, col = path[-1]
                                idx = v.index((row, col))
                                p = pi[idx]
                                if p == (-1, -1):
                                    path.reverse()
                                    path.pop(0)
                                    return path
                                else:
                                    path.append(p)

        return []
        
    def __iter__(self):
        return iter(self.cells) 

    def __str__(self):
        # return str(self.cells)
        for r in self.cells:
            print()
            for c in r:
                if not any(c):
                    print('  -  ', end='')
                elif c[0]:
                    print('  W  ', end='')
                elif c[1]:
                    print('  K  ', end='')
                elif c[2] == 2:
                    print('  F  ', end='')
                elif c[2] == 1:
                    print('  C  ', end='')
                elif c[4]:
                    print('  #  ', end='')
                elif c[3]:
                    print('  *  ', end='')
        print()
        return ''
    
if __name__ == '__main__':
    brd = Board(5, 5, 3)
    print(brd)
            