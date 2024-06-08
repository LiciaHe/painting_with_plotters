# 3: Developing a Plotter Painting Environment in Python

**Overview**: In this module, I describe my target development environment for generative plotter paintings. I explain why I choose Python as the primary language, and demonstrate the process of developing a foundational project management system in Python.  

Learning Objective: 
1. Understanding the development requirements and ideal pipeline for designing generative plotter instruction
2. Observing the design and development process of a foundational project management system. 
3. Familiarize with programming terminologies such as class, array, list, dictionary, random seed.

## An Ideal Development Environment (For Licia)

Primary Goal: 
1. Generating a list of paths. 
2. Visualizing this list of paths. 
3. Using the axidraw-operating script to iterate through this list.

Good to have: 
1. All outputs are stored in a customized location. 
   1. Organized by project, date, and a customized batch name. 
2. Handles basic plotting needs, such as unit convert, paper size, margin, tool management automatically. 
3. Support seeding for randomness. 
4. Can be extended and modified. 

Takeaway: 
1. I need to export my designs to different formats
2. I need a file management system
3. I need a storage/export system for random seed. 

## Why Python? Can I use something else? 
1. File management and generating are easy 
2. Powerful and fast
3. Flexible

Consider:
1. Do you need real-time feedback? 

## Building A Project Management System

### Structures 

PWP (main library)/
    Generator/ # stores file-generating classes  
    Util/      # stores utility & helper functions

project_folder/
    project_0/
        project_0.py # a customized generator
    project_1/
        run.py
        settings.py


output/
    project_0/
        2024-04-12/
            084036/
                random_seed.txt
                084037.svg
                084037.py 
            084037/
                random_seed.txt
                084037.svg
                084037.py
    project_1/
        2025-03-22/
            custom_batch_1/ 
                084036/
                    random_seed.txt
                084037/
                    random_seed.txt
            custom_batch_1/ 
                084036/
                    random_seed.txt
    

### Development Process 
1. mkdir/rmdir (util)
2. init settings and storage generator 
3. extract information from settings (getter/random from range)
4. init storage (export loc, dated folder, time tag)
5. set random seed, export random seed

