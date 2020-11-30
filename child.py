import random

class Child():
    def __init__(self, id, pos):
        self.id  = id
        self.pos = pos
        self.is_carry = False
    
    def gen_trash(self, brd, n, posible_movs, old_pos, new_pos):
        if n <= len(posible_movs):
            # Tengo mas espacios vacios que posibles basuras a generar
            taken_pos = []
            for i in range(n):
                gt = random.randint(0, 1)
                if gt:
                    r_trash_pos = random.randint(0, len(posible_movs)-1)
                    # print(r_trash_pos)
                    if r_trash_pos not in taken_pos:
                        taken_pos.append(r_trash_pos)
                        brd.add_child_trash(posible_movs[r_trash_pos])
            #print('CHILD' + str(old_pos) + ':> MOVING TO ' + str(new_pos) + '-> ' + str(len(taken_pos)) + ' TRASH GENERATED')
        else:
            # Tengo que generar mas basura que espacios vacios
            trh_gen_n = 0
            for pos in posible_movs:
                gt = random.randint(0, 1)
                if gt:
                    trh_gen_n += 1
                    brd.add_child_trash(pos)
            
            #print('CHILD' + self.__str__() + ':> MOVING TO ' + str(self.pos) + '-> ' + str(trh_gen_n) + ' TRASH GENERATED')                


    def gen_trash_alter(self, brd, n, posible_movs, old_pos, new_pos):
        n_trash_gen = random.randint(0, n)
        
        # tengo mas espacios vacios que basuras a generar
        if n_trash_gen <= len(posible_movs):
            taken_pos = [] 
            while n_trash_gen:
                id_trash = random.randint(0, len(posible_movs)-1)
                if id_trash not in taken_pos:
                    taken_pos.append(id_trash)
                    brd.add_child_trash(posible_movs[id_trash])
                    n_trash_gen -= 1
            #print('CHILD' + str(old_pos) + ':> MOVING TO ' + str(new_pos) + '-> ' + str(len(taken_pos)) + ' TRASH GENERATED')
        
        # tengo que generar mas basura que espacios vacios
        else:
            for pos in posible_movs:
                brd.add_child_trash(pos)
            #print('CHILD' + self.__str__() + ':> MOVING TO ' + str(self.pos) + '-> ' + str(len(posible_movs)) + ' TRASH GENERATED')                            


    def move_child(self, brd):
        cuadricule   = brd.get_cuadricule(self.pos)
        adj_childs   = brd.get_childs(cuadricule)
        posible_movs = brd.get_emptys(cuadricule)

        if self.pos in adj_childs:
            adj_childs.remove(self.pos)

        obstacules = brd.get_obstacules(cuadricule)
        m_obst = brd.get_movable_obstacules(obstacules, self.pos)
        
        for pos in m_obst:
            posible_movs.append(pos)

        if len(posible_movs) and not self.is_carry:
            move = random.randint(0, 1)
            if move:
                r_idx = random.randint(0, len(posible_movs)-1)
                n_pos = posible_movs[r_idx]
                brd.move_child(self.pos, n_pos)
                posible_movs.remove(n_pos)
                posible_movs.append(self.pos)
                
                if len(adj_childs) == 0:
                    #print('tiene 0 adj')
                    self.gen_trash(brd, 1, posible_movs, self.pos, n_pos)
                    #self.gen_trash_alter(brd, 1, posible_movs, self.pos, n_pos)

                elif(len(adj_childs) == 1):
                    #print('tiene 1 adj')
                    self.gen_trash(brd, 2, posible_movs, self.pos, n_pos)
                    #self.gen_trash_alter(brd, 3, posible_movs, self.pos, n_pos)

                else:
                    #print('tiene 3 o mas adj')
                    self.gen_trash(brd, 3, posible_movs, self.pos, n_pos)
                    #self.gen_trash_alter(brd, 6, posible_movs, self.pos, n_pos)

                self.pos = n_pos
            
            else:
                pass
                #print('CHILD' + self.__str__() + ':> NOT MOVING')

        else:
            pass
            #print('CHILD' + self.__str__() + ':> NOT MOVING')

    def __str__(self):
        return str(self.pos)