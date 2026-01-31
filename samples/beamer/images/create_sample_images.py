#!/usr/bin/env python3
"""
Create sample images for the Beamer presentation
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_chart():
    """Create a sample chart image"""
    # Create a simple bar chart
    width, height = 400, 300
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Draw bars
    bars = [(50, 200), (100, 150), (150, 180), (200, 120), (250, 160)]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

    for i, ((x, y), color) in enumerate(zip(bars, colors)):
        draw.rectangle([x, y, x+40, 250], fill=color, outline='black')
        # Add value labels
        draw.text((x+10, y-20), str(250-y), fill='black')

    # Add axes
    draw.line([30, 250, 280, 250], fill='black', width=2)  # X-axis
    draw.line([30, 50, 30, 250], fill='black', width=2)   # Y-axis

    # Add title
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    draw.text((150, 20), "Sample Data", fill='black', font=font, anchor='mt')

    img.save('sample_chart.png')
    print("Created sample_chart.png")

def create_diagram1():
    """Create system architecture diagram"""
    width, height = 200, 150
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Draw rectangles for system components
    draw.rectangle([20, 20, 80, 60], fill='#E3F2FD', outline='#1976D2', width=2)
    draw.rectangle([120, 20, 180, 60], fill='#E8F5E8', outline='#388E3C', width=2)
    draw.rectangle([70, 80, 130, 120], fill='#FFF3E0', outline='#F57C00', width=2)

    # Draw arrows
    draw.line([80, 40, 120, 40], fill='black', width=2)
    draw.line([50, 60, 90, 80], fill='black', width=2)
    draw.line([150, 60, 110, 80], fill='black', width=2)

    # Add labels
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 10)
    except:
        font = ImageFont.load_default()

    draw.text((50, 35), "Client", fill='black', font=font, anchor='mm')
    draw.text((150, 35), "Server", fill='black', font=font, anchor='mm')
    draw.text((100, 95), "Database", fill='black', font=font, anchor='mm')

    img.save('diagram1.png')
    print("Created diagram1.png")

def create_diagram2():
    """Create data flow diagram"""
    width, height = 200, 150
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Draw circles for process nodes
    centers = [(50, 75), (100, 40), (100, 110), (150, 75)]
    colors = ['#FFCDD2', '#C5E1A5', '#BBDEFB', '#FFE0B2']

    for (x, y), color in zip(centers, colors):
        draw.ellipse([x-20, y-20, x+20, y+20], fill=color, outline='black', width=2)

    # Draw arrows showing flow
    draw.line([70, 75, 80, 55], fill='black', width=2)
    draw.line([70, 75, 80, 95], fill='black', width=2)
    draw.line([120, 40, 130, 65], fill='black', width=2)
    draw.line([120, 110, 130, 85], fill='black', width=2)

    img.save('diagram2.png')
    print("Created diagram2.png")

def create_diagram3():
    """Create results diagram"""
    width, height = 200, 150
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Draw a simple line graph
    points = [(20, 120), (50, 100), (80, 90), (110, 60), (140, 40), (170, 30)]

    # Draw grid
    for i in range(0, 200, 40):
        draw.line([i, 20, i, 130], fill='#E0E0E0', width=1)
    for i in range(20, 140, 20):
        draw.line([20, i, 180, i], fill='#E0E0E0', width=1)

    # Draw the line
    for i in range(len(points)-1):
        draw.line([points[i][0], points[i][1], points[i+1][0], points[i+1][1]],
                 fill='#2196F3', width=3)

    # Draw points
    for x, y in points:
        draw.ellipse([x-3, y-3, x+3, y+3], fill='#2196F3', outline='black')

    # Draw axes
    draw.line([20, 130, 180, 130], fill='black', width=2)
    draw.line([20, 20, 20, 130], fill='black', width=2)

    img.save('diagram3.png')
    print("Created diagram3.png")

def create_thank_you():
    """Create a thank you image"""
    width, height = 200, 200
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Draw a simple smiley face
    # Face circle
    draw.ellipse([40, 40, 160, 160], fill='#FFD700', outline='#FFA500', width=3)

    # Eyes
    draw.ellipse([70, 70, 90, 90], fill='black')
    draw.ellipse([110, 70, 130, 90], fill='black')

    # Smile
    draw.arc([70, 90, 130, 130], 0, 180, fill='black', width=3)

    # Add text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((100, 170), "Thank You!", fill='black', font=font, anchor='mt')

    img.save('thank_you.png')
    print("Created thank_you.png")

if __name__ == "__main__":
    print("Creating sample images for Beamer presentation...")

    create_sample_chart()
    create_diagram1()
    create_diagram2()
    create_diagram3()
    create_thank_you()

    print("\nAll sample images created successfully!")
    print("Images created:")
    print("- sample_chart.png")
    print("- diagram1.png")
    print("- diagram2.png")
    print("- diagram3.png")
    print("- thank_you.png")
