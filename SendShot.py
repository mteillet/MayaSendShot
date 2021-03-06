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
        if "None" not in str(findFile(pathEditorList[current], currentProjectPath)):
            fileAbsoluteList.append(str(findFile(pathEditorList[current], currentProjectPath)))
            current += 1
    print(len(fileAbsoluteList), " File has been detected and will be copied")
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
    newMayaScene = copySceneEnv(newProjectPath, scene, currentProjectPath)

    # Copying the textures to the new project
    copyTextures(newProjectPath, currentProjectPath, fileAbsoluteList)

    # Modifying the Maya ASCII file to replace the texture strings
    modMayaAscii(newProjectPath, currentProjectPath, fileAbsoluteList, newMayaScene)

   


def getProject():
    currentProjectPath = cmds.workspace(query = True, rootDirectory = True)
    projectPathList = currentProjectPath.split("/")
    currentProjectName = projectPathList[len(projectPathList) - 2]
    return(currentProjectPath, currentProjectName)

def listFilePathEditor():
    listFullPathEditor = (cmds.filePathEditor(query=True, listFiles="", listDirectories=""))
    return(listFullPathEditor)

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

    return(newMayaScene)

def copyTextures(newProjectPath, currentProjectPath, fileAbsoluteList):
    # Copying the old.tex textures to the new project
    current = 0
    for i in fileAbsoluteList:
        oldTexture = (fileAbsoluteList[current])
        newTexture = oldTexture.replace(currentProjectPath, "")
        newTexture = newProjectPath + "/" + newTexture 

        pathList = newTexture.split("/")
        pathList = pathList[0:(len(pathList)-1)]
        path = "/".join(map(str, pathList)) + "/"

        # Creating needed folders if they exists
        try:
            os.makedirs(path)
            print("Created", path)
        except OSError:
            print(path, " already exists")
            if not os.path.isdir(path):
                raise

        if os.path.isfile(oldTexture + ".tex"):
            print("Copying the texture and its .tex conversion", oldTexture)
            shutil.copy(oldTexture, newTexture)
            oldTex = str(oldTexture) + ".tex"
            newTex = str(newTexture) + ".tex"
            shutil.copy(oldTex, newTex)
        else:
            print("Could not find a .tex, copying only the original texture", oldTexture)
            shutil.copy(oldTexture, newTexture)   

        current += 1

def modMayaAscii(newProjectPath, currentProjectPath, fileAbsoluteList, newMayaScene):
    print("Changing the Maya ASCII file to change the texture paths detected")

    # Getting all of the paths to change
    current = 0
    oldFiles = []
    newFiles = []
    for i in fileAbsoluteList:
        relativePath = fileAbsoluteList[current]
        relativePath = relativePath.replace(currentProjectPath, "")
        # Getting the search name for the path to replace
        oldFiles.append(currentProjectPath + "/" + relativePath)
        
        # Creating the new name for the path to replace
        newFiles.append(newProjectPath + "//" + relativePath)
        
        current += 1
    

    # Searching for files in the Maya ASCII code
    searchfile = open(newMayaScene).read()
    
    current = 0
    for i in oldFiles:
        searchfile = searchfile.replace(oldFiles[current], newFiles[current])
        current += 1

    writefile = open(newMayaScene, "w")
    writefile.write(searchfile)
    writefile.close()




if __name__ == "__main__":
    main()