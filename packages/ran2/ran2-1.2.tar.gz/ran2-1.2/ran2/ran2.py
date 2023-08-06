# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 14:15:58 2021

@author: djgates
"""

#import numpy
import numpy as np

class ran2_wrapper():
    def __init__(self, idum):
        self.idum  = idum
        self.idum2 = 123456789
        self.iv    = np.zeros(32,dtype=int)
        self.iy    = 0
    #enddef
    
    def ran2(self):
        #Constants for the function
        IM1  = 2147483563
        IM2  = 2147483399
        IMM1 = IM1-1
        IA1  = 40014
        IA2  = 40692
        IQ1  = 53668
        IQ2  = 52774
        IR1  = 12211
        IR2  = 3791
        NTAB = 32
        NDIV = 1 + int(IMM1//NTAB)
        AM   = 1.0/IM1
        EPS  = 1.0e-15
        RNMX = 1.0-EPS
        
        #Load the mutable static variables 
        idum  = self.idum
        idum2 = self.idum2
        iv    = self.iv
        iy    = self.iy
    
        #Begin the process
        if (idum <= 0):
            idum  = max(-idum,1)
            idum2 = idum
            for j in range(NTAB+8,0,-1):
                k    = int(idum//IQ1)
                idum = IA1*(idum-k*IQ1)-k*IR1
                if (idum < 0):
                    idum  = idum+IM1
                if (j <= NTAB):
                    iv[j-1] = idum
            #enddo
            iy = iv[0]
        #endif
        k    = int(idum//IQ1)
        idum = IA1*(idum-k*IQ1)-k*IR1
        if (idum < 0):
            idum = idum+IM1
        #endif
        k     = int(idum2//IQ2)
        idum2 = IA2*(idum2-k*IQ2)-k*IR2
        if (idum2 < 0):
            idum2 = idum2+IM2
        #endif
        j       = 1+int(iy//NDIV)
        iy      = iv[j-1]-idum2
        iv[j-1] = idum
        if(iy < 1):
            iy = iy+IMM1
        #endif
        ran2 = min(AM*iy,RNMX)
        
        #Update the mutable static variables
        self.idum  = idum
        self.idum2 = idum2
        self.iv    = iv
        self.iy    = iy
        
        return ran2
    #end function ran2
#end def wrapper