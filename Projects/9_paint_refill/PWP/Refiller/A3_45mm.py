'''
An ink refill system that paints with A3 paper and 45mm ink trays.
'''

from refill import InkTray,Inkwell
from ..Util.basic import  convert_unit
class A3_45mm(InkTray):
    full_w = convert_unit(17,"in")
    full_h = convert_unit(11,"in")
    canvas_w=convert_unit(15,"in")
    canvas_h=convert_unit(11,"in")
    ink_box_w=convert_unit(48,"mm")
    ink_box_h=convert_unit(48,"mm")
    m = convert_unit(0.35, 'inch')
    ink_box_ct=5

    tray_w=full_w-canvas_w
    tray_h=full_h

    clean_box_w=tray_w
    clean_box_h=full_h-ink_box_ct*ink_box_h
    skip_clean = False
    alt_trigger_ct=10

    refill_stroke_ct=1
    refill_direction="hor"
    alt_refill_stroke_ct=3
    alt_refill_direction="ver"

    def setup(self):
        '''
        initiate inkwells
        Returns:
        '''
        for i in range(self.ink_box_ct):
            x=self.canvas_w
            y=i*self.ink_box_h
            w=self.ink_box_w
            h=self.ink_box_h
            inkwell=Inkwell(
                bbox=[x,y,w,h],
                alt_trigger_ct=self.alt_trigger_ct,
                margin=self.m
            )
            inkwell.paths=[inkwell.produce_ink_path(
                stroke_ct=self.refill_stroke_ct,
                stroke_direction=self.refill_direction
            )]
            inkwell.alt_paths=[inkwell.produce_ink_path(
                stroke_ct=self.alt_refill_stroke_ct,
                stroke_direction=self.alt_refill_direction
            )]

            self.inkwells.append(inkwell)





