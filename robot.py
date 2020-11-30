class Robot():
    def __init__(self, pos):
        self.status = {
            'can_move_to_child'  : False,
            'can_move_to_trash'  : False,
            'can_move_to_corral' : False
        }
        self.pos = pos
        self.carry_child = False

    def reset_status(self):
        for var in self.status.keys():
            self.status[var] = False

    # Robot Actions Reactive
    def get_trash(self, brd):
        path = brd.get_path_to(self.pos, 3, self.carry_child)
        #print(path)
        if len(path):
            #print('ROBOT:> RECOGIENDO BASURA')
            self.status['can_move_to_trash'] = True
            if len(path) >= 2 and self.carry_child:
                output = brd.move_robot(self.pos, path[0], self.carry_child)
                if output['drop_child']:
                    self.carry_child = False
                output = brd.move_robot(path[0], path[1], self.carry_child)
                if output['drop_child']:
                    self.carry_child = False
                self.pos = path[1]
            else:
                output = brd.move_robot(self.pos, path[0], self.carry_child)
                self.pos = path[0]
                if output['drop_child']:
                    self.carry_child = False
        else:
            self.status['can_move_to_trash'] = False
            #print('ROBOT:> DO NOTHING')
    
    def take_child_to_corral(self, brd):
        path = brd.get_path_to(self.pos, 2, self.carry_child)
        #print(path)
        if len(path):
            #print('ROBOT:> LLEVANDO NIÑO AL CORRAL')
            # Hay camino hacia el corral mas cercano
            self.status['can_move_to_corral'] = True
            if len(path) >= 2:
                # Puedo dar dos pasos
                output = brd.move_robot(self.pos, path[0], self.carry_child)
                if output['drop_child']:
                    self.carry_child = False
                output = brd.move_robot(path[0], path[1], self.carry_child)
                self.pos = path[1]
                if output['drop_child']:
                    self.carry_child = False
            else:
                # Puedo dar solo un paso
                output = brd.move_robot(self.pos, path[0], self.carry_child)
                self.pos = path[0]
                if output['drop_child']:
                    self.carry_child = False
        else:
            # No hay camino hacia un corral
            self.status['can_move_to_corral'] = False
            self.get_trash(brd)

    def seek_child(self, brd):
        path = brd.get_path_to(self.pos, 1, self.carry_child)
        #print(path)
        if len(path):
            #print('ROBOT:> BUSCANDO NIÑO')
            # Hay camino hacia el niño mas cercano
            self.status['can_move_to_child'] = True
            output = brd.move_robot(self.pos, path[0], self.carry_child)
            self.pos = path[0]
            if output['pickup_child']:
                self.carry_child = True
        else:
            # No hay camino hacia el niño mas cercano
            self.status['can_move_to_child'] = False
            self.get_trash(brd)

    def next_action_alter_1(self, brd):
        # Reinicio todas las variables de estado
        self.reset_status()
        
        # Si se me esta llenando el env de basura voy a recoger
        per = brd.dirt_per
        #print('PORCIENTO DE BASURA ' + str(per))
        if per > 50:
            #print('ROBOT:> LIMPIANDO POR EXCESO DE BASURA')
            self.get_trash(brd)

        # Si tengo un niño cargado me intento mover al corral mas cercano
        elif self.carry_child:
            self.take_child_to_corral(brd)
            
        # Si hay niños aun fuera de los corrales intento buscar el niño mas cercano   
        elif brd.remain_childs():
            self.seek_child(brd)

        # EOC recoger la basura restante
        else:
            self.get_trash(brd)

    def next_action_alter_2(self, brd):
        # Reinicio todas las variables de estado
        self.reset_status()

        per = brd.dirt_per

        if self.carry_child:
            if per < 10:
                self.take_child_to_corral(brd)
            else:
                self.get_trash(brd)

        elif brd.remain_childs():
            self.seek_child(brd)

        else:
            self.get_trash(brd) 

    def next_action_alter_3(self, brd):
        # Reinicio todas las variables de estado
        self.reset_status()

        per = brd.dirt_per

        if per > 50:
            self.get_trash(brd)

        if self.carry_child:
            if per < 10:
                self.take_child_to_corral(brd)
            else:
                self.get_trash(brd)

        elif brd.remain_childs():
            self.seek_child(brd)

        else:
            self.get_trash(brd)        

    def __str__(self):
        return str(self.pos)