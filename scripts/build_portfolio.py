# build_portfolio.py

import os
import svgwrite
import argparse
from datetime import datetime


def add_intro(dwg, width, height):
    intro = dwg.g(id="intro")
    intro.add(dwg.rect(insert=(0, 0), size=(width, height), fill="#0d1117"))
    intro.add(dwg.text("Welcome to My GitHub Portfolio!",
                        insert=(width / 2, height / 4),
                        text_anchor="middle",
                        font_size="32px",
                        fill="white"))
    return intro


def embed_snake_svg(dwg, snake_path, width, height):
    with open(snake_path, 'r') as f:
        snake_svg = etree.fromstring(f.read().encode())
        embedded = dwg.g(id="snake")
        embedded.add(dwg.image(href=snake_path, insert=(0, height * 0.3), size=(width, height * 0.3)))
        return embedded


def add_project_showcase(dwg, width, height):
    showcase = dwg.g(id="projects")
    projects = ["Project Alpha", "Project Beta", "Project Gamma"]
    y_start = height * 0.65
    for idx, project in enumerate(projects):
        y = y_start + idx * 30
        showcase.add(dwg.text(f"{project}", insert=(width / 2, y),
                              text_anchor="middle",
                              font_size="20px", fill="lightblue"))
    return showcase


def add_skills_section(dwg, width, height):
    skills = dwg.g(id="skills")
    skills_list = ["Python", "JavaScript", "Git", "Linux"]
    x_start = width / 2 - 100
    y = height - 40
    for i, skill in enumerate(skills_list):
        x = x_start + i * 60
        skills.add(dwg.text(skill, insert=(x, y),
                            font_size="16px", fill="lightgreen"))
    return skills


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contrib", required=True, help="Path to snake contribution SVG")
    parser.add_argument("--output", required=True, help="Output SVG file path")
    args = parser.parse_args()

    width, height = 600, 800
    dwg = svgwrite.Drawing(args.output, size=(f"{width}px", f"{height}px"))

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    dwg.add(add_intro(dwg, width, height))
    dwg.add(embed_snake_svg(dwg, args.contrib, width, height))
    dwg.add(add_project_showcase(dwg, width, height))
    dwg.add(add_skills_section(dwg, width, height))

    dwg.save()
    print(f"SVG saved to {args.output}")


if __name__ == "__main__":
    main()
