# 4. Authoring Axidraw Instructions

Overview: In this module, we walk through my process for designing and generating plotter instructions. We start by developing a SVG-generating tool that handles the creation, manipulation, and storage of SVG files. Then, we develop a script-generating tool that creates Python scripts for operating the Axidraw plotter. 

Learning Objective:
1. Develop the pipeline for 1) creating designs with simple geometries, 2) export the design to SVG, 3) export the design to Axidraw-operating script. 
2. Understand the following modules/classes in the PWP library: 
   1. SvgGenerator
   2. Path
   3. ScriptGenerator
   4. ScriptWriter
3. Developing a tool/color-management system and split designs by tools. 

## Developing A SVG Generator

- Extract dimensions and convert unit
- Using Beautiful Soup to create a svg 
- Develop a SVG init and saving pipeline 
- Develop a SVG <path> building pipeline. 

## Managing tools and attributes
- making self.tools
- populating tool colors with random color 

## create() and generate()
- Implement create() function and develop generate()
- Making the Path class 

## Developing the ScriptGenerator and ScriptWriter
- init and export 
- process options 
- process path str (unit convert, margin issue)
- putting it together 

## Practice: Inspired by (Des)Ordres by Vera Molnar

Practice inspiration:
(Des)Ordres
Drawing
1974 (made)
https://collections.vam.ac.uk/item/O1193781/desordres-drawing-vera-molnar/desordres-drawing-molnar-vera/?carousel-image=2011EY3129



