#!/usr/bin/env python3

from pyroute2 import IPRoute

from io import BytesIO
import subprocess

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF

PRINTER = 'ql700'

PAGE_W = 112.0 * mm # Variabel
PAGE_H = 62.0 * mm # Fix

MARGIN_L = 3 * mm
MARGIN_R = 3 * mm
MARGIN_T = 2 * mm
MARGIN_B = 2 * mm

ORIGIN_X = MARGIN_L
ORIGIN_Y = MARGIN_B
WIDTH = PAGE_W - (MARGIN_L + MARGIN_R)
HEIGHT = PAGE_H - (MARGIN_T + MARGIN_B)

registerFont(TTFont('LeagueGothic', 'fonts/leaguegothic-regular-webfont.ttf'))

def hello(c, link):
	c.translate(ORIGIN_X, ORIGIN_Y)

	# Draw paragraph
	stylesheet = getSampleStyleSheet()
	style = stylesheet['BodyText']
	style.fontName = 'LeagueGothic'
	style.fontSize = 42
	style.leading = 44

	p = Paragraph('<b>print</b><br/>your<br/><b>badge</b><br/>here', style)
	qr_left = 30*mm
	p_w, p_h = p.wrap(qr_left, HEIGHT)
	p.drawOn(c, 0, 0)


	# Add QR Code
	qr_code = qr.QrCodeWidget(link)
	qr_bounds = qr_code.getBounds()
	qr_width = qr_bounds[2] - qr_bounds[0]
	qr_height = qr_bounds[3] - qr_bounds[1]
	d = Drawing(HEIGHT, HEIGHT, transform=[HEIGHT/qr_width,0,0,HEIGHT/qr_height,0,0])
	d.add(qr_code)
	renderPDF.draw(d, c, qr_left, 0)

	# Draw thin line between text and QR code
	c.line(qr_left, 0, qr_left, HEIGHT)
	c.line(qr_left + HEIGHT, 0, qr_left+HEIGHT, HEIGHT)

	img_left = qr_left + HEIGHT

	# Draw images
	c.drawImage('images/ipv6.jpg', img_left, 0, 20*mm, 1/3 * HEIGHT, mask=None, preserveAspectRatio=True, anchor='c')
	c.drawImage('images/ffrhein_logo_claim_line_rot.png', img_left, 1/3*HEIGHT, 20*mm, 2/3 * HEIGHT, mask=None, preserveAspectRatio=True, anchor='c')

def main():
	pdf = BytesIO()

	# Find all IPv6 addresses with global scope
	ips = [dict(a['attrs'])['IFA_ADDRESS'] for a in IPRoute().get_addr() if a['scope'] == 0 and a['family'] == 10]

	if ips:
		c = Canvas(pdf, pagesize=(PAGE_W, PAGE_H))
		hello(c, 'http://[%s]/badge' % ips[0])
	else:
		# ToDo: Legacy IP bild
		c = Canvas(pdf, pagesize=(PAGE_W, PAGE_H))
		
	c.showPage()
	c.save()
	lpr = subprocess.Popen(['lpr', '-P', PRINTER], stdin=subprocess.PIPE)
	lpr.communicate(pdf.getvalue())
	if lpr.returncode != 0:
		pass

if __name__ == '__main__':
	main()
