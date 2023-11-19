import matplotlib.pyplot as plot
import numpy as np
import math

time = np.arange(0, 2.1*math.pi, 0.1)
amp = np.sin(time*2)
plot.plot(time, amp)
plot.title("Sine Wave")
plot.xlabel("Time")
plot.ylabel("Amplitude")
plot.axhline(y=0, color='k')
plot.show()