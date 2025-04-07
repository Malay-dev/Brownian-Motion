"""
Utility script to generate GIFs demonstrating different Brownian motion scenarios.
This script uses the main application to generate several GIFs with different configurations.
"""

import subprocess
import os

def ensure_directory(directory):
    """Ensure that the specified directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    # Create output directory
    output_dir = "output_gifs"
    ensure_directory(output_dir)
    
    # Configuration for different scenarios
    scenarios = [
        {
            "name": "single_robot",
            "args": ["--robots", "1", "--trails", "--trail-length", "100", "--frames", "300"]
        },
        {
            "name": "multiple_robots",
            "args": ["--robots", "5", "--trails", "--trail-length", "50", "--frames", "300"]
        },
        {
            "name": "no_trails",
            "args": ["--robots", "3", "--frames", "300"]
        },
        {
            "name": "long_trails",
            "args": ["--robots", "2", "--trails", "--trail-length", "500", "--frames", "450"]
        },
        {
            "name": "small_arena",
            "args": ["--width", "400", "--height", "400", "--robots", "3", "--trails", "--frames", "300"]
        }
    ]
    
    # Generate GIFs for each scenario
    for scenario in scenarios:
        output_file = os.path.join(output_dir, f"{scenario['name']}.gif")
        command = ["python", "app.py", "--record", "--output", output_file] + scenario["args"]
        
        print(f"Generating {scenario['name']} GIF...")
        subprocess.run(command)
        print(f"Generated {output_file}")
    
    print("\nAll GIFs generated successfully!")

if __name__ == "__main__":
    main()