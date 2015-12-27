'''
Created on 24 Dec 2015

@author: bliang03
'''
from load_utils import loadXmlDepthFile2
import cPickle as pickle
import os
import constants
import gc

def saveDepthFile(savePath, fileName, depthSequence):
    """
        FUNC: save loaded depth file on disk
        PARAM:
            savePath: path to be saved at
            fileName: saved file name
        RETURN:
    """
    if not os.path.exists(savePath):
        os.makedirs(savePath)
        
    saveFile = os.path.join(savePath, fileName + ".pkl")
    if not os.path.exists(saveFile):
        with open(saveFile, "wb") as f:
            pickle.dump(depthSequence, f)
        print "%s saved." %fileName
    else:
        print "%s skipped." %fileName
        
        
def loadDataset(datasetPath, savePath, modality):
    """
        FUNC: load dataset and save file on disk
        PARAM:
            datasetPath: dataset path
            savePath: path where loaded files to be saved
            modality: depth or skeleton
        RETURN:
    """
    configFile = os.path.join(datasetPath, "actionLabel.txt")
    with open(configFile, "r") as f:
        lines = f.read().splitlines()
        
    if (modality == constants.MODALITY[0]):
        
        for i in xrange(0,220,11):
            currLines = lines[i:i+11]
#             depthFileDir = "s03_e01"
            depthFileDir = currLines[0]
            print "loading %s" %depthFileDir
            for line in currLines[1:]:
                splitIdx = line.index(":")
#                 depthFileName = "walk"
                depthFileName = line[:splitIdx]
                nums = line[splitIdx+1:].split()
#                 beginFrm = 372
                beginFrm = int(nums[0])
                endFrm = int(nums[1])
                depthSequence = loadXmlDepthFile2(os.path.join(datasetPath, "depth", depthFileDir), 
                                  beginFrm, endFrm)
                actionSavePath = os.path.join(savePath, depthFileDir)
                saveDepthFile(actionSavePath, depthFileName, depthSequence)
                
                del depthSequence
                gc.collect()
        
#         for depthFileDir in depthFileDirs:
#             depthFileName = depthFileDir
#             depthSequence = loadXmlDepthFile(
#                                 os.path.join(datasetPath, "depth", depthFileDir))
#             
#             actionSavePath = os.path.join(savePath, depthFileDir)
#             saveDepthFile(actionSavePath, depthFileName, depthSequence)
                


if __name__ == "__main__":
    dataset = constants.DATASETS_NAME[4]
    datasetPath = os.path.join(constants.DATASETS_PATH, dataset, "data")
    savePath = os.path.join(constants.DATASETS_PATH, dataset, "load/depth/")
    loadDataset(datasetPath, savePath, constants.MODALITY[0])
    