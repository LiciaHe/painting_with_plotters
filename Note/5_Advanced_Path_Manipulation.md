### 5. Advanced Path Manipulation for Plotter Painting
Definition:
line, path 
cut vs split 

1. Cut paths by distance
   - cut a line (by getting pt using perc/dist)
   - split a line by dist/perc (sections to be shorter than a given value)
   - Annotate a path (create uniform polygon)
3. cut a path 
   - split_path_by_dist (make line segments shorter than a given length)
   - cut_path_into_lines 
   - cut_path_into paths 
   
2. Polygon Boolean Operation and Hatch 
   - pyclipper library https://pypi.org/project/pyclipper/
   - nested path test (svg)
      https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule
   - boolean operation 
   - optional (offset)
   - Hatch:
     - bounding box and format 
     - create 2 bounding boxes 
     - create lines within the box 
     - rotate lines 
     - cut lines using pyclipper

3. Drawing Curves
   3. Intro to cubic bezier curve 
   4. by segment 
   5. approximate and create segment


