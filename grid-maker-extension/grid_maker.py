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

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
from simplestyle import *

#from xml.etree import ElementTree as ET

# for printing debugging output
import gettext
_ = gettext.gettext

def printDebug(string):
        inkex.debug(_(str(string)))

def showError(string):
        inkex.errormsg(_(str(string)))

def drawColumnGuides(column_number,column_width,column_spacing,parent,horizontal_shift=0):

        # vertical guides
        orientation = "1,0"

        for i in range(0,column_number+1):

                #draw left guide of each column
                position1 = str(horizontal_shift + i*(column_spacing+column_width)) + ",0"
                createGuide(position1,orientation,parent)

                #draw right guide of each column
                position2 = str(horizontal_shift + i*(column_spacing+column_width) + column_spacing) + ",0"
                createGuide(position2,orientation,parent)

def drawRowGuides(row_number,row_height,row_spacing,parent,vertical_shift=0):

        # horizontal guides
        orientation = "0,1"

        for i in range(0,row_number+1):

                #draw top guide of each row (note: start with "0," - unlike columns)
                position1 =  "0," + str(vertical_shift + i*(row_spacing+row_height))
                createGuide(position1,orientation,parent)

                #draw bottom guide of each row
                position2 = "0," + str(vertical_shift + i*(row_spacing+row_height) + row_spacing)
                createGuide(position2,orientation,parent)

def createGuide(position,orientation,parent):
        # Create a sodipodi:guide node
        # (look into inkex's namespaces to find 'sodipodi' value in order to make a "sodipodi:guide" tag)
        # see NSS array in file inkex.py for the other namespaces
        inkex.etree.SubElement(parent,'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide',{'position':position,'orientation':orientation})

def deleteAllGuides(document):
        # getting the parent's tag of the guides
        nv = document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]

        # getting all the guides
        children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',namespaces=inkex.NSS)

        # removing each guides
        for element in children:
                nv.remove(element)

class Grid_Creator(inkex.Effect):

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
                        help = 'Alignment of columns')

                # Define string option "--column_offset"
                self.OptionParser.add_option('--column_offset',
                        action = 'store',type = 'string',
                        dest = 'column_offset',default = '0',
                        help = 'Space between grid and left page border')

                # Define string option "--column_number"
                self.OptionParser.add_option('--column_number',
                        action = 'store',type = 'string',
                        dest = 'column_number',default = 0,
                        help = 'Number of columns')

                # Define string option "--column_width"
                self.OptionParser.add_option('--column_width',
                        action = 'store',type = 'string',
                        dest = 'column_width',default = 0,
                        help = 'Width of each column')

                # Define string option "--column_spacing"
                self.OptionParser.add_option('--column_spacing',
                        action = 'store',type = 'string',
                        dest = 'column_spacing',default = 0,
                        help = 'Spacing between columns (gutter)')

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
                        help = 'Alignment of rows')

                # Define string option "--row_offset"
                self.OptionParser.add_option('--row_offset',
                        action = 'store',type = 'string',
                        dest = 'row_offset',default = '0',
                        help = 'Space between grid and top page border')

                # Define string option "--row_number"
                self.OptionParser.add_option('--row_number',
                        action = 'store',type = 'string',
                        dest = 'row_number',default = 0,
                        help = 'Number of rows')

                # Define string option "--row_height"
                self.OptionParser.add_option('--row_height',
                        action = 'store',type = 'string',
                        dest = 'row_height',default = 0,
                        help = 'Width of each row')

                # Define string option "--row_spacing"
                self.OptionParser.add_option('--row_spacing',
                        action = 'store',type = 'string',
                        dest = 'row_spacing',default = 0,
                        help = 'Spacing between rows (gutter)')

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
                cols = int(self.options.column_number)
                col_width = int(self.options.column_width)
                col_gut = int(self.options.column_spacing)
                delete_existing = self.options.delete_existing_guides

                # second tab - rows
                row_alignment = self.options.row_alignment
                row_offset_from_top = int(self.options.row_offset)
                row_number = int(self.options.row_number)
                row_height = int(self.options.row_height)
                row_gut = int(self.options.row_spacing)
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
                total_row_height = row_number*row_height + (row_number+1)*row_gut

                # row offset from top converted to offset from bottom (origin is at left BOTTOM)
                row_offset = canvas_height - total_row_height - row_offset_from_top

                # getting edges coordinates
                # h_orientation = '0,' + str(round(canvas_width,4))
                # v_orientation = str(round(canvas_height,4)) + ',0'

                if (tab == "\"columns\""):

                        # delete existing guides if chosen
                        if (delete_existing):
                                deleteAllGuides(self.document)

                        # Set horizontal shift depending on grid alignment
                        if (col_alignment == 'centered'):

                                hor_shift = round(canvas_width/2) - round(total_col_width/2)

                        if (col_alignment == 'left'):

                                hor_shift = 0

                        if (col_alignment == 'right'):

                                hor_shift = canvas_width - total_col_width

                        if (col_alignment == 'custom'):

                                hor_shift = col_offset

                        # create column guides with column_spacings
                        drawColumnGuides(cols,col_width,col_gut,nv,hor_shift)

                elif (tab == "\"rows\""):

                        # delete existing guides if chosen
                        if (delete_existing2):
                                deleteAllGuides(self.document)

                        # Set vertical shift depending on grid alignment
                        if (row_alignment == 'centered'):

                                vert_shift = round(canvas_height/2) - round(total_row_height/2)

                        if (row_alignment == 'top'):

                                vert_shift = canvas_height - total_row_height

                        if (row_alignment == 'bottom'):

                                vert_shift = 0

                        if (row_alignment == 'custom'):

                                vert_shift = row_offset

                        # create row guides
                        drawRowGuides(row_number,row_height,row_gut,nv,vert_shift)



# Create effect instance and apply it.
effect = Grid_Creator()
effect.affect()

## end of file grid_maker.py ##
