import pymunk as pm
from pymunk import Vec2d
import pygame
import math
import heapq

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

class Polygon():
    def __init__(self, pos, length, height, space, mass=5.0):
        moment = 1000
        body = pm.Body(mass, moment)
        body.position = Vec2d(*pos)
        shape = pm.Poly.create_box(body, (length, height))
        shape.color = (0, 0, 255)
        shape.friction = 0.5
        shape.collision_type = 2
        space.add(body, shape)
        self.body = body
        self.shape = shape
        wood = pygame.image.load("resources/images/wood.png").convert_alpha()
        wood2 = pygame.image.load("resources/images/wood2.png").convert_alpha()
        rect = pygame.Rect(251, 357, 86, 22)
        self.beam_image = wood.subsurface(rect).copy()
        rect = pygame.Rect(16, 252, 22, 84)
        self.column_image = wood2.subsurface(rect).copy()

    def to_pygame(self, p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y+600)

    def draw_poly(self, element, screen):
        """Draw beams and columns"""
        poly = self.shape
        ps = poly.get_vertices()
        ps.append(ps[0])
        ps = map(self.to_pygame, ps)
        ps = list(ps)
        color = (255, 0, 0)
        pygame.draw.lines(screen, color, False, ps)
        if element == 'beams':
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.beam_image, angle_degrees)
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.
            p = p - offset
            np = p
            screen.blit(rotated_logo_img, (np.x, np.y))
        if element == 'columns':
            p = poly.body.position
            p = Vec2d(*self.to_pygame(p))
            angle_degrees = math.degrees(poly.body.angle) + 180
            rotated_logo_img = pygame.transform.rotate(self.column_image, angle_degrees)
            offset = Vec2d(*rotated_logo_img.get_size()) / 2.
            p = p - offset
            np = p
            screen.blit(rotated_logo_img, (np.x, np.y))

    def move_to_target(self, target_position, grid):
        start = Node((int(self.body.position.x), int(self.body.position.y)))
        end = Node(target_position)
        path = a_star(start, end, grid)
        
        if path:
            for position in path:
                self.body.position = position
