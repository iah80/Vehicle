def save(path,lst):
    with open(path,"w+") as f:
        for coor in lst:
            x,y = coor
            x = x/1916
            y = y/912
            f.write("{} {}\n".format(x,y))

# l = [[1583,357],[6,357],[1550,784],[6,784]]
# l = [[1583,200],[6,200],[1550,784],[6,784]]
l = [[1106,142],[796,142],[1623,611],[861,624]]
path = r"E:\python\Nhom15\resource\polygon.txt"
save(path,l)
