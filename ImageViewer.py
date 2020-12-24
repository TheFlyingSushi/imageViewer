import PySimpleGUI as sg
import os.path
import pathlib
#This is a GUI with some work from https://realpython.com/pysimplegui-python/

default_path = pathlib.Path().absolute()
#Image folder text box and the list of images
file_list_column = [
    [sg.Text("Image Folder"),sg.In(size=(25, 1), enable_events=True, key="folderLocation", default_text=default_path),sg.FolderBrowse(),],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="fileList")],
]

# The image that will be shown
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-", size=(100,100))],
]

# The layout of the two above, and a seperator
layout = [
    [sg.Column(file_list_column), sg.VSeperator(), sg.Column(image_viewer_column),]
]

def getImages(folder):
    try:
        # Get list of files in folder
        file_list = os.listdir(folder)
    except:
        file_list = []

    fnames = [
        f for f in file_list
        if os.path.isfile(os.path.join(folder, f))
        and f.lower().endswith((".png", ".gif"))
    ]
    return fnames

window = sg.Window("Image Viewer", layout, finalize=True)
#Put a default path down
window["fileList"].update(getImages(default_path))

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "folderLocation": # Folder name changed, update list of images
        fnames = getImages(values["folderLocation"])
        window["fileList"].update(fnames)
    elif event == "fileList":  # A file was chosen from the listbox
        try:
            filename = os.path.join(values["folderLocation"], values["fileList"][0])
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)
        except:
            pass
window.close()