'''
Created on 24 Dec 2015

@author: bliang03
'''
import os
import cv2
import h5py
import xml.etree.cElementTree as ET
import numpy as np
from utils import showDepthData

def loadPngDepthFile(depthFilePath):
        """
            FUNC: load depth file with extension of '.xml'
            
            PARAM: 
                depthFilePath: file path where xml depth files are
                
            RETURN: 
                depthSequence: a list of depth frame 
        """
        pngFiles = [f for f in os.listdir(depthFilePath) if f.endswith('.png')] 
        depthSequence = []
        
        for pngFile in pngFiles:
            depthData = cv2.imread(os.path.join(depthFilePath, pngFile), cv2.IMREAD_UNCHANGED)
            depthSequence.append(depthData)
            
        return depthSequence
    

def loadXmlDepthFile(depthFilePath):
        """
            FUNC: load depth file with extension of '.xml'
            
            PARAM: 
                depthFilePath: file path where xml depth files are
                
            RETURN: 
                depthSequence: a list of depth frame 
        """
        xmlFiles = [f for f in os.listdir(depthFilePath) if f.endswith('.xml')]
        xmlFiles.sort(key=lambda item: (len(item), item))
        depthSequence = []
        
        for xmlFile in xmlFiles:
            tree = ET.parse(os.path.join(depthFilePath, xmlFile))
            filename, _ = os.path.splitext(xmlFile)
            elem = tree.find('%s/data' % filename)
            strData = elem.text
            floatData = map(float, strData.split())
            depthData = np.array(floatData).reshape(240, 320)
#             showDepthData(depthData)
            depthSequence.append(depthData)
            
        return depthSequence


def loadXmlDepthFile2(depthFilePath, beginFrm, endFrm):
        """
            FUNC: load depth file with extension of '.xml' 
                  within [beginFrm, endFrm]
            
            PARAM: 
                depthFilePath: file path where xml depth files are
                beginFrm: begin frame
                endFrm: end frame
                
            RETURN: 
                depthSequence: a list of depth frame 
        """
        xmlFiles = [f for f in os.listdir(depthFilePath) if f.endswith('.xml')]
        xmlFiles.sort(key=lambda item: (len(item), item))
        depthSequence = []
        
        beginFrmFile = "depthImg%i.xml" %beginFrm
        endFrmFile = "depthImg%i.xml" %endFrm
        
        beginIdx = xmlFiles.index(beginFrmFile)
        endIdx = xmlFiles.index(endFrmFile)
        useXmlFiles = xmlFiles[beginIdx:endIdx+1]
        
        for xmlFile in useXmlFiles:
            tree = ET.parse(os.path.join(depthFilePath, xmlFile))
            filename, _ = os.path.splitext(xmlFile)
            elem = tree.find('%s/data' % filename)
            strData = elem.text
            floatData = map(float, strData.split())
            depthData = np.array(floatData).reshape(240, 320)
#             showDepthData(depthData)
            depthSequence.append(depthData)
            
        return depthSequence    
    
    
def loadMatDepthFile(depthFile):
    """
        FUNC: load depth file in mat format
        
        PARAM: 
            depthFile: mat depth files
            
        RETURN: 
            depthSequence: a list of depth frame 
    """
    depthSequence = []
    with h5py.File(depthFile, 'r') as f:
        seqData = f['depth_part'].value
#         print seqData.size
        if seqData.size > 3:
            # if data exist
            n,_,_ = seqData.shape
            
            for i in xrange(n):
                data = seqData[i,:,:]
                depthData = data.transpose()
                depthSequence.append(depthData)
        
    return depthSequence