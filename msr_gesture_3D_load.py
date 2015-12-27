'''
Created on 24 Dec 2015

@author: bliang03
'''
from load_utils import loadMatDepthFile
import cPickle as pickle
import os
import constants

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
    if (modality == constants.MODALITY[0]):
        matFiles = os.listdir(os.path.join(datasetPath, "depth"))
        for matFile in matFiles:
            depthFileName, _ = os.path.splitext(matFile)
            depthSequence = loadMatDepthFile(
                                os.path.join(datasetPath, "depth", matFile))
            if len(depthSequence) == 0:
                print "errors occur in reading %s" % depthFileName
            else:
                saveDepthFile(savePath, depthFileName, depthSequence)
                


if __name__ == "__main__":
    dataset = constants.DATASETS_NAME[2]
    datasetPath = os.path.join(constants.DATASETS_PATH, dataset, "data")
    savePath = os.path.join(constants.DATASETS_PATH, dataset, "load/depth/")
    loadDataset(datasetPath, savePath, constants.MODALITY[0])
    