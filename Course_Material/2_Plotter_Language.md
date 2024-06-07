# 2: The Plotter Language: How to Talk To A Plotter

**Overview:** In this module, I introduce what plotters can do and how to construct instructions for plotters. I discuss two common methods to control an Axidraw plotter, including plotting SVG through the Inkscape plugin, and plotting through pyaxidraw, the Axidraw Python API. 

Learning Objectives: 
1. Understanding the Plotter Language.
2. Observing methods to create SVG files using Inkscape and Adobe Illustrator.
3. Understanding the structure and selected elements of a SVG file.  
4. Constructing simple SVGs manually. 
5. Plotting SVGs through Inkscape plug-in
6. Discussing mixed use of unit 
7. Implementing a Python-based plotter-operating script. 
8. Plotting through Python. 
9Comparing the difference between two methods. 

Link To Materials:
1. Video 
2. Files 

## The Plotter Language

Plotters, regardless of brands and models, can basically only perform 3 actions. They mostly "speak" of a straightforward language. The language is so simple that it only contains three sentences.

1. Go to a location: Given a point (x, y), move the plotter-held tool to this location. i.e., moveto(x,y)
2. Lift the pen/tool: Move the plotter-held tool in the positive Z axis. i.e., penup()
3. Lower the pen: pendown()

Note: penup() and pendown() are controlling plotter movement in the z axis. Some machine might use different syntax: e.g., z(100) to lift the pen to 100% of the full range, z(0) to lower the pen to 0%. 

You can consider the operation of plotters a conversation using this language. Your machine only understands these 3 commands, and you generate your plotter instruction only with these 3 commands. 

To draw a line [pt0,pt1], you would say 
```
move to pt0
lower the pen
move to pt1
lift the pen
```

In a function format: 
```
axidraw.moveto(pt0)
axidraw.pendown()
axidraw.moveto(pt1)
axidraw.penup()
```

Plotter operations requires vector information because of this plotter language. Based on this language, we can also know that 

1. Plotters have no understanding about the tools they are holding. It can be anything. 
2. Plotters have no understanding of their current status, unless you/the operating-software builder intentionally store that. 
3. Plotters do not understand the concept of solid shapes. They move from point to point. 


## Two Ways to Control An Axidraw

There are multiple ways to control an Axidraw. I will introduce 2 methods in this course: 

1. Plotting through a SVG file.  
2. Plotting a Python script. 

Drawing Objective: 
On a 6x6 inch paper with 1 inch margin
1. draw a line that goes from the top left corner to the bottom right corner,
2. draw a 4x4 inch rectangle

### Generating SVG files using vector editing/authoring software

#### Plotting SVG files
##### Plotting with Inkscape
##### Plotting with pyaxidraw 

### Constructing SVG files manually
- Understanding SVG: XML syntax, <svg> attributes. 
- Determine the coordinates of each element

PPI = 96
SVG Size:
- width and Height: 6 x 6 inch (576 px x 576 px) 
- viewBox: 0 0 576 576 #has to be pixel. 
Line:
- inch: [[1,1],[5,5]]
- px:[[96,96],[480,480]]
Rectangle:
- inch: [[1,1],[5,1],[5,5],[1,5]]
- px:[[96,96],[480,96],[480,480],[96,480]]

- Using the <path> element
- Constructing the svg with/without a <g> element (translation)

### Using the pyaxidraw interactive mode
Authoring the init_test.py 
### Manually authoring an instruction
Authoring basic_axidraw_template.py
