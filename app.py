import argparse
import pygame
import numpy as np
from brownian_simulation import BrownianSimulator
from robot import Robot

def save_frames_as_gif(frames, filename="brownian_motion.gif", fps=30):
    """Save recorded frames as a GIF file."""
    try:
        import imageio
        
        # Convert pygame surfaces to numpy arrays
        images = []
        for frame in frames:
            # Convert pygame surface to RGB array
            rgb_array = pygame.surfarray.array3d(frame)
            # Swap axes because pygame and imageio use different conventions
            rgb_array = np.transpose(rgb_array, (1, 0, 2))
            images.append(rgb_array)
        
        # Save as GIF
        imageio.mimsave(filename, images, fps=fps)
        print(f"GIF saved as {filename}")
        
    except ImportError:
        print("Error: imageio is required to save GIFs. Install it with 'pip install imageio'.")

def main():
    """Main function to run the Brownian motion simulation."""
    parser = argparse.ArgumentParser(description='Brownian Motion Simulator')
    parser.add_argument('--width', type=int, default=800, help='Width of the arena')
    parser.add_argument('--height', type=int, default=800, help='Height of the arena')
    parser.add_argument('--robots', type=int, default=1, help='Number of robots')
    parser.add_argument('--trails', action='store_true', help='Show trails')
    parser.add_argument('--trail-length', type=int, default=100, help='Length of trails')
    parser.add_argument('--fps', type=int, default=60, help='Frames per second')
    parser.add_argument('--record', action='store_true', help='Record and save as GIF')
    parser.add_argument('--frames', type=int, default=300, help='Number of frames to record')
    parser.add_argument('--output', type=str, default='brownian_motion.gif', help='Output filename for GIF')
    
    args = parser.parse_args()
    
    # Create simulator
    simulator = BrownianSimulator(width=args.width, height=args.height)
    
    # Set initial trail state
    simulator.show_trails = args.trails
    simulator.set_trail_length(args.trail_length)
    
    # Add robots
    for _ in range(args.robots):
        x = args.width // 2 + np.random.randint(-50, 50)
        y = args.height // 2 + np.random.randint(-50, 50)
        radius = np.random.randint(5, 15)
        speed = np.random.uniform(1.5, 3.0)
        color = (
            np.random.randint(100, 255),
            np.random.randint(100, 255),
            np.random.randint(100, 255)
        )
        robot = Robot(x, y, radius=radius, speed=speed, color=color)
        simulator.add_robot(robot)
    
    if args.record:
        # Record frames for GIF
        print(f"Recording {args.frames} frames...")
        frames = simulator.record_frames(args.frames)
        save_frames_as_gif(frames, args.output, args.fps)
    else:
        # Run the simulation
        simulator.run(fps=args.fps)

if __name__ == "__main__":
    main()