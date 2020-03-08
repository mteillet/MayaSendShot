import maya.cmds as cmds

def main():
    # Getting the set project root directory and its name
    projectList = getProject()
    currentProjectPath = str(projectList[0])
    currentProjectName = str(projectList[1])

    # Getting the list in the filePathEditor
    pathEditorList = listFilePathEditor()
    print(pathEditorList)


def getProject():
    currentProjectPath = cmds.workspace(query = True, rootDirectory = True)
    projectPathList = currentProjectPath.split("/")
    currentProjectName = projectPathList[len(projectPathList) - 2]
    return(currentProjectPath, currentProjectName)

def listFilePathEditor():
    return(cmds.filePathEditor(query=True, listDirectories=""))

if __name__ == "__main__":
    main()