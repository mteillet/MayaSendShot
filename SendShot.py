import maya.cmds as cmds
import os
import shutil

def main():
    # Getting the set project root directory and its name
    projectList = getProject()
    currentProjectPath = str(projectList[0])
    currentProjectName = str(projectList[1])

    # Getting the list in the filePathEditor
    pathEditorList = listFilePathEditor()

    # Getting the absolute path for every texture listed in the filePathEditor
    current = 0
    fileAbsoluteList = []
    for i in pathEditorList:
        fileAbsoluteList.append(str(findFile(pathEditorList[current], currentProjectPath)))
        current += 1
    print(fileAbsoluteList)

    # Get the currently opened scene
    scene = getScene()
    print(scene)

    # Ask for the new project location
    newProjectPath = str(newProjectLocation())
    print(newProjectPath)

    # Creating the base folder structure
    createDefaultProject(newProjectPath)

    # Copying the maya workspace.mel and the currently opened scene in the new project
    copySceneEnv(newProjectPath, scene, currentProjectPath)


def getProject():
    currentProjectPath = cmds.workspace(query = True, rootDirectory = True)
    projectPathList = currentProjectPath.split("/")
    currentProjectName = projectPathList[len(projectPathList) - 2]
    return(currentProjectPath, currentProjectName)

def listFilePathEditor():
    listFullPathEditor = (cmds.filePathEditor(query=True, listFiles=""))
    listPathEditor = listFullPathEditor[2:(len(listFullPathEditor))]
    return(listPathEditor)

def findFile(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            filePath = (os.path.join(root, name))
    filePath = filePath.replace("\\", "/")
    return(filePath)

def getScene():
    scene = cmds.file(q = True, sceneName = True)
    return(scene)

def newProjectLocation():
    projectLocation = str(cmds.fileDialog2(caption = "Choose a new directory for the project", dialogStyle=1, fileMode = 3))
    projectLocation = projectLocation.replace("[u'", "")
    projectLocation = projectLocation.replace("']", "")
    return(projectLocation)

def createDefaultProject(newProjectPath):
    projectFolders = ["assets", "autosave", "cache", "clips", "images", "movies", "renderData", "renderman", "sceneAssembly", "scenes", "scripts", "sound", "sourceimages", "Time Editor"]
    print("Creating the new project structure...")

    current = 0
    for i in projectFolders:
        path = (str(newProjectPath) + "/" + str(projectFolders[current]) + "/")

        try:
            os.makedirs(path)
            print("Created", path)
        except OSError:
            print(path, "already exists")
            if not os.path.isdir(path):
                raise

        current += 1

def copySceneEnv(newProjectPath, scene, currentProjectPath):
    # Copying the workspace.mel
    oldMayaEnv = currentProjectPath + "workspace.mel"
    newMayaEnv = newProjectPath + "/" + "workspace.mel"
    shutil.copy(oldMayaEnv, newMayaEnv)

    # Saving the scene before copying it in order to keep the last changes made
    cmds.file(save = True)

    # Copying the current scene.ma
    oldMayaScene = scene
    scenePath = oldMayaScene.replace(currentProjectPath, "")
    newMayaScene = newProjectPath + "/" + scenePath
    shutil.copy(oldMayaScene, newMayaScene)

def copyTextures(newProjectPath, currentProjectPath, fileAbsoluteList):
    current = 0
    for i in fileAbsoluteList:
        print(fileAbsoluteList[current])
        current += 1

if __name__ == "__main__":
    main()