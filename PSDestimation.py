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

def nextpow2(x):
    ''' 
    calculate the next power of 2 of x
    '''
    return (x-1).bit_length()

def time_signal(f0, amp,t):
    '''
    calculate time domain signal w\ and w\o noise
    '''
    # non noisey sigal y 
    y = amp*np.sin(2 * np.pi * f0 * t) # fundamental component
    y = amp/2*np.sin(2 * np.pi * f0/2 * t) + y # subharmonic component
    # add noise to signal ynoise
    noise = np.random.normal(0,.01,len(t))
    ynoise = y + noise
    # plot signal
    fig = plt.figure(1)
    plt.subplot(2,2,1)
    plt.plot(t, y,'b-',linewidth=1.2)
    plt.plot(t, ynoise,'r--',linewidth=1.2)
    plt.xlabel('time')
    plt.ylabel('amp')
    plt.title('Time-domain signal')
    plt.grid()
    plt.show()
    return y, ynoise
    
def freq_spec(y,ynoise,t,Fs):
    '''
    Calculate fft/freqeuncy spectrum
    '''
    freq  = np.linspace(0,Fs,len(t)) # freq vec for non-zero pad signal
    freqn = np.linspace(0,Fs, 2**nextpow2(len(ynoise)))
    # fft of non-noisey signal
    Y = np.fft.fft(y) # fft of y (non-noisey signal)
    Y = np.abs(Y)**2 # 
    Y = (Y/max(Y))# normalize and log scale
    # fft of noisey signal
    Y2 = np.fft.fft(ynoise,2**nextpow2(len(ynoise))) # fft with zero padding to length Nzero
    Y2 = np.abs(Y2) 
    Y2 = Y2/max(Y2) # normalize and log scale
    # plot --------------------
    fig = plt.figure(1)
    plt.subplot(2,2,2)
    plt.plot(freq, Y, 'b-')
    plt.plot(freqn, Y2, 'r--',linewidth=1.2)
    plt.ylabel('Amplitude (norm)')
    plt.xlabel('frequency (Hz)')
    plt.title('Frequency Spectrum')
    plt.grid()
    plt.show()
    plt.xlim([0,Fs/2])
    
def periodogram_spec(y, ynoise, Fs):
    '''
    calculate PSD using method of periodograms
    '''
    # signal w\o noise
    f, Pper_spec = signal.periodogram(y, Fs, 'flattop', scaling='spectrum')
    Pper_spec = Pper_spec/max(Pper_spec) # normalize re max
    # signal w\ noise
    f, Pper_spec2 = signal.periodogram(ynoise, Fs, 'flattop', scaling='spectrum')
    Pper_spec2 = Pper_spec2/max(Pper_spec2) # normalize re max
    # plot ------------
    fig = plt.figure(1)
    plt.subplot(2,2,3)
    plt.semilogy(f, Pper_spec,'b-')
    plt.semilogy(f, Pper_spec2,'r-',linewidth=1.2)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD')
    plt.grid()
    plt.show()
    plt.title('Method of periodograms')
def Welch_spec(y, ynoise, Fs):
    '''
    calculate PSD using Welchs method 
    '''
    # signal w\ noise
    f, Pwelch_spec2 = signal.welch(ynoise, Fs, scaling='spectrum')
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

def PSDexample():
    '''
    main
    '''
    f0 = float(input('Enter center frequency (f0): '))
    amp = float(input('Enter amplitude of f0: '))        
    # paramters
    Fs = 10*f0 # make sure we dont alias
    t = np.arange(0,float(10*f0/2),float(1/Fs))

    # make signal
    y, ynoise = time_signal(f0, amp,t) 
    # take FFT
    freq_spec(y,ynoise,t,Fs)
    # method of periodogram
    periodogram_spec(y, ynoise, Fs)
    # welchs method
    Welch_spec(y, ynoise, Fs)
    
    
PSDexample()
