import time
import pyfldigi

c = pyfldigi.Client()
time.sleep(1)
c.main.send('SOS')
time.sleep(2)
lorems = ["Lorem ipsum dolor sit amet,",
          "consectetur adipiscing elit,",
          "sed do eiusmod tempor incididunt",
          "ut labore et dolore magna aliqua."]

for lorem in lorems:
    c.main.send(lorem, block=True, timeout=100)

time.sleep(10)
# c.main.tx()
# c.text.add_tx('SOS')
# time.sleep(5)

print(str(c.txmonitor.history))
