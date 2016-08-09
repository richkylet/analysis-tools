'''
=== Quantitative FFT ====
> Fast Fourier Transform (FFT) is a 
relatively fast algorithm for calculating 
the discrete Fourier transform (DFT)
of a time-domain signal. 

Here is an example of FFT implementation
while maintaining proper units (normalization), 
including zero padded signals
'''
import matplotlib.pyplot as plt
import numpy as np
import math

#=====  calculate next power of 2 of a var ================
def nextpow2(x):
    return (x-1).bit_length()
    
#===== consider a time-domain signal  ================
# parameters & vars---
Fs    = 50               # [Hz] sampling freq
L     = 500                # len of signal
dt    = 1/float(Fs)       # time step
Nzero = 2**nextpow2(L) # zero pad length
time  = np.arange(0,L)*float(dt)  # time array
freq  = np.linspace(0,Fs,L) # freq vec for non-zero pad signal
freqn = np.linspace(0,Fs,Nzero)# freq vec for zero pad signal

# signal characteristics---
f1 = 5     # fundamental signal
a1 = 10    # fundamental amplitude
f2 = float(f1)/2 # subharmonic signal
a2 = float(a1)/2 # subharmonic amplitude

# voltage signal y ---
y = a1*np.sin(2 * np.pi * f1 * time) + a2*np.sin(2 * np.pi * f2 * time) 

# add zero mean noise to signal---
noise = np.random.normal(0,1,L)
y2 = y+noise

#plot our non-noisey & noisey time-domain signal
fig = plt.figure
plt.subplot(2,1,1)
plt.plot(time, y2,'b-') # signal w\ noise
plt.plot(time, y,'r--') # signal w\o noise
plt.ylabel('voltage(V)')
plt.xlabel('time(seconds)')
plt.show()

#===== frequency domain  ================

# non-noisey signal
Y = np.fft.fft(y)
Y = 2/float(L)*np.abs(Y) # take abs and divide multiply 2/len(signal)

# noisey signal
Y2 = np.fft.fft(y2)
Y2 = 2/float(L)*np.abs(Y2) # take abs and divide multiply 2/len(signal)

# noisey signal, zeropadded
Yn = np.fft.fft(y2,Nzero)
Yn = 2/float(Nzero)*np.abs(Yn) # take abs and divide multiply 2/len(padded signal)

plt.subplot(2,1,2)
plt.plot(freq[0:L/2], Y2[0:L/2], 'r--')
plt.plot(freq[0:L/2], Y[0:L/2], 'b:')
plt.plot(freqn[0:Nzero/2],Yn[0:Nzero/2], 'k-')

plt.ylabel('voltage (|V|)')
plt.xlabel('freq (Hz)')
plt.show()
