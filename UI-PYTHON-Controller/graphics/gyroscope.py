import math
import pygame
import numpy as np
from scipy.spatial.transform import Rotation

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotate(self, angle_x, angle_y, angle_z):
        rotation_matrix_x = np.array([[1, 0, 0],
                                      [0, np.cos(angle_x), -np.sin(angle_x)],
                                      [0, np.sin(angle_x), np.cos(angle_x)]])
        rotation_matrix_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                                      [0, 1, 0],
                                      [-np.sin(angle_y), 0, np.cos(angle_y)]])
        rotation_matrix_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                                      [np.sin(angle_z), np.cos(angle_z), 0],
                                      [0, 0, 1]])
        
        rotated_point = np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, [self.x, self.y, self.z])))
        return Point(rotated_point[0], rotated_point[1], rotated_point[2])

    def perspective_projection(self, distance):
        return Point(self.x * distance / (self.z + distance), self.y * distance / (self.z + distance), self.z)

class Gyroscope(pygame.sprite.Sprite):
    def __init__(self, distance=200):
        super().__init__()
        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()

        self.point_top_left = Point(-distance, 0, -distance)
        self.point_top_right = Point(distance, 0, -distance)
        self.point_bottom_left = Point(-distance, 0, distance)
        self.point_bottom_right = Point(distance, 0, distance)

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))

    def rotate(self, angle_x, angle_y, angle_z):
        self.angle_x += angle_x
        self.angle_y += angle_y
        self.angle_z += angle_z

    def get_rotated_points(self):
        rotated_top_left = self.point_top_left.rotate(self.angle_x, self.angle_y, self.angle_z)
        rotated_top_right = self.point_top_right.rotate(self.angle_x, self.angle_y, self.angle_z)
        rotated_bottom_left = self.point_bottom_left.rotate(self.angle_x, self.angle_y, self.angle_z)
        rotated_bottom_right = self.point_bottom_right.rotate(self.angle_x, self.angle_y, self.angle_z)
        return rotated_top_left, rotated_top_right, rotated_bottom_left, rotated_bottom_right
    

    def render(self):
        self.image.fill((0, 0, 0, 0))
        rotated_top_left, rotated_top_right, rotated_bottom_left, rotated_bottom_right = self.get_rotated_points()

        # Ajout de la perspective
        distance = 500  # Distance du point de fuite
        perspective_top_left = rotated_top_left.perspective_projection(distance)
        perspective_top_right = rotated_top_right.perspective_projection(distance)
        perspective_bottom_left = rotated_bottom_left.perspective_projection(distance)
        perspective_bottom_right = rotated_bottom_right.perspective_projection(distance)

        pygame.draw.line(self.image, (255, 255, 0),
                         (self.WIDTH // 2 + perspective_top_left.x, self.HEIGHT // 2 + perspective_top_left.y), 
                         (self.WIDTH // 2 + perspective_top_right.x, self.HEIGHT // 2 + perspective_top_right.y), 5)
        pygame.draw.line(self.image, (0, 0, 255),
                         (self.WIDTH // 2 + perspective_top_right.x, self.HEIGHT // 2 + perspective_top_right.y), 
                         (self.WIDTH // 2 + perspective_bottom_right.x, self.HEIGHT // 2 + perspective_bottom_right.y), 3)
        pygame.draw.line(self.image, (0, 255, 0), 
                         (self.WIDTH // 2 + perspective_bottom_right.x, self.HEIGHT // 2 + perspective_bottom_right.y), 
                         (self.WIDTH // 2 + perspective_bottom_left.x, self.HEIGHT // 2 + perspective_bottom_left.y), 2)
        pygame.draw.line(self.image, (255, 0, 0), 
                         (self.WIDTH // 2 + perspective_bottom_left.x, self.HEIGHT // 2 + perspective_bottom_left.y), 
                         (self.WIDTH // 2 + perspective_top_left.x, self.HEIGHT // 2 + perspective_top_left.y), 3)


    def update(self, key_dict, fps, *_):
        angle = (75*math.pi/360)/fps
        # z
        if key_dict[pygame.K_w]:
            self.rotate(0, 0, angle)
        elif key_dict[pygame.K_c]:
            self.rotate(0, 0, -angle)

        # y
        if key_dict[pygame.K_LEFT]:
            self.rotate(0, angle, 0)
        elif key_dict[pygame.K_RIGHT]:
            self.rotate(0, -angle, 0)

        # x
        if key_dict[pygame.K_UP]:
            self.rotate(-angle, 0, 0)
        elif key_dict[pygame.K_DOWN]:
            self.rotate(angle, 0, 0)


        self.render()
