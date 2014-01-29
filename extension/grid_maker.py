#!/usr/bin/env python
'''
Grid creator by Samuel Dellicour (www.samplify.be),
heavily based on Guides creator - Copyright (C) 2008 Jonas Termeau - jonas.termeau **AT** gmail.com


## This extension allows you to automatically draw column and row guides in inkscape (including gutters - spacing between columns).

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

# # # extension's begining # # #

# These two lines are only needed if you don't put the script directly into the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
from simplestyle import *

# Allow for translation, later
import gettext
_ = gettext.gettext

# For printing debugging output
def printDebug(string):
        inkex.debug(_(str(string)))

def showError(string):
        inkex.errormsg(_(str(string)))

# FUNCTIONS

# TODO: rewrite functions, check for single/double; add to class ?

def drawColumnGuides(columns,column_width,column_gutter,parent,horizontal_shift=0):

        # vertical guides
        orientation = "1,0"

        for i in range(0,columns+1):

                #draw all left guides of each column
                position1 = str(horizontal_shift + i*(column_gutter+column_width)) + ",0"
                createGuide(position1,orientation,parent)

                #draw all right guides of each column
                position2 = str(horizontal_shift + i*(column_gutter+column_width) + column_gutter) + ",0"
                createGuide(position2,orientation,parent)

def drawRowGuides(rows,row_height,row_gutter,parent,vertical_shift=0):

        # horizontal guides
        orientation = "0,1"

        for i in range(0,rows+1):

                # draw top guide of each row (note: start with "0," - unlike columns)
                position1 =  "0," + str(vertical_shift + i*(row_gutter+row_height))
                createGuide(position1,orientation,parent)

                # draw bottom guide of each row
                position2 = "0," + str(vertical_shift + i*(row_gutter+row_height) + row_gutter)
                createGuide(position2,orientation,parent)

def createGuide(position,orientation,parent):
        # Create a sodipodi:guide node
        inkex.etree.SubElement(parent,'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide',{'position':position,'orientation':orientation})

def deleteAllGuides(document):
        # getting the parent's tag of the guides
        nv = document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]

        # getting all the guides
        children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',namespaces=inkex.NSS)

        # removing each guide
        for element in children:
                nv.remove(element)

# CLASS

class Grid_Maker(inkex.Effect):

        def __init__(self):
                """
                Constructor.
                Defines options of the script.
                """
                # Call the base class constructor.
                inkex.Effect.__init__(self)

                # Define option for the tab.
                self.OptionParser.add_option("--tab",
                        action="store",type="string",
                        dest="tab", default="columns",
                        help="")

                # COLUMNS

                # Define string option "--column_alignment"
                self.OptionParser.add_option('--column_alignment',
                        action = 'store',type = 'string',
                        dest = 'column_alignment',default = 'centered',
                        help = 'Alignment of the columns in relation to the document')

                # Define string option "--column_offset"
                self.OptionParser.add_option('--column_offset',
                        action = 'store',type = 'string',
                        dest = 'column_offset',default = '0',
                        help = 'Offset distance from the left')

                # Define string option "--columns"
                self.OptionParser.add_option('--columns',
                        action = 'store',type = 'string',
                        dest = 'columns',default = 0,
                        help = 'Number of columns')

                # Define string option "--column_width"
                self.OptionParser.add_option('--column_width',
                        action = 'store',type = 'string',
                        dest = 'column_width',default = 0,
                        help = 'Width of each column')

                # Define string option "--column_gutter"
                self.OptionParser.add_option('--column_gutter',
                        action = 'store',type = 'string',
                        dest = 'column_gutter',default = 0,
                        help = 'Spacing between columns')

                # Define boolean option "--delete_existing_guides"
                self.OptionParser.add_option('--delete_existing_guides',
                        action = 'store',type = 'inkbool',
                        dest = 'delete_existing_guides',default = False,
                        help = 'Delete existing guides')

                # ROWS

                # Define string option "--row_alignment"
                self.OptionParser.add_option('--row_alignment',
                        action = 'store',type = 'string',
                        dest = 'row_alignment',default = 'centered',
                        help = 'Alignment of rows in relation to the document')

                # Define string option "--row_offset"
                self.OptionParser.add_option('--row_offset',
                        action = 'store',type = 'string',
                        dest = 'row_offset',default = '0',
                        help = 'Offset distance from the top')

                # Define string option "--rows"
                self.OptionParser.add_option('--rows',
                        action = 'store',type = 'string',
                        dest = 'rows',default = 0,
                        help = 'Number of rows')

                # Define string option "--row_height"
                self.OptionParser.add_option('--row_height',
                        action = 'store',type = 'string',
                        dest = 'row_height',default = 0,
                        help = 'Width of each row')

                # Define string option "--row_gutter"
                self.OptionParser.add_option('--row_gutter',
                        action = 'store',type = 'string',
                        dest = 'row_gutter',default = 0,
                        help = 'Spacing between rows')

                # Define boolean option "--delete_existing_guides"
                self.OptionParser.add_option('--delete_existing_guides2',
                        action = 'store',type = 'inkbool',
                        dest = 'delete_existing_guides2',default = False,
                        help = 'Delete existing guides')

        def effect(self):

                # Get script's options value.

                tab = self.options.tab

                # first tab - columns
                col_alignment = self.options.column_alignment
                col_offset = int(self.options.column_offset)
                cols = int(self.options.columns)
                col_width = int(self.options.column_width)
                col_gut = int(self.options.column_gutter)
                delete_existing = self.options.delete_existing_guides

                # second tab - rows
                row_alignment = self.options.row_alignment
                row_offset = int(self.options.row_offset)
                rows = int(self.options.rows)
                row_height = int(self.options.row_height)
                row_gut = int(self.options.row_gutter)
                delete_existing2 = self.options.delete_existing_guides2

                # getting parent tag of the guides
                nv = self.document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]

                # getting the main SVG document element (canvas)
                svg = self.document.getroot()

                # getting the width and height attributes of the canvas
                canvas_width  = inkex.unittouu(svg.get('width'))
                canvas_height = inkex.unittouu(svg.attrib['height'])

                # total width (columns and gutters)
                total_col_width = cols*col_width + (cols+1)*col_gut

                # total height (rows and gutters)
                total_row_height = rows*row_height + (rows+1)*row_gut

                if (tab == "\"columns\""):

                        # delete existing guides if chosen
                        if (delete_existing):
                                deleteAllGuides(self.document)

                        # Set horizontal shift (starting position for drawing) depending on grid alignment
                        if (col_alignment == 'centered'):

                                hor_start = round(canvas_width/2) - round(total_col_width/2) + col_offset

                        if (col_alignment == 'left'):

                                hor_start = col_offset

                        if (col_alignment == 'right'):

                                hor_start = canvas_width - total_col_width + col_offset

                        # create column guides with column_spacings
                        drawColumnGuides(cols,col_width,col_gut,nv,hor_start)

                elif (tab == "\"rows\""):

                        # delete existing guides if chosen
                        if (delete_existing2):
                                deleteAllGuides(self.document)

                        # Set vertical shift depending on grid alignment (0,0 is at BOTTOM left of document)
                        if (row_alignment == 'top'):

                                vert_start = round(canvas_height) - total_row_height - row_offset

                        if (row_alignment == 'centered'):

                                vert_start = round(canvas_height/2) - round(total_row_height/2) - row_offset

                        if (row_alignment == 'bottom'):

                                vert_start =  -row_offset

                        # create row guides (draw bottom up)
                        drawRowGuides(rows,row_height,row_gut,nv,vert_start)



# Create effect instance and apply it.
effect = Grid_Maker()
effect.affect()

## end of file grid_maker.py ##
