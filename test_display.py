# https://docs.badge.team/esp32-app-development/api-reference/display/

print('Test: Display')


import display
display.flush()

display.drawFill(0x000000)
display.drawText(10, 10, "LaserTag 2 :D", 0xFFFF00, "permanentmarker22")
display.flush()

display.drawCircle(60, 60, 50, 0, 360, True, 0xFFFFFF)
display.drawCircle(60, 60, 40, 0, 360, True, 0x000000)
display.drawCircle(60, 60, 30, 0, 360, True, 0xFFFFFF)
display.drawCircle(60, 60, 20, 0, 360, True, 0x000000)
display.drawCircle(60, 60, 10, 0, 360, True, 0xFFFFFF)

display.drawLine(1, 1, 100, 100, 0xFFFFFF)
display.drawRect(30, 30, 50, 50, True, 0xFFFFFF)

display.drawText(150,25,"STILL",0xFFFFFF,"Roboto_BlackItalic24")
display.drawText(130,50,"Hacking",0xFFFFFF,"PermanentMarker22")
l = display.getTextWidth("Hacking","PermanentMarker22")
display.drawLine(130, 72, 144 + l, 72, 0xFFFFFF)
display.drawLine(140 + l, 52, 140 + l, 70, 0xFFFFFF)
display.drawText(140,75,"Anyway",0xFFFFFF,"Roboto_BlackItalic24")

display.flush()

print('done')
