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

# We will use the inkex module with the predefined Effect base class. Essential.
import inkex

from simplestyle import *

# Allow for translation, later
import gettext
_ = gettext.gettext

# To show debugging output
def printDebug(string):
        inkex.debug(_(str(string)))

# To show error to user
def printError(string):
        inkex.errormsg(_(str(string)))

# FUNCTIONS

def deleteGuidesByOrientation(document, orientation):

        # getting the parent's tag of the guides
        namedview = document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]

        # getting all the guides
        children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',namespaces=inkex.NSS)

        # depending on which type of guide to remove, remove them
        if (orientation == 'all'):
                for element in children:
                        namedview.remove(element)
        elif (orientation == 'horizontal'):
                for element in children:
                        if (element.get('orientation') == '0,1'):
                                namedview.remove(element)
        elif (orientation == 'vertical'):
                for element in children:
                        if (element.get('orientation') == '1,0'):
                                namedview.remove(element)

def createGuide(position,orientation,parent):
        # Create a sodipodi:guide node
        inkex.etree.SubElement(parent,'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide',{'position':position,'orientation':orientation})

# Draw series of guides with or without gutter - same function called for columns and rows
def drawDoubleGuides(colsRows, width, gutter, start_pos, has_outer_gutter, orientation, parent):

        # position of guide
        position = start_pos

        # orientation
        if (orientation == "vertical"):
                orient = "1,0"
        elif (orientation == "horizontal"):
                orient = "0,1"
        else:
                printError("orientation is not valid")

        # Draw double guides (or single guides when no gutter)
        # i will have value 0 to colsRows
        for i in range(0, colsRows+1):

                # Draw first guide of gutter
                # don't draw for first gutter if no outer gutter; don't draw if gutter = 0 to avoid duplicated guides
                if not ( i==0 and has_outer_gutter == False) and gutter > 0:

                        if (orientation == "vertical"):
                                first_pos = str(position) + ",0"
                        elif (orientation == "horizontal"):
                                first_pos = "0," + str(position)
                        # draw the guide
                        createGuide(first_pos, orient, parent)
                        # move position
                        position = position + gutter

                # Draw second guide of gutter
                # don't draw for last gutter if no outer gutter; draw even if gutter = 0
                if not ( i==colsRows and has_outer_gutter == False):

                        if (orientation == "vertical"):
                                second_pos = str(position) + ",0"
                        elif (orientation == "horizontal"):
                                second_pos = "0," + str(position)
                        # draw the guide
                        createGuide(second_pos, orient, parent)
                        # move position
                        position = position + width


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
                        action="store", type="string",
                        dest="tab", default="columns",
                        help="")

                # COLUMNS (vertical guides)

                # Define string option "--column_alignment"
                self.OptionParser.add_option('--column_alignment',
                        action = 'store', type = 'string',
                        dest = 'column_alignment', default = 'centered',
                        help = 'Alignment of the columns in relation to the document')

                # Define string option "--column_offset"
                self.OptionParser.add_option('--column_offset',
                        action = 'store', type = 'string',
                        dest = 'column_offset', default = '0',
                        help = 'Offset distance from the left')

                # Define string option "--columns"
                self.OptionParser.add_option('--columns',
                        action = 'store', type = 'string',
                        dest = 'columns', default = 0,
                        help = 'Number of columns')

                # Define string option "--column_width"
                self.OptionParser.add_option('--column_width',
                        action = 'store', type = 'string',
                        dest = 'column_width', default = 0,
                        help = 'Width of each column')

                # Define string option "--column_gutter"
                self.OptionParser.add_option('--column_gutter',
                        action = 'store', type = 'string',
                        dest = 'column_gutter', default = 0,
                        help = 'Spacing between columns')

                # Define string option "--include_outer_col_gutter"
                self.OptionParser.add_option('--include_outer_col_gutter',
                        action = 'store', type = 'inkbool',
                        dest = 'include_outer_col_gutter', default = True,
                        help = 'Include outer gutters (double guides)')

                # Define boolean option "--delete_vert_guides"
                self.OptionParser.add_option('--delete_vert_guides',
                        action = 'store', type = 'inkbool',
                        dest = 'delete_vert_guides', default = False,
                        help = 'Delete existing vertical guides')

                # ROWS (horizontal guides)

                # Define string option "--row_alignment"
                self.OptionParser.add_option('--row_alignment',
                        action = 'store', type = 'string',
                        dest = 'row_alignment', default = 'centered',
                        help = 'Alignment of rows in relation to the document')

                # Define string option "--row_offset"
                self.OptionParser.add_option('--row_offset',
                        action = 'store', type = 'string',
                        dest = 'row_offset', default = '0',
                        help = 'Offset distance from the top')

                # Define string option "--rows"
                self.OptionParser.add_option('--rows',
                        action = 'store', type = 'string',
                        dest = 'rows', default = 0,
                        help = 'Number of rows')

                # Define string option "--row_height"
                self.OptionParser.add_option('--row_height',
                        action = 'store', type = 'string',
                        dest = 'row_height', default = 0,
                        help = 'Width of each row')

                # Define string option "--row_gutter"
                self.OptionParser.add_option('--row_gutter',
                        action = 'store', type = 'string',
                        dest = 'row_gutter', default = 0,
                        help = 'Spacing between rows')

                # Define string option "--include_outer_row_gutter"
                self.OptionParser.add_option('--include_outer_row_gutter',
                        action = 'store', type = 'inkbool',
                        dest = 'include_outer_row_gutter', default = True,
                        help = 'Include outer gutters (double guides)')

                # Define boolean option "--delete_hor_guides"
                self.OptionParser.add_option('--delete_hor_guides',
                        action = 'store', type = 'inkbool',
                        dest = 'delete_hor_guides', default = False,
                        help = 'Delete existing horizontal guides')

        def effect(self):

                # Get script's options value.

                tab = self.options.tab

                # first tab - columns
                col_alignment = self.options.column_alignment
                col_offset = int(self.options.column_offset)
                cols = int(self.options.columns)
                col_width = int(self.options.column_width)
                col_gut = int(self.options.column_gutter)
                has_outer_col_gutter = self.options.include_outer_col_gutter
                delete_hor = self.options.delete_hor_guides

                # second tab - rows
                row_alignment = self.options.row_alignment
                row_offset = int(self.options.row_offset)
                rows = int(self.options.rows)
                row_height = int(self.options.row_height)
                row_gut = int(self.options.row_gutter)
                has_outer_row_gutter = self.options.include_outer_row_gutter
                delete_vert = self.options.delete_vert_guides

                # getting parent tag of the guides
                namedview = self.document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]

                # getting the main SVG document element (canvas)
                svg = self.document.getroot()

                # getting the width and height attributes of the canvas
                canvas_width  = inkex.unittouu(svg.get('width'))
                canvas_height = inkex.unittouu(svg.attrib['height'])

                # total width (columns and gutters)
                # TODO change total col/row width, instead of extra shift later
                total_col_width = cols*col_width + (cols+1)*col_gut

                # total height (rows and gutters)
                total_row_height = rows*row_height + (rows+1)*row_gut

                if (tab == "\"columns\""):

                        # delete existing vertical guides
                        if (delete_vert):
                                deleteGuidesByOrientation(self.document, 'vertical')

                        # Set horizontal starting position (starting position for drawing) depending on grid alignment
                        if (col_alignment == 'left'):
                                hor_start = col_offset

                        if (col_alignment == 'centered'):
                                hor_start = round(canvas_width/2) - round(total_col_width/2) + col_offset
                                # if no outer gutter, move start position
                                if has_outer_col_gutter == False:
                                        hor_start = hor_start + col_gut

                        if (col_alignment == 'right'):
                                hor_start = canvas_width - total_col_width + col_offset
                                # if no outer gutter, move start position
                                if has_outer_col_gutter == False:
                                        hor_start = hor_start + 2*col_gut

                        # create column guides with column_spacings
                        drawDoubleGuides(cols, col_width, col_gut, hor_start, has_outer_col_gutter, "vertical", namedview)

                elif (tab == "\"rows\""):

                        # delete existing horizontal guides
                        if (delete_hor):
                                deleteGuidesByOrientation(self.document, 'horizontal')

                        # Set vertical starting position depending on grid alignment (0,0 is at BOTTOM left of document)
                        if (row_alignment == 'top'):
                                vert_start = round(canvas_height) - total_row_height - row_offset
                                # if no outer gutter, move start position
                                if has_outer_row_gutter == False:
                                        vert_start = vert_start + 2*row_gut

                        if (row_alignment == 'centered'):
                                vert_start = round(canvas_height/2) - round(total_row_height/2) - row_offset
                                # if no outer gutter, move start position
                                if has_outer_row_gutter == False:
                                        vert_start = vert_start + row_gut

                        if (row_alignment == 'bottom'):
                                vert_start =  -row_offset

                        # create row guides (draw bottom up)
                        drawDoubleGuides(rows, row_height, row_gut, vert_start, has_outer_row_gutter, "horizontal", namedview)



# Create effect instance and apply it.
effect = Grid_Maker()
effect.affect()

## end of file grid_maker.py ##
