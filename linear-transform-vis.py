# Visualizing 2D linear transformations as animated gifs
#
# Created by: Raibatak Das
# Date: Nov 2016
# Last modified: Dec 2016

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# This function assigns a unique color based on position
def colorizer(x, y):
    """
    Map x-y coordinates to a rgb color
    """
    r = min(1, 1-y/3)
    g = min(1, 1+y/3)
    b = 1/4 + x/16
    return (r, g, b)

# To animate the transform, we generate a series of intermediates
# Function to compute all intermediate transforms
def stepwise_transform(a, points, nsteps=30):
    '''
    Generate a series of intermediate transform for the matrix multiplication
      np.dot(a, points) # matrix multiplication
    starting with the identity matrix, where
      a: 2-by-2 matrix
      points: 2-by-n array of coordinates in x-y space 
    returns a (nsteps + 1)x2xn array
    '''
    # create empty array of the right size
    transgrid = np.zeros((nsteps+1,) + np.shape(points))
    for j in range(nsteps+1):
        intermediate = np.eye(2) + j/nsteps*(a - np.eye(2)) # compute intermediate matrix
        transgrid[j] = np.dot(intermediate, points) # apply intermediate matrix transformation
    return transgrid

# Create a series of figures showing the intermediate transforms
def make_plots(transarray, color, outdir="png-frames", figuresize=(4,4), figuredpi=150):
    '''
    Generate a series of png images showing a linear transformation stepwise
    '''
    nsteps = transarray.shape[0]
    ndigits = len(str(nsteps)) # to determine filename padding
    maxval = np.abs(transarray.max()) # to set axis limits
    # create directory if necessary
    import os
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # create figure
    plt.ioff()
    fig = plt.figure(figsize=figuresize, facecolor="w")
    for j in range(nsteps): # plot individual frames
        plt.cla()
        plt.scatter(transarray[j,0], transarray[j,1], s=36, c=color, edgecolor="none")
        plt.xlim(1.1*np.array([-maxval, maxval]))
        plt.ylim(1.1*np.array([-maxval, maxval]))
        plt.grid(True)
        plt.draw()
        # save as png
        outfile = os.path.join(outdir, "frame-" + str(j+1).zfill(ndigits) + ".png")
        fig.savefig(outfile, dpi=figuredpi)
    plt.ion()


steps = 30
plt.figure(figsize=(4, 4), facecolor="w")
plt.grid(True)
plt.axis("equal")
plt.title("Grid test")

# Apply to x-y grid
xvals = np.linspace(-4, 4, 9)
yvals = np.linspace(-3, 3, 7)
xygrid = np.column_stack([[x, y] for x in xvals for y in yvals])
colors = list(map(colorizer, xygrid[0], xygrid[1]))


# Example 1: test
a = np.column_stack([[2, 1], [-1, 1]])
print(a)
uvgrid = np.dot(a, xygrid)
plt.scatter(xygrid[0], xygrid[1], s=36, c=colors, edgecolor="none")
transform = stepwise_transform(a, xygrid, nsteps=steps)
make_plots(transform, colors)


'''
# Example 2: Rotation
theta = np.pi/3 # 60 degree clockwise rotation
a = np.column_stack([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
print(a)
# Generate intermediates
transform = stepwise_transform(a, xygrid, nsteps=steps)
#make_plots(transform, colors)
# see above to create gif
'''

'''
# Example 3: Shear
a = np.column_stack([[1, 0], [2, 1]]) # shear along x-axis
print(a)
# Generate intermediates
transform = stepwise_transform(a, xygrid, nsteps=steps)
#make_plots(transform, colors)
# see above to create gif
'''

'''
# Example 4: Permutation
a = np.column_stack([[0, 1], [1, 0]])
print(a)
# Generate intermediates
transform = stepwise_transform(a, xygrid, nsteps=steps)
make_plots(transform, colors)
# see above to create gif
'''

'''
# Example 5: Projection
a = np.column_stack([[1, 0], [0, 0]])
print(a)
# Generate intermediates
transform = stepwise_transform(a, xygrid, nsteps=steps)
make_plots(transform, colors)
# see above to create gif
'''

# Convert to gif (works on linux/os-x, requires image-magick)
from subprocess import call
call("convert -delay 10 ./png-frames/frame-*.png ./content/animation.gif", shell=True)
# Optional: clean up png files
call("rm -f ./png-frames/*.png", shell=True)