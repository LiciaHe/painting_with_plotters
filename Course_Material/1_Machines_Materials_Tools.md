# Module 1: Everything You Need For Plotter Painting: Machine, Material, and Tools

<img name="1/1_machines_banner.jpg" class="full-width-img">

## Overview
In this module, we will cover:

1. Equipment needed for plotter painting
2. Prepare the machine
3. Prepare the painting environment 
4. Materials and Tools overview 
5. Making Inkwells
6. Stretching watercolor paper
7. [Bonus]: Creating 3D models with Python and Blender

### Plan
This module will be divided into multiple parts. It will contain 2 main videos and a bonus video (subject to change). 


## Part 1: Machines and Preparation

 In this first video, I will cover two major topics, including 1) equipment and 2) preparing the machine/environment.

<div class="youtube-video-container"><iframe src="https://www.youtube.com/embed/PFlyvhYRsTA" class="youtube_video"     loading="lazy"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen></iframe></div>

The video is a detailed walk through of the following topics. I will add additional notes and materials here. 

### Things to consider when finding a plotter for painting 
1. Plotting Angle
    This impacts which material you can use on your plotter. I mainly use watercolor, ink, and liquid acrylic at this moment, so I will only cover flat plotters in the course. But there are many types of plotters waiting for your exploration. 

    Some examples of plotters with different plotting angles: 
    
**Hanging Plotter:**  
    - [Scribit](https://scribit.design/)
    - [Makelangelo](http://www.makelangelo.com/)
    
**Flat Plotters**
    - [Axidraw](https://axidraw.com/)
    - [IDraw](https://idrawpenplotter.com/)
    
**Slanted Plotter**
    - I mostly see vintage plotters with slanted surfaces, such as [this one](    https://commons.wikimedia.org/wiki/File:My_drawing_-_Brighton_Mini_Maker_Fair_2011.jpg)


2. Paper Feeding Mechanism
3. Z-axis space
    [A good question](!Q_12!) about how much you need exactly on the Z-Axis. 

### Plotter I use

I mainly use [AxiDraw/NextDraw](https://axidraw.com/). I discussed the servo motor issue I had and how to solve it. If you are painting with your plotter, I highly recommend you use a durable and sturdy motor for your z-axis. 

### Computers I use 

When I started plotting, I was using my laptop to control the plotter. I switched to raspberry pi later on because of many benefits they provide.

I mentioned a centralized control system for multiple pi and plotters. We might get to this in the future. The high-level idea is to connect all devices to a wifi, and utilize one machine to control other machines (using SSH) . I am running python command to operate the plotters, which made this remote control easier, as I don't need a graphical interface (e.g., inkscape) to operate the machine.  

### 4 principles I use in my studio

These are guidelines I use in my studio, and I learned some of them the hard way. 

**Nothing can move except for the plotter arm**
- Fix paper and ink trays with tape/magnets. I recommend using a magnetic system. 
- Fix and raise plotters with wooden blocks/boards. I've used clamps mostly. 
  - I recently switched to a 3D printed version. [The STL file of the model is stored in the repository.](https://github.com/LiciaHe/painting_with_plotters/tree/master/Projects/1_machines_materials_tools/3D_models/Axidraw_Base_Block_default.stl) 

**Water shouldn't reach electricity**

It's important to protect your machines from water/paint damage. I use a multi-level system:
- Move the plotter up
- Move computer down

**Prepare for paint splashing damage**
Because it will happen. Cover everything, especially the walls. 

**Double check before every plotter run**
- Check if the plotter arm is in its home location 
- Check if the brush/tool is at the correct z-axis height. 




[Let me know if you have any questions](https://www.eyesofpanda.com/project/painting_with_plotters/QA/)

I will see you in the next part! Happy plotting!








