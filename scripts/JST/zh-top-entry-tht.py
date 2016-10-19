#!/usr/bin/env python

'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
'''

import sys
import os

output_dir = os.getcwd()

#if specified as an argument, extract the target directory for output footprints
if len(sys.argv) > 1:
    out_dir = sys.argv[1]

    if os.path.isabs(out_dir) and os.path.isdir(out_dir):
        output_dir = out_dir
    else:
        out_dir = os.path.join(os.getcwd(),out_dir)
        if os.path.isdir(out_dir):
            output_dir = out_dir

if output_dir and not output_dir.endswith(os.sep):
    output_dir += os.sep

#import KicadModTree files
sys.path.append(".." + os.sep + "..")
from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

"""
footprint specific details to go here

Datasheet: http://www.jst-mfg.com/product/pdf/eng/eZH.pdf

"""
pitch = 1.50
pincount = range(2, 14)


#FP name strings
part = "B{n:02}B-ZR" #JST part number format string

prefix = "JST_ZH_"
suffix = "_{n:02}x{p:.2f}mm_Straight"

#FP description and tags

if __name__ == '__main__':

    for pins in pincount:
        #calculate fp dimensions
        A = (pins - 1) * pitch
        B = A + 3.0

        #connector thickness
        T = 3.5

        #corners
        x1 = -1.5
        x2 = x1 + B

        x_mid = (x1 + x2) / 2

        y1 = -1.3
        y2 = y1 + T

        #generate the name
        fp_name = prefix + part.format(n=pins) + suffix.format(n=pins, p=pitch)

        footprint = Footprint(fp_name)

        description = "JST ZH series connector, " + part.format(n=pins) + ", top entry type, through hole"

        #set the FP description
        footprint.setDescription(description)

        tags = "connector jst zh tht top vertical 1.50mm"

        #set the FP tags
        footprint.setTags(tags)

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[x_mid,-2.7], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[x_mid,3.7], layer='F.Fab'))

        drill = 0.7

        #generate the pads
        pa = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=1.1, drill=drill, layers=['*.Cu','*.Mask'])

        footprint.append(pa)

        #draw the courtyard
        cy = RectLine(start=[x1,y1],end=[x2,y2],layer='F.CrtYd',width=0.05,offset = 0.5)
        footprint.append(cy)

        #offset the outline around the connector
        off = 0.15

        xo1 = x1 - off
        yo1 = y1 - off

        xo2 = x2 + off
        yo2 = y2 + off

        #thickness of the notches
        notch = 1.5

        #wall thickness of the outline
        wall = 0.6

        #draw the outline of the connector

        footprint.append(RectLine(start=[xo1,yo1],end=[xo2,yo2]))

        outline = [
        {'x': xo1,'y': yo2-wall - 2.15},
        {'x': xo1 + wall,'y': yo2-wall - 2.15},
        {'x': xo1 + wall,'y': yo1+wall},
        {'x': x_mid,'y': yo1+wall},
        ]

        footprint.append(PolygoneLine(polygone=outline))

        footprint.append(PolygoneLine(polygone=outline,x_mirror=x_mid))

        outline2 = [
        {'x': xo1,'y': yo2-wall - 1},
        {'x': xo1 + wall,'y': yo2-wall - 1},
        {'x': xo1 + wall,'y': yo2-wall},
        {'x': x_mid,'y': yo2-wall},
        ]
        footprint.append(PolygoneLine(polygone=outline2))

        footprint.append(PolygoneLine(polygone=outline2,x_mirror=x_mid))

        #Add a model
        footprint.append(Model(filename="Connectors_JST.3dshapes/" + fp_name + ".wrl"))

        #filename
        filename = output_dir + fp_name + ".kicad_mod"
        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
