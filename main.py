import copy
from board import Board

def run(rows, cols, n_childs, dirt_per, obst_per, t):
    brd    = Board.gen_brd(rows, cols, n_childs, dirt_per, obst_per)
    bot    = brd.robot
    childs = brd.childs    
    print(brd)
    #input()

    n = 100*t
    iter = 0
    t_prime = 0

    while n:
        if brd.dirt_per > 60:
            return 0

        if brd.dirt_per == 0 and brd.get_corrals_full() == n_childs:
            return 1

        # Diferentes Modelos de Comportamiento del Robot
        #bot.next_action_alter_1(brd)
        #bot.next_action_alter_2(brd)
        bot.next_action_alter_3(brd)
        
        for child in childs.keys():
            childs[child].move_child(brd)
        print(brd)

        if t_prime == t:
            #print('ENVIRONMENT CHANGE')
            t_prime = 0
            new_brd = suffle(brd)
            brd     = copy.deepcopy(new_brd)
            bot     = brd.robot
            childs  = brd.childs

        n -= 1
        iter += 1
        t_prime += 1
    
    return 0

def suffle(brd):
    rows       = brd.rows
    cols       = brd.cols
    childs     = brd.n_childs
    dirt_per   = brd.dirt_per
    obst_per   = brd.obst_per
    n_cor_full = brd.get_corrals_full()
    new_brd    =  Board.gen_brd(rows, cols, childs, dirt_per, obst_per)
    new_brd.adjust_child_corrals(n_cor_full)
    
    if brd.robot.carry_child:
        new_brd.adjust_child_robot()

    return new_brd

if __name__ == '__main__':
    samples = {
        0 : [4, 4,  3, 20, 10, 10],
        1 : [5, 6,  4, 25, 15, 10],
        2 : [6, 6,  5, 20, 30, 10],
        3 : [6, 8,  5, 45, 25, 15],
        4 : [7, 5,  6, 30, 25, 20],
        5 : [8, 8,  7, 40, 15, 10],
        6 : [8, 10, 8, 35, 25, 20],
        7 : [9, 8,  7, 25, 35, 15],
        8 : [9, 9,  7, 40, 20, 10],
        9 : [10,10, 8, 45, 25, 20]
    }
    
    results = {}
    for i, smp in samples.items():

        fails   = 0
        success = 0
        
        n = 30
        while n:
            res = run(smp[0], smp[1], smp[2], smp[3], smp[4], smp[5])
            if res:
                success += 1
            else:
                fails += 1
            
            n -= 1
        print('--- Sample_'+str(i) + ' ---')
        print('Success: ' + str(success))
        print('Fails:   ' + str(fails))
        results[i] = (success, fails)
        
        #print()
        #print('Press any key for next sample')
        #input()
    print(results)