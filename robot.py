import numpy as np
import math
from typing import Tuple, List

class Robot:
    def __init__(self, x: float, y: float, radius: float = 10, speed: float = 2.0, color: Tuple[int, int, int] = (255, 0, 0)):
        """
        Initialize a robot for Brownian motion simulation.
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            radius (float): Radius of the robot
            speed (float): Movement speed of the robot
            color (Tuple[int, int, int]): RGB color of the robot
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = 0  # Direction in radians (0 = right, π/2 = down)
        self.is_rotating = False
        self.rotation_time = 0
        self.rotation_duration = 0
        self.color = color
        self.trail = []  # Store positions for trail display
        self.max_trail_length = 100  # Maximum trail length

    def update(self, arena_width: int, arena_height: int, delta_time: float = 1.0):
        """
        Update robot position based on current state and check for collisions.
        
        Args:
            arena_width (int): Width of the arena
            arena_height (int): Height of the arena
            delta_time (float): Time delta for simulation
        """
        if self.is_rotating:
            # Continue rotation for the set duration
            self.rotation_time += delta_time
            if self.rotation_time >= self.rotation_duration:
                self.is_rotating = False
            else:
                # Rotate at a constant rate
                rotation_speed = np.pi / 32  # Radians per frame
                self.direction += rotation_speed * delta_time
        else:
            # Move forward in the current direction
            dx = self.speed * math.cos(self.direction) * delta_time
            dy = self.speed * math.sin(self.direction) * delta_time
            next_x = self.x + dx
            next_y = self.y + dy
            
            # Check for collision with boundaries
            collision = False
            
            # Check left and right walls
            if next_x - self.radius < 0 or next_x + self.radius > arena_width:
                collision = True
                
            # Check top and bottom walls
            if next_y - self.radius < 0 or next_y + self.radius > arena_height:
                collision = True
                
            if collision:
                self.start_rotation()
            else:
                self.x = next_x
                self.y = next_y
                
                # Add current position to trail
                self.trail.append((int(self.x), int(self.y)))
                # Trim trail if it gets too long
                if len(self.trail) > self.max_trail_length:
                    self.trail.pop(0)
    
    def start_rotation(self):
        """Start rotating in a random direction for a random duration."""
        self.is_rotating = True
        self.rotation_time = 0
        # Random rotation duration between 10 and 30 frames
        self.rotation_duration = np.random.uniform(10, 30)
        
        # Reflect off the wall (with some randomization)
        self.direction = self.direction + np.pi + np.random.uniform(-np.pi/4, np.pi/4)
        
    def set_trail_length(self, length: int):
        """Set the maximum trail length."""
        self.max_trail_length = length
        # Trim existing trail if needed
        while len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
            
    def clear_trail(self):
        """Clear the robot's trail."""
        self.trail = []