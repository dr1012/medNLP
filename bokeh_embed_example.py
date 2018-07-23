import io

from jinja2 import Template

from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.plotting import figure, output_file
from bokeh.resources import INLINE
from bokeh.util.browser import view

def test_lda_tsne():

    # create some data
    x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
    y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]


    # select the tools we want
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"

    # the red and blue graphs will share this data range
    xr1 = Range1d(start=0, end=30)
    yr1 = Range1d(start=0, end=30)

    # only the green will use this data range
    xr2 = Range1d(start=0, end=30)
    yr2 = Range1d(start=0, end=30)

    # build our figures
    p1 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, plot_width=300, plot_height=300)
    p1.scatter(x1, y1, size=12, color="red", alpha=0.5)


    script, div = components(p1)



    return script, div