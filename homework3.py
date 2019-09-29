#Yiming Chen
#9.24 2019 
#CSCI 561 hw1


import queue
# to do list
# beyond the board
# clean while change target
start = None
end = None


try:
    f = open("input.txt", "r")
    data = f.read()

finally:
    f.close()

# handle data
datalist = data.split('\n')
alg = datalist[0]
W = int(datalist[1].split(' ')[0])
H = int(datalist[1].split(' ')[1])
s_x = int(datalist[2].split(' ')[0])
s_y = int(datalist[2].split(' ')[1])

MAXD = int(datalist[3])
Tar_num = int(datalist[4])
Targ_x = [0]*Tar_num
Targ_y = [0]*Tar_num
for i in range(Tar_num):
    t_data = datalist[i+5].split(' ')
    Targ_x[i] = t_data[0]
    Targ_y[i] = t_data[1]
ele = [[0]*H for i in range(W)]
# wh
w1 = 0
h1 = 0
k1 = Tar_num + 5
while k1 <= Tar_num+4+H:
    ele1 = datalist[k1].split(' ')
    for ele2 in range(W):
        ele[w1][h1] = int(ele1[ele2])
        w1 += 1
        if w1 >= W:
            w1 = 0
            h1 += 1
    k1 += 1

###############################document dealing #################################
# 8 direction
next_step = [[0, 1], [0, -1],
             [1, 1], [1, -1],
             [-1, 1], [-1, -1],
             [1, 0], [-1, 0]
             ]
# structure for Node


class Node:
    def __init__(self, x, y, z, parent, att):
        self.x = x
        self.y = y
        self.z = z
        self.parent = parent
        self.att = att  # -1 cannot find next 0unsearched 1 searched 2 start node 3 target node
        #self.id = str(x) + '|' + str(y)
        if parent != None:  # start node
            g_new = g_func(parent, self)
            self.G = g_new + parent.G
            self.H = h_func(self, end)
            self.F = self.G + self.H
        else:
            self.G = 0
            self.H = 0
            self.F = 0

    def set_parent(self, parent, g_new):
        if parent != None:
            self.G = g_new
            self.F = self.G + self.H
        self.parent = parent

def cmp_z(cx,cy,nx,ny):
    if abs(ele[cx][cy]-ele[nx][ny]) >MAXD:
        return True
    else:
        return False
#######################commom struction ##############################3
# H function ->future cost
def h_func(cur, end):
    #return pow((((cur.x - end.x)**2) + ((cur.y - end.y)**2)), 1/2)
    #new h function
    x_move = abs(cur.x - end.x)
    y_move = abs(cur.y - end.y)
    z_move = abs(cur.z - end.z)
    xy_move = min(x_move,y_move)
    return xy_move *14 + (x_move - xy_move)*10 + (y_move - xy_move)*10 + z_move
# G function -> actually cost

def g_func(node1, node2):
    if abs(node1.x-node2.x) * abs(node1.y - node2.y) == 1:
        return 14 + abs(node1.z - node2.z)
    else:
        return 10 + abs(node1.z - node2.z)
# in open list find the next node


def next_node():
    if len(open_list) == 0:
        #print ("FAIL")
        return Node(-1, -1, -1, None, -1)
    _min = 10000000
    _k = (start.x, start.y)
    for i, j in open_list.items():
        if _min > j.F:
            _min = j.F
            _k = i
    return open_list[_k]



# add the available node to updata list

def add_list(node):
    open_list.pop((node.x, node.y))
    close_list[(node.x, node.y)] = node
    
    for i in range(len(next_step)):
        next_x = node.x + next_step[i][0]
        next_y = node.y + next_step[i][1]
        if next_x < 0 or next_y < 0 or next_x >= W or next_y >=H  :
            continue  # jump out of board
        if cmp_z(next_x,next_y,node.x,node.y):
            continue

        a = Node(next_x, next_y, ele[next_x][next_y], node, 0)
        if (next_x, next_y) == (end.x, end.y):  # find the target
            g_new = g_func(a, node)+node.G
            end.set_parent(node, g_new)
            return True
        if (next_x, next_y) in close_list:
            continue
        if (next_x, next_y) not in open_list:
            open_list[(next_x, next_y)] = a
        else:  # if g is smaller then change it
            t_node = open_list[(next_x, next_y)]
            g_new = g_func(a, node) + node.G
            if g_new < t_node.G:
                t_node.set_parent(node, g_new)

    return False


def find_path(start, end):
    open_list[(start.x, start.y)] = start
    c_node = start
    if(start.x,start.y) == (end.x,end.y):
        return True;
    while not add_list(c_node):
        c_node = next_node()
        if c_node.att == -1:
            # of.write("FAIL")
            return False
    return True

# A*searching ###################################3

