import wifi, woezel, system, display

def showmsg(msg):
	display.drawFill(0x000000)
	display.drawText(0,0,msg,0xFFFFFF)

showmsg("WiFi...")
wifi.connect()
status=wifi.wait()


if not status:
	showmsg("WiFi failed")
	time.sleep(1)
	system.launcher()

showmsg("Installing...")

woezel.install("lasertag")

showmsg("Done")
time.sleep(1)

system.launcher()
