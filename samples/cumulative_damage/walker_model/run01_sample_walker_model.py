# ______          _           _     _ _ _     _   _      
# | ___ \        | |         | |   (_) (_)   | | (_)     
# | |_/ / __ ___ | |__   __ _| |__  _| |_ ___| |_ _  ___ 
# |  __/ '__/ _ \| '_ \ / _` | '_ \| | | / __| __| |/ __|
# | |  | | | (_) | |_) | (_| | |_) | | | \__ \ |_| | (__ 
# \_|  |_|  \___/|_.__/ \__,_|_.__/|_|_|_|___/\__|_|\___|
# ___  ___          _                 _                  
# |  \/  |         | |               (_)                 
# | .  . | ___  ___| |__   __ _ _ __  _  ___ ___         
# | |\/| |/ _ \/ __| '_ \ / _` | '_ \| |/ __/ __|        
# | |  | |  __/ (__| | | | (_| | | | | | (__\__ \        
# \_|  |_/\___|\___|_| |_|\__,_|_| |_|_|\___|___/        
#  _           _                     _                   
# | |         | |                   | |                  
# | |     __ _| |__   ___  _ __ __ _| |_ ___  _ __ _   _ 
# | |    / _` | '_ \ / _ \| '__/ _` | __/ _ \| '__| | | |
# | |___| (_| | |_) | (_) | | | (_| | || (_) | |  | |_| |
# \_____/\__,_|_.__/ \___/|_|  \__,_|\__\___/|_|   \__, |
#                                                   __/ |
#                                                  |___/ 
#														  
# MIT License
# 
# Copyright (c) 2019 Probabilistic Mechanics Laboratory
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

""" Walker model sample 
"""

import numpy as np
import pandas as pd
import tensorflow as tf

import matplotlib.pyplot as plt

import sys
sys.path.append('../../../')
from pinn.layers.physics import WalkerModel
# =============================================================================
# Functions
# =============================================================================
def create_model(Co, m , batch_input_shape, myDtype):
    wmLayer = WalkerModel(input_shape = batch_input_shape, dtype = myDtype)
    wmLayer.build(input_shape = batch_input_shape)
    wmLayer.set_weights([np.asarray([Co,m], dtype = wmLayer.dtype)])
    wmLayer.trainable = False
    
    model = tf.keras.Sequential()
    model.add(wmLayer)        
    return model

def walker(dK,R,gamma,Co,m): # implementation of the layer in matrix form for comparison purposes
    C = Co/((1-R)**(m*(1-gamma)))
    da = C*(dK**m)
    return da
#--------------------------------------------------------------------------
if __name__ == "__main__":
    myDtype = tf.float32  # defining type for the layer
    
    df = pd.read_csv('Walker_model_data.csv', index_col = None) # loading required data
    input_array = np.asarray([df['dK'],df['R'],df['gamma']])
    input_array = np.transpose(input_array)
    
    dK = df['dK'].values # stress intensity values for 10 different machines at a given instant t
    R = df['R'].values # stress ratio values for 10 different machines at a given instant t
    gamma = df['gamma'].values # Walker model coefficient
    
    Co,m = 1.1323e-10,3.859 # Walker model coefficients (similar to Paris law) 
    
    #--------------------------------------------------------------------------
    danp = walker(dK,R,gamma,Co,m) # prediction of the genereic function
    
    batch_input_shape = (input_array.shape[-1],)
    
    model = create_model(Co = Co, m = m, batch_input_shape = batch_input_shape, myDtype = myDtype)
    results = model.predict_on_batch(input_array) # custumized layer prediction
    #--------------------------------------------------------------------------
    fig  = plt.figure(1)
    fig.clf()
    
    plt.plot(dK,danp,'ok', label = 'numpy')
    plt.plot(dK,results,'sm', label = 'tf Layer')
    
    
    plt.title('Walker model response')
    plt.xlabel('$\Delta$ K [MPa $m^{1/2}$]')
    plt.ylabel('$\Delta$ a [m]')
    plt.legend(loc=0, facecolor = 'w')
    plt.grid(which = 'both')
    #--------------------------------------------------------------------------
