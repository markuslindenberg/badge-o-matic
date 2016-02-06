#!/usr/bin/env python3

from flask import Flask, request, make_response, redirect

import logging
import sys

from os import path
from io import BytesIO
import subprocess

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont

from reportlab.lib.units import mm, pica
from reportlab.pdfgen.canvas import Canvas

PRINTER = 'ql700'
MAX_CHARS_PER_LINE = 50

BADGE_W = 150.0 * mm # Variabel
BADGE_H = 62.0 * mm # Fix

MARGIN_L = 3 * mm
MARGIN_R = 3 * mm
MARGIN_T = 2 * mm
MARGIN_B = 2 * mm

ORIGIN_X = MARGIN_L
ORIGIN_Y = MARGIN_B
WIDTH = BADGE_W - (MARGIN_L + MARGIN_R)
HEIGHT = BADGE_H - (MARGIN_T + MARGIN_B)

app = Flask(__name__)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

registerFont(TTFont('LeagueGothic', path.join(path.dirname(__file__), 'fonts/leaguegothic-regular-webfont.ttf')))
registerFont(TTFont('Awesome', path.join(path.dirname(__file__), 'fonts/fontawesome-webfont.ttf')))

@app.route('/print/badge', methods=['POST'])
def badge():
    name = request.form['name'][:MAX_CHARS_PER_LINE] if 'name' in request.form else ''
    name2 = request.form['name2'][:MAX_CHARS_PER_LINE] if 'name2' in request.form else ''
    nick = request.form['nick'][:MAX_CHARS_PER_LINE] if 'nick' in request.form else ''
    community = request.form['community'][:MAX_CHARS_PER_LINE] if 'community' in request.form else ''

    pdf = BytesIO()
    c = Canvas(pdf, pagesize=(BADGE_W, BADGE_H))

    c.translate(ORIGIN_X, ORIGIN_Y)

    ico_center = 7*mm
    offset = HEIGHT+2*mm

    c.setFillGray(0.66)
    c.setFont('Awesome', 42)
    c.drawCentredString(ico_center, offset-42*pica/12, '\uf007')
    c.setFont('Awesome', 38)
    c.drawCentredString(ico_center, offset-(2*42+40)*pica/12, '\uf1fa')
    c.drawCentredString(ico_center, offset-(2*42+2*40)*pica/12, '\uf041')

    txt_start = 15*mm

    c.setFillGray(0.0)
    c.setFont('LeagueGothic', 42)
    c.drawString(txt_start, offset-42*pica/12, name)
    c.drawString(txt_start, offset-2*42*pica/12, name2)
    c.setFont('LeagueGothic', 38)
    c.drawString(txt_start, offset-(2*42+40)*pica/12, nick)
    c.drawString(txt_start, offset-(2*42+2*40)*pica/12, community)

    evt_width = 38*pica/12
    evt_start = WIDTH - evt_width

    img_width = 20*mm
    img_start = evt_start - img_width
    c.drawImage(path.join(path.dirname(__file__), 'images/ffrhein_logo_claim_line_rot.png'), img_start, 0, img_width, HEIGHT, mask=None, preserveAspectRatio=True, anchor='c')

    c.rotate(90)
    c.rect(0, -WIDTH, HEIGHT, evt_width, 0, 1)
    c.setFillGray(1.0)
    c.drawCentredString(HEIGHT/2, -WIDTH+MARGIN_R, 'routing days')  

    c.showPage()
    c.save()
    _print(pdf.getvalue())
    pdf.close()

    # response = make_response('Meh')
    # response.headers['Content-Type'] = 'text/plain'
    # return response
    return redirect('/badge/printing.html')

def _print(pdfdata):
    if app.config['DEBUG']:
        app.logger.info('printing to /tmp/out.pdf')
        open('/tmp/out.pdf', 'wb').write(pdfdata)
    else:
        lpr = subprocess.Popen(['lpr', '-P', PRINTER], stdin=subprocess.PIPE)
        lpr.communicate(pdfdata)

if __name__ == '__main__':
    app.run(debug=True)
