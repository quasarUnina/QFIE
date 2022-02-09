from math import sin, cos, radians, pi
from Backend import compute_current
import os
import  sys


class Quantum_Control():
    def __init__(self, theta_0, omega_0, T, t, g, qfie):
        self.theta = theta_0
        self.dtheta = omega_0
        self.points = [(self.theta, self.dtheta)]
        self.T = T
        self.t = t
        self.qfie = qfie
        self.g = g
        

    def recomputeAngle(self, plot_histo=False, draw_qc=False):
        
        if self.dtheta > 2 :
            self.dtheta = self.dtheta % 2
        if self.dtheta <-2 :
            self.dtheta = self.dtheta % (-2)
        if self.theta > 8 :
            self.theta = self.theta % 8
        if self.theta <-8 :
            self.theta = self.theta % (-8)
        self.qfie.build_inference_qc({'theta':self.theta, 'omega':self.dtheta}, draw_qc=draw_qc)

        current = self.qfie.execute('qasm_simulator', 8000, plot_histo=plot_histo)[0]    
        print('I = ',current)
        l = 12
        tau = 100
        m = 1
        
        if self.g == True:
            theta_new = self.theta + self.dtheta *self.t + ((3* tau*100/(l*l))*current-(3*32/2)*cos(self.theta*pi/4)) *(self.t*self.t/2)
            omega_new = self.dtheta + ((3*tau*100/(l*l))*current-(3*32/2)*cos(self.theta*pi/4)) * self.t
        else: 
            theta_new = self.theta + self.dtheta *self.t + ((3* tau/(l*l))*current) *(self.t*self.t/2)
            omega_new = self.dtheta + ((3*tau/(l*l))*current) * self.t
        
        
        self.theta, self.dtheta = theta_new, omega_new
        print('theta_new =', theta_new, 'omega_new =', omega_new)
        self.points.append((theta_new, omega_new))

        
    def update(self,plot_histo, draw_qc):
        i=0
        while len(self.points)<=self.T:
            print('Call n. ', i)
            self.recomputeAngle(plot_histo=plot_histo, draw_qc=draw_qc)
            i+=1
        return self.points
    

    
#_______________________________________________________________________________________________________________________________#    
    
class Classical_Control():
    def __init__(self, theta_0, omega_0, T, t, g, cfie):
        self.theta = theta_0
        self.dtheta =  omega_0
        self.points = [(self.theta, self.dtheta)]
        self.T = T
        self.t = t
        self.cfie = cfie
        self.g = g
        
    def recomputeAngle(self):
        if self.dtheta > 2 :
            self.dtheta = self.dtheta % 2
        if self.dtheta <-2 :
            self.dtheta = self.dtheta % (-2)
        if self.theta > 8 :
            self.theta = self.theta % 8
        if self.theta <-8 :
            self.theta = self.theta % (-8)    
        
        self.cfie.input['theta']=self.theta
        self.cfie.input['omega']=self.dtheta
        self.cfie.compute()
        current = self.cfie.output['current']
        print('I = ',current)
        
        l = 12
        tau = 100
        m = 1
        if self.g == True:
            theta_new = self.theta + self.dtheta *self.t + ((3* tau*100/(l*l))*current-(3*32/2)*cos(self.theta*pi/4)) *(self.t*self.t/2)
            omega_new = self.dtheta + ((3*tau*100/(l*l))*current-(3*32/2)*cos(self.theta*pi/4)) * self.t
        else: 
            theta_new = self.theta + self.dtheta *self.t + ((3* tau/(l*l))*current) *(self.t*self.t/2)
            omega_new = self.dtheta + ((3*tau/(l*l))*current) * self.t
        
        
        self.theta, self.dtheta = theta_new, omega_new
        print('theta_new =', theta_new, 'omega_new =', omega_new)
        self.points.append((theta_new, omega_new))

        
    def update(self):
        i=0
        while len(self.points)<=self.T:
            print('Call n. ', i)
            i+=1
            self.recomputeAngle()
        return self.points