import pygame
import pymunk as pm
from pymunk import Vec2d
import heapq


pygame.init()
screen = pygame.display.set_mode((1200, 650))
clock = pygame.time.Clock()


space = pm.Space()
space.gravity = (0.0, -700.0)

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def a_star(start, end, grid):
    open_list = []
    closed_list = []
    heapq.heappush(open_list, start)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) - 1) or node_position[1] < 0:
                continue
            if grid[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(node_position, current_node)
            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end.position[0]) ** 2) + ((child.position[1] - end.position[1]) ** 2)
            child.f = child.g + child.h
            if len([i for i in open_list if child == i and child.g > i.g]) > 0:
                continue
            heapq.heappush(open_list, child)

class Bird():
    def __init__(self, distance, angle, x, y, space):
        self.life = 20
        mass = 5
        radius = 12
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        power = distance * 53
        impulse = power * Vec2d(1, 0)
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 0
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def move_to_target(self, target_position, grid):
        start = Node((int(self.body.position.x), int(self.body.position.y)))
        end = Node(target_position)
        path = a_star(start, end, grid)
        if path:
            for position in path:
                self.body.position = position

class Pig():
    def __init__(self, x, y, space):
        self.life = 20
        mass = 5
        radius = 14
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 1
        space.add(body, shape)
        self.body = body
        self.shape = shape

space = pm.Space()
bird = Bird(10, 45, 100, 100, space)
pig = Pig(200, 200, space)

grid = [[0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]]

bird.move_to_target((4, 4), grid)

