# -*- coding: utf-8 -*-
import segno
from PIL import Image
import os
import glob
from pathlib import Path
from datetime import datetime
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

COUNT_PER_PAGE = 40
COUNT_PER_LINE = 5

file_paths = glob.glob("./*.txt")
print("target paths: ", file_paths)

now = datetime.now()
target_dir = "{}{}{}_{:0>2d}{:0>2d}{:0>2d}".format(
    now.year, now.month, now.day, now.hour, now.minute, now.second)
print("create base directory for this round: ", target_dir)
os.makedirs(target_dir)


for path in file_paths:
    filename = Path(path).stem
    splitext = filename.split("_")
    target_sub_dir = splitext[0]
    target_count = splitext[1]

    f = open(path, encoding="utf8")
    qrcontent = f.read()
    qrcontent = qrcontent.replace(
        "(01)", "({{:0>{0}d}})".format(len(target_count)))
    print("will generate qrcode for")
    print(qrcontent)
    f.close()

    qrDir = os.path.join(target_dir, filename)
    os.makedirs(qrDir)
    print("create sub directory {} for file {}".format(target_dir, path))

    my_canvas = canvas.Canvas(os.path.join(
        target_dir, "qrcode{}.pdf".format(target_sub_dir)))
    for i in range(0, int(target_count)):
        qrcode = segno.make_qr(qrcontent.format(i+1))
        qrcode_file = "{}/qrcode_{}.svg".format(qrDir, i+1)
        qrcode.save(qrcode_file, scale=1.85)

        drawing = svg2rlg(qrcode_file)
        index = i % COUNT_PER_LINE
        line = i % COUNT_PER_PAGE//COUNT_PER_LINE
        x = 50+index*100
        y = 725-(line * 100)
        print("draw qrcode {} at x:{} y:{}".format(i+1, x, y))
        renderPDF.draw(drawing, my_canvas, x, y)
        if i > 0 and i % COUNT_PER_PAGE == COUNT_PER_PAGE-1:
            print("create a new page in pdf")
            my_canvas.showPage()

    my_canvas.save()
