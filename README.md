# Potential-Flow-GUI
One of the greatest difficulties in visualizing potential flow is the quick plotting and manipulation of superimposed elementary solutions.  This GUI was created to facilitate the graphing of flow comprised of the elements: uniform crosswind, sources/sinks, vortices, doublets, and corner flow.  The tool is intuitive to use and provides a number of options to produce a saveable custom plot.


  Features include:
  
    Initial prompt to choose a template, either blank or pre-made example.
    
    Streamplot created using the summed velocity field with adjustable variables: stream density, 
    line weight, arrows/size, color, and frame limits.
    
    Dividing streamline created using the zero contour of the stream function.
    
    Selection mode creates a marker on the plot for highlighted elements.  Be advised this requires 
    that the graph be refreshed each time there is a new selection, creating delays while editing.
    
    Add/remove elements with modifiable position and strengths. Note the coordinates of a uniform 
    crosswind determines its direction.
    
    Navigation toolbar has options for plot: reset, pan, zoom to rectangle, and save.
 
 
  Possible/known issues:
  
    Dimensions of Tkinter windows and objects were optimized and tested using resolutions 2560x1440 
    and 1280x800.  Other resolutions have not been tested and may occlude certain items.
    
    The script can run in the most up-to-date native Anaconda environment, other environments may 
    require that modules be imported.  As such, a standalone app or executable was not able to be 
    created using either py2app or pyinstaller due to incompatibility with conda pathing.
    
    The source/sink stream function for the dividing streamline uses atan2(-Y,-X) and thus plots 
    an undesirable horizontal branch cut. The alternative is to have certain dividing streams 
    missing in particular setups.
    
    
For a description of components and their velocities and stream functions, reference:
http://web.mit.edu/16.unified/www/FALL/fluids/Lectures/f15.pdf,
http://web.mit.edu/16.unified/www/FALL/fluids/Lectures/f16.pdf

For corner flow reference:
http://web.stanford.edu/~cantwell/AA200_Course_Material/AA200_Course_Notes/AA200_Ch_10_Elements_of_potential_flow_Cantwell.pdf,   http://web.mit.edu/fluids-modules/www/potential_flows/LecturesHTML/lec1011/node36.html


Questions and feedback? Email alecwmitchell@gmail.com
    
