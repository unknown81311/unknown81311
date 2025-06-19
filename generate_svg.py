# generate_svg.py
import os
import svgwrite

# Get GitHub username from environment variable
github_username = os.getenv("GITHUB_ACTOR", "Unknown User")

# Create an SVG file
svg = svgwrite.Drawing(filename="github_username.svg", size=(300, 100))
svg.add(svg.text(github_username, insert=(10, 60), fill="black", font_size="30"))
svg.save()

print(f"SVG created for GitHub username: {github_username}")
