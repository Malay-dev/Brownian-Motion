import pygame
import numpy as np
from typing import List
from robot import Robot

class BrownianSimulator:
    def __init__(self, width: int = 800, height: int = 800, background_color: tuple = (255, 255, 255)):
        """
        Initialize the Brownian motion simulator.
        
        Args:
            width (int): Width of the arena
            height (int): Height of the arena
            background_color (tuple): RGB color for the background
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        self.robots = []
        self.show_trails = True
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Brownian Motion Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        
    def add_robot(self, robot: Robot = None):
        """
        Add a robot to the simulation.
        
        Args:
            robot (Robot, optional): Robot to add. If None, creates a robot at the center.
        """
        if robot is None:
            # Default robot at the center of the arena
            x = self.width // 2
            y = self.height // 2
            color = (
                np.random.randint(100, 255),
                np.random.randint(100, 255),
                np.random.randint(100, 255)
            )
            robot = Robot(x, y, color=color)
        
        self.robots.append(robot)
        
    def toggle_trails(self):
        """Toggle trail visibility."""
        self.show_trails = not self.show_trails
        
    def clear_trails(self):
        """Clear all robot trails."""
        for robot in self.robots:
            robot.clear_trail()
            
    def set_trail_length(self, length: int):
        """Set trail length for all robots."""
        for robot in self.robots:
            robot.set_trail_length(length)
            
    def draw(self):
        """Draw the current state of the simulation."""
        # Fill background
        self.screen.fill(self.background_color)
        
        # Draw arena boundary
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, self.height), 2)
        
        # Draw robots and their trails
        for robot in self.robots:
            # Draw trail if enabled
            if self.show_trails and robot.trail:
                # Draw trail with fading opacity
                for i, (trail_x, trail_y) in enumerate(robot.trail):
                    # Calculate opacity based on position in trail (older = more transparent)
                    alpha = int(255 * (i / len(robot.trail)))
                    trail_color = (*robot.color[:3], alpha)
                    trail_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surface, trail_color, (1, 1), 1)
                    self.screen.blit(trail_surface, (trail_x - 1, trail_y - 1))
            
            # Draw robot
            pygame.draw.circle(self.screen, robot.color, (int(robot.x), int(robot.y)), robot.radius)
            
        
        # Draw UI elements
        trail_status = "ON" if self.show_trails else "OFF"
        trail_text = self.font.render(f"Trails: {trail_status} (T to toggle)", True, (0, 0, 0))
        robot_text = self.font.render(f"Robots: {len(self.robots)} (R to add)", True, (0, 0, 0))
        clear_text = self.font.render("C to clear trails", True, (0, 0, 0))
        
        self.screen.blit(trail_text, (10, 10))
        self.screen.blit(robot_text, (10, 40))
        self.screen.blit(clear_text, (10, 70))
        
        # Update display
        pygame.display.flip()
        
    def update(self, delta_time: float = 1.0):
        """
        Update all robots in the simulation.
        
        Args:
            delta_time (float): Time delta for updates
        """
        for robot in self.robots:
            robot.update(self.width, self.height, delta_time)
            
    def run(self, fps: int = 60):
        """
        Run the simulation loop.
        
        Args:
            fps (int): Frames per second for the simulation
        """
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.toggle_trails()
                    elif event.key == pygame.K_r:
                        self.add_robot()
                    elif event.key == pygame.K_c:
                        self.clear_trails()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update simulation
            delta_time = 1.0
            self.update(delta_time)
            
            # Draw current state
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(fps)
            
        pygame.quit()
        
    def record_frames(self, duration: int = 500):
        """
        Record frames for creating a GIF later.
        
        Args:
            duration (int): Number of frames to record
            
        Returns:
            List[pygame.Surface]: List of frames as pygame surfaces
        """
        frames = []
        
        for _ in range(duration):
            # Update simulation
            self.update()
            
            # Draw current state
            self.draw()
            
            # Capture frame
            frame = pygame.Surface((self.width, self.height))
            frame.blit(self.screen, (0, 0))
            frames.append(frame)
            
            # Cap the frame rate
            self.clock.tick(60)
            
        return frames