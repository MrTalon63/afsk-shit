import wavio
import numpy as np

s = input("Enter your data: ")

def splitEvery(string, splitLength):
	return [string[i:i+splitLength] for i in range(0, len(string), splitLength)]

filename = input("Enter filename(without extension): ")

binout = bin(int.from_bytes(s.encode(), 'big'))
splitout = splitEvery(binout, 2)
print(binout)

frequency_difference = 625
rate = 48000  					 # samples per second, every second 44100 samples are used, for 100ms --> 44100/(1000/100)
T = 1         					 # sample duration for each bit (seconds), can be changed using the ms down below
f1 = 400   						 # sound frequency (Hz) for 00 bit (600Hz)
f2 = f1 + frequency_difference   # sound frequency (Hz) for 01 bit (1000Hz)
f3 = f2 + frequency_difference   # sound frequency (Hz) for 10 bit (1400Hz)
f4 = f3 + frequency_difference   # sound frequency (Hz) for 11 bit (1800Hz)
start_sequence = 1200.0  		 # start frequencies
stop_sequence = 2400.0    		 # stop frequency


ms = 4; #milliseconds between each baud
samples = 48000//(1000//ms)

x = []
l = []

#------------------------------------------------------------------------------
#start sequence with 1800hz
t = np.linspace(0, T, T*rate, endpoint=False)
x.append(np.sin(2*np.pi * start_sequence * t[:samples]))


for i in splitout:
	
	if i == '00':
		x.append(np.sin(2*np.pi * f1 * t[:samples]))
	if i == '01':
		x.append(np.sin(2*np.pi * f2 * t[:samples]))
	if i == '10':
		x.append(np.sin(2*np.pi * f3 * t[:samples]))
	if i == '11':
		x.append(np.sin(2*np.pi * f4 * t[:samples]))


#end sequence with 4000hz
x.append(np.sin(2*np.pi * stop_sequence * t[:samples]))
x.append(np.sin(2*np.pi * stop_sequence * t[:samples]))
x.append(np.sin(2*np.pi * stop_sequence * t[:samples]))
#------------------------------------------------------------------------------

for i in x:
	for j in i:
		l.append(j);

l = np.array(l)

wavio.write(filename+".wav", l, rate, sampwidth=2)