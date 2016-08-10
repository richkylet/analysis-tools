'''
=== Signal Processing of continuous, time-domain signals ====
Signal processing examples

> Fast Fourier Transform (FFT) is a 
relatively fast algorithm for calculating 
the discrete Fourier transform (DFT)
of a continuous, discrete-sampled, time-domain signal. 
Periodogram and Welch's methods are also spectral analysis tools commonly used.

Here is an example of FFT implementation
while maintaining proper units (normalization), method of periodograms, 
and Welch's method

----------
KTR 2016

'''
#===========================================================
import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import math

plt.close("all")

#=====  calculate next power of 2 of a var ================
def nextpow2(x):
    ''' 
    calculate the next power of 2 of x
    '''
    return (x-1).bit_length()
    
#===== time-domain signal       ================
'''
Generate some time-domain signal
'''
# parameters & vars---
Fs    = 50               # [Hz] sampling freq
L     = 390                # len of signal
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
fig = plt.figure(1)
plt.subplot(2,2,1)
plt.plot(time, y2,'b-') # signal w\ noise
plt.plot(time, y,'r--') # signal w\o noise
plt.ylabel('voltage(V)')
plt.xlabel('time(seconds)')
plt.title('Time-domain signal')
plt.grid()
plt.show()


#===== 1-D FTT ================
'''
Take fft of signal, noisey signal, and zero-padded signal
using numpy.fft.fft(array,[zeropad_len,axis,norm])
'''
# fft of non-noisey signal
Y = np.fft.fft(y)
Y = 2/float(L)*np.abs(Y) # take abs and divide multiply 2/len(signal)

# fft of noisey signal
Y2 = np.fft.fft(y2)
Y2 = 2/float(L)*np.abs(Y2) # take abs and divide multiply 2/len(signal)

# # zero-padded fft of noisey signal
# Yn = np.fft.fft(y2,Nzero)
# Yn = 2/float(np.sqrt(L*Nzero))*np.abs(Yn) # take abs and divide multiply 2/len(padded signal)

fig = plt.figure(1)
plt.subplot(2,2,2)
plt.plot(freq[0:L/2], Y[0:L/2], 'b-')
plt.plot(freq[0:L/2], Y2[0:L/2], 'r--')
# plt.plot(freqn[0:Nzero/2],Yn[0:Nzero/2], 'k-')

plt.ylabel('voltage (|V|)')
plt.xlabel('freq (Hz)')
plt.title('Frequency Spectrum')
plt.grid()
plt.show()


#==== method of periodograms ================
'''
Calculate power spectral density using the method of periodograms, compare with 
periodogram method and noisey vs. non-noisey signal:
'''
fig = plt.figure(1)
plt.subplot(2,2,3)
# signal w\ noise
f, Pper_spec = signal.periodogram(y2, Fs, 'flattop', scaling='spectrum')
# signal w\o noise
f, Pper_spec2 = signal.periodogram(y, Fs, 'flattop', scaling='spectrum')
plt.semilogy(f, Pper_spec,'r-')
plt.semilogy(f, Pper_spec2,'b-')
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD')
plt.grid()
plt.show()
plt.title('Method of periodograms')

#==== Welch's method       ================
'''
Calculate power spectral density using Welch's method, compare with 
periodogram method and noisey vs. non-noisey signal
'''
fig = plt.figure(1)
plt.subplot(2,2,4)
# signal w\ noise
f, Pwelch_spec = signal.welch(y2, Fs, scaling='spectrum')
# signal w\o noise
f, Pwelch_spec2 = signal.welch(y, Fs, scaling='spectrum')
plt.semilogy(f, Pwelch_spec,'r--')
plt.semilogy(f, Pwelch_spec2,'b--')
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD')
plt.title('Welchs method ')
plt.grid()
plt.show()