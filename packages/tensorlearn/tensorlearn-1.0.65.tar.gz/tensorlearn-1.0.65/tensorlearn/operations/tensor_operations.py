#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 21:00:44 2022

@author: Ryan Solgi
"""
import numpy as np
from tensorlearn.operations import tensor_operations

      
    ###################### unfolding 
    ###################### ###################### ###################### ######################               
def unfold(tensor,n):
    
            return np.rollaxis(tensor, n, 0).reshape(tensor.shape[n], -1)
    
    ###################### determine the shape of tensor according
    ###################### ###################### ###################### ######################
def tensor_shape(factors, factors_format):
    
    if factors_format=='TT':
        t_shape=[f.shape[1] for f in factors]
        return t_shape
    else:
        raise Exception("format is not defined")


    ###################### making tensor from factors 
    ###################### ###################### ###################### ######################  
def tensor(factors, factors_format): # factors is the list of facotrs

    if factors_format=='TT':
        t_shape=tensor_operations.tensor_shape(factors, 'TT')
        left_matrix=np.transpose(tensor_operations.unfold(factors[0],-1))
        for i in range (1,len(factors)):
            left_matrix=np.dot(left_matrix, tensor_operations.unfold(factors[i],0))
            left_matrix=np.reshape(left_matrix,(-1,factors[i].shape[-1]))
            
            
        tensor=np.reshape(left_matrix,t_shape)
        return tensor
    else:
        raise Exception("format is not defined")
    ###################### tensor resize, eneter zeros if the new size is bigger 
    ###################### ###################### ###################### ######################      
def tensor_resize(tensor,new_size): #new size is a tuple
    
    tensor_resized=tensor.copy()
    tensor_resized.resize(new_size)
    
    if tensor_resized.size < tensor.size:
        raise Exception ("new size is smaller than the origianl size") #does not allow data be missed
    
    else:
        return tensor_resized
    ###################### undo tensor resize using the factors
    ###################### ###################### ###################### ######################
    
def tensor_undo_resize(factors, shape, factors_format): #factors is the list of factors and the operation reverse tensor_resize function


    if type(shape) != tuple:
        raise Exception ("shape must be a tuple")
        
        
    original_size=1
    for item in shape:
        if not isinstance(item, int):
            raise Exception("item is not integer")
        original_size*=item
        
        

    
    tensor=tensor_operations.tensor(factors, factors_format)
        
        
    if tensor.size < original_size:
        raise Exception ("tensor size is smaller than the requested size")
        
    tensor_flatten=tensor.flatten()
    tensor_cut=tensor_flatten[:original_size]
    
    tensor_undo_resize = np.reshape(tensor_cut,shape)
    
    return tensor_undo_resize
    
    ###################### Tensor Frobenius norm
    ###################### ###################### ###################### ######################  
def tensor_frobenius_norm (tensor):
    tensor_flat=tensor.flatten()
    tensor_v=tensor_flat[...,np.newaxis]
    
    #tensor_v=np.reshape(tensor_flat,(1,(len(tensor_flat))))
    
    norm=np.linalg.norm(tensor_v,'fro')
    
    return norm

    
    ###################### Compression Ratio without reshaping
    ###################### ###################### ###################### ######################      
def compresion_ratio(factors, factors_format, original_shape=None):
    factors_size=0
    for item in factors:
        factors_size+=item.size
        
    if original_shape==None:
        t_shape=tensor_operations.tensor_shape(factors, factors_format)
    else:
        t_shape=original_shape
    
    t_shape_array=np.array(t_shape)
    
    tensor_size=np.prod(t_shape_array)
    
    compression_ratio=tensor_size/factors_size
    
    return compression_ratio
        

    
    
    

    
    
    
    

                 

        
        
        
        
        
                
        
            
        
        
        

        
    
        
            