def find_BFS_path(start,end):
    que = queue.Queue()
    que.put(start)
    if(start.x,start.y) == (end.x,end.y):
        return True;
    search_list = {}
    search_list[(start.x,start.y)] = start
    search_list[(end.x,end.y)] = end

    while not que.empty():
        cur = que.get()
        cur_x = cur.x
        cur_y = cur.y
        #print ("%d,%d\t",cur_x,cur_y)
        for i in range(len(next_step)):
            #the next step
            next_x = cur_x + next_step[i][0]
            next_y = cur_y + next_step[i][1]
            #check whether it is available 
            if next_x <0 or next_y < 0 or next_x >=W or next_y >=H  :
                continue #jump out of board 
            if cmp_z(next_x,next_y,cur_x,cur_y):
                continue
            
            if (next_x,next_y) == (end.x,end.y):
                end.att = cur.att +1
                end.parent = cur
                return True
            if (next_x,next_y) not in search_list : #no searched before
                a= Node(next_x,next_y,ele[next_x][next_y],cur,cur.att+1)
                search_list[(next_x,next_y)] = a
                que.put(a)
    
    return False

############BFS##################################33
class compare1(object): #compare function to  order the node
    def __init__(self,priority,node):
        self.priority = priority
        self.node = node
    def __lt__(self,other):
        '''
        if self.priority < other.priority:
            return -1
        elif self.priority == other.priority:
            return 0
        else: 
            return 1
        '''
        return self.priority < other.priority

def g_UCS(cx,cy, nx,ny):
    if abs(cx-nx) * abs(cy - ny) == 1:
        return 14
    else:
        return 10


def find_UCS_path(start,end):
    pri_que = queue.PriorityQueue()
    pri_que.put(compare1(1,start))
    searched_list = {}
    searched_list[(start.x,start.y)] = start
    searched_list[(end.x,end.y)] = end
    if(start.x,start.y) == (end.x,end.y):
        return True;
    while not pri_que.empty():
        cur = pri_que.get_nowait().node
        cur_x = cur.x
        cur_y = cur.y
        for i in range(len(next_step)):
            #the next step
            next_x = cur_x + next_step[i][0]
            next_y = cur_y + next_step[i][1]
            #check whether it is available 
            if next_x <0 or next_y < 0 or next_x >=W or next_y >=H :
                continue #jump out of board 
            if cmp_z(cur_x,cur_y,next_x,next_y):
                continue
            if (next_x,next_y) == (end.x,end.y):
                end.att = cur.att +g_UCS(next_x,next_y,end.x,end.y)
                end.parent = cur
                return True
            if (next_x,next_y) not in searched_list : #no searched before
                a= Node(next_x,next_y,ele[next_x][next_y],cur,cur.att + g_UCS(next_x,next_y,cur_x,cur_y))
                searched_list[(next_x,next_y)] = a
                pri_que.put(compare1( a.att, a))
            else : #in searched_list
                if searched_list[(next_x,next_y)].att > cur.att + g_UCS(next_x,next_y,cur_x,cur_y) :
                    searched_list[(next_x,next_y)].att = cur.att + g_UCS(next_x,next_y,cur_x,cur_y)

                
    return False








#####################UCS###########################
def output():
    #of = open("output1.txt","a")
 # output the arry
    global s_flag 
    k = end
    path_que = queue.LifoQueue()
    #path_que.put(k)
    while k != None:
        path_que.put(k)
        #of.write("%d,%d " % (k.x, k.y))
        k = k.parent
    #of.write('\n')
    if s_flag != 0:
            of.write('\n')
            s_flag = 1
    while not path_que.empty():
        w = path_que.get()
        of.write("%d,%d" % (w.x, w.y))
        if not path_que.empty():
            of.write(' ')
    s_flag = 1

    


# output file #################################3
if __name__ == '__main__':
    of = open("output.txt", 'w')
    s_flag = 0
    if alg =="A*":
        for i in range(Tar_num):
            open_list = {}
            close_list = {}
            e_x = int(Targ_x[i])  # this time the target is this one
            e_y = int(Targ_y[i])
            start = Node(s_x, s_y, ele[s_x][s_y], None, 2)
            end = Node(e_x, e_y, ele[e_x][e_y], None, 3)
            if find_path(start, end):
                output()
            else:
                if s_flag != 0:
                    of.write('\n')
                    s_flag = 1
                of.write("FAIL")
                s_flag = 1
        print ("A*")
    elif alg =="BFS":
        for i in range(Tar_num):
            e_x = int(Targ_x[i])  # this time the target is this one
            e_y = int(Targ_y[i])
            start = Node(s_x, s_y, ele[s_x][s_y], None, 0)
            end = Node(e_x, e_y, ele[e_x][e_y], None, 999999)
            if find_BFS_path(start,end):
                output()
            else:
                if s_flag != 0:
                    of.write('\n')
                    s_flag = 1
                of.write("FAIL")
                s_flag = 1
        print("BFS")
    else:
        for i in range(Tar_num):
            e_x = int(Targ_x[i])  # this time the target is this one
            e_y = int(Targ_y[i])
            start = Node(s_x, s_y, 0, None, 2)
            end = Node(e_x, e_y, 99999, None, 3)
            if find_UCS_path(start,end):
                output()
            else:
                if s_flag != 0:
                    of.write('\n')
                    s_flag = 1
                of.write("FAIL")
                s_flag = 1
        print("UCS")

