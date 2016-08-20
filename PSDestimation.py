'''
=== Power spectral density estimation ====
>The power spectrum of a time series x(t) describes the distribution of power 
into frequency components composing that signal. The frequency spectrum X(f) of the 
time series x(t) is calculated by Fourier Transform. 

> A 'Fast Fourier Transform' (FFT) is a 
relatively fast algorithm for calculating 
the discrete Fourier transform (DFT)
of a continuous, discrete-sampled, time series signal. 
Periodogram and Welch's methods are also spectral analysis tools commonly used.

> Welch's method improves upon the periodogram method by reducing noise in 
exchange for reducing the frequency resolution.

>Here are various examples of estimating the power spectral density of a time-
domain signal. 

----------
KTR 2016

'''

#===========================================================
import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import math

plt.close("all")

#=====  calculate next power of 2 of a number x ================
def nextpow2(x):
    ''' 
    calculate the next power of 2 of x
    '''
    return (x-1).bit_length()
    
#===== time series (signal)       ================
'''
Generate some time-domain signal
'''
# parameters & vars---
Fs    = 200               # [Hz] sampling freq
L     = 2000                # len of signal
dt    = 1/float(Fs)       # time step
Nzero = 2**nextpow2(L) # zero pad length
time  = np.arange(0,L)*float(dt)  # time array
freq  = np.linspace(0,Fs,L) # freq vec for non-zero pad signal
freqn = np.linspace(0,Fs,Nzero)# freq vec for zero pad signal
df = freq[1]-freq[0] # step size freq, bin width
dfn = freqn[1]-freqn[0]# step size zero pad len, bin width

# signal characteristics---
f1 = 24     # fundamental signal
a1 = 10      # fundamental amplitude
f2 = float(f1)/2 # subharmonic signal
a2 = float(a1)/2 # subharmonic amplitude

# signal y ---
y = a1*np.sin(2 * np.pi * f1 * time) + a2*np.sin(2 * np.pi * f2 * time) 

# add zero mean noise to signal---
noise = np.random.normal(0,2,L)
y2 = y+noise

#plot our non-noisey & noisey time-domain signal
fig = plt.figure(1)
plt.subplot(2,2,1)
plt.plot(time, y,'b-') # signal w\ noise
plt.plot(time, y2,'r--',linewidth=1.2) # signal w\o noise
plt.ylabel('Amplitude')
plt.xlabel('time (seconds)')
plt.title('Time-domain signal')
plt.grid()
plt.show()
plt.xlim([0,time[round(L/10)] ])


#------------------------------------------
'''
Methods for estimating the power spectral density of a given signal (w\ and w\o 
zero-sum added noise).
---------------------------------------------------------------
'''
#------------------------------------------
#===== 1-D FTT (Power spectrum) ================
'''
Calculate power spectrum using fft (numpy.fft.fft(array,[zeropad_len,axis,norm]))
'''
# fft of non-noisey signal
Y = np.fft.fft(y) # fft of y (non-noisey signal)
Y = np.abs(Y)**2 # 
Y = (Y/max(Y))# normalize and log scale


# fft of noisey signal
Y2 = np.fft.fft(y2,Nzero) # fft with zero padding to length Nzero
Y2 = np.abs(Y2) 
Y2 = Y2/max(Y2) # normalize and log scale
# plot --------------------
fig = plt.figure(1)
plt.subplot(2,2,2)
plt.plot(freq, Y, 'b-')
plt.plot(freqn,Y2, 'r-',linewidth=1.2)
plt.ylabel('Amplitude (norm)')
plt.xlabel('frequency (Hz)')
plt.title('Frequency Spectrum')
plt.grid()
plt.show()
plt.xlim([0,f1*2])



#------------------------------------------
#==== method of periodograms (PSD estimation) ================
'''
Calculate power spectral density using the method of periodograms, compare with 
periodogram method and noisey vs. non-noisey signal:
'''
fig = plt.figure(1)
plt.subplot(2,2,3)
# signal w\o noise
f, Pper_spec = signal.periodogram(y, Fs, 'flattop', scaling='spectrum')
Pper_spec = Pper_spec/max(Pper_spec) # normalize re max

# signal w\ noise
f, Pper_spec2 = signal.periodogram(y2, Fs, 'flattop', scaling='spectrum')
Pper_spec2 = Pper_spec2/max(Pper_spec2) # normalize re max

# plot ------------
plt.semilogy(f, Pper_spec,'b-')
plt.semilogy(f, Pper_spec2,'r-',linewidth=1.2)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD')
plt.grid()
plt.show()
plt.title('Method of periodograms')
plt.xlim([0,f1*2])

#------------------------------------------
#==== Welch's method       ================
'''
Calculate power spectral density using Welch's method, compare with 
periodogram method and noisey vs. non-noisey signal
'''
# signal w\ noise
f, Pwelch_spec2 = signal.welch(y2, Fs, scaling='spectrum')
Pwelch_spec2 = Pwelch_spec2/max(Pwelch_spec2)

# signal w\o noise
f, Pwelch_spec = signal.welch(y, Fs, scaling='spectrum')
Pwelch_spec = Pwelch_spec/max(Pwelch_spec)
# plot
fig = plt.figure(1)
plt.subplot(2,2,4)
plt.semilogy(f, Pwelch_spec2/max(Pwelch_spec2),'r-',linewidth=1.2)
plt.semilogy(f, Pwelch_spec/max(Pwelch_spec)  ,'b-')
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD')
plt.title('Welchs method ')
plt.grid()
plt.show()
plt.xlim([0,f1*2])
