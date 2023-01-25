import sys, pygame, math, time, os
import numpy as np
from pygame.locals import*

width = 1920
height = 1020
screen_color = (49, 150, 100)
line_color = (255, 0, 0)


cwd = os.getcwd()
vertices_3D = []
with open(cwd + r"/mesh.csv") as file:
    data=file.readlines()
    for i in data:
            a=i.split(";")
            #print(a)
            vertices_3D.append((float(a[0]),float(a[1]),float(a[2][:-2])))
        
    #print(vertices_3D)

edge_table = []
li = []
with open(cwd + '/file.txt') as file:
    data=file.readline()[1:-1]
    a=data.split(',')
    for i in a:
        b=i.replace("[","").replace("]","").replace(" ","")
        li.append(int(b))

for i in range(len(li)-1):
    if li[i]!=li[i+1]:
        edge_table.append((li[i],li[i+1]))
#print(edge_table)

def rotate(axis, phi : int, vertices : list[int, int, int]):
    match axis.lower():
        case "x":
            matrix = [[1,0,0],[0,math.cos(phi), math.sin(phi)],[0,-math.sin(phi),math.cos(phi)]]
        case "y":
            matrix = [[math.cos(phi),0,-math.sin(phi)],[0,1,0],[math.sin(phi),0,math.cos(phi)]]
    

    result = [[0,0,0] for x,y,z in vertices_3D]
    #matrix = [[1,0,0],[0,math.cos(phi), math.sin(phi)],[0,-math.sin(phi),math.cos(phi)]]
    for i in range(len(vertices)):
        for j in range(len(matrix[0])):
            for k in range(len(matrix)):
                result[i][j] += vertices_3D[i][k] * matrix[k][j]

    #print(result)
    #result = [x+3 for x in result]
    return result
    

#rotate(50,vertices_3D)
def make_2d(li : list[int,int,int]):
    vertices_3D = li
    focal_length = 720
    vertices_2D = []
    for i in vertices_3D:
        x = i[0] * (focal_length/(focal_length+i[2]))
        y = i[1] * (focal_length/(focal_length+i[2]))
        vertices_2D.append((x,y))
    
    vertices_2D = [(x+(width/2),y+(height/2)) for x,y in vertices_2D]
    #print(vertices_2D)
    return vertices_2D


def main():
    screen=pygame.display.set_mode((width,height))
    s = 0
    while(1):
        s += 1
        vertices_2D = make_2d(rotate("x",s,vertices_3D))
        screen.fill(screen_color)
        pygame.display.flip()
        for i in edge_table:
            pygame.draw.line(screen, line_color, vertices_2D[i[0]],vertices_2D[i[1]])
        pygame.display.flip()
        #time.sleep(0.15)

    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
main()