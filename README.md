Inkscape grid maker
===================

This [Inkscape](http://inkscape.org/) extension will generate a grid (guides) with **equal width columns and gutters**, or rows and gutters.

It is an alternative to positioning paths and converting them to guides.

It was derived from the Inkscape Guide Creator extension, for making grids when **designing websites** in Inkscape. The guides are therefore positioned using pixels, and use rounded numbers (they are set on the pixel). Not tested with other units.

Example:

![grid maker in action](readme-img/inkscape-gridmaker.png)

### Features

- Define number of columns, column width and gutter width to generate a grid;
- Gutter width can be set to zero (but this creates double guides, sorry)
- Choose to align the grid in relation to the page: left aligned, centered, right aligned, or left aligned with an offset (a distance from the left border); this offset can be negative;
- Same with rows (horizontal guides)
- Option to delete all existing guides before generating the new guides
- Live preview to test different widths

### How to install the extension

1. Download zip archive from current site (github) to your computer;
2. Unzip (extract) the archive on your computer;
3. Open it. In the folder grid-maker-extension, you wil find two files: **grid_maker.inx** and **grid_maker.py**. Copy these two files into your Inkscape extensions folder:

- on Windows: "C:\Program Files\Inkscape\share\extensions"
- on Linux: " ~/.config/inkscape/extensions" (where "~" is /home/yourusername/)
- on OS X: "/Applications/Inkscape.app/Contents/Resources/extensions" 

Restart or open Inkscape.

### Usage

You will find the Guides Grid Maker under menu **Extensions > Render > Guides grid maker**. (so *not* Guides creator, and *not* Grid).

Change the settings (columns, columns width, etc), you can use the Live preview to preview it. If you're happy with the settings, click Apply before clicking Close.

Note: you can choose to automatically delete all existing guides before applying the new guides.

That's it.


### To do (no promises...)

- when gutter set to zero, there should be single guides, not double guides;
- allow the choice to include (or not) the outer gutters/guides;
- Align grid in relation to a selected bounding box, instead of the whole page ?
- other units than pixels ?
- should the guide be allowed to be on non-rounded positions ? (maybe for print ?)
- merge this extension with the Guides Creator extension ?
- other ideas ?

### Thank you

Thanks to the creator of the [Inkscape Guides Creator](http://code.google.com/p/inkscape-guides-creator/), the extension which I used as a base for this one. Most of the work was already done, I just adapted it to my needs.

### Licence

Licence of the plugin : GPL v2, just like Inkscape