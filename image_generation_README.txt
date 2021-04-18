Step 1 - Setting up automatic downloads:
	Open your default web browser.
	Open the options menu.
	Set the default action for downloading the filetype ".png" so that it is automatically saved to your downloads folder.
	The steps for this vary from browser to browser.
	If you don't know how to do this, look up a guide.
	(I would include the steps here, but they would be outdated very quickly.)

Step 2 - Generating images:
	Run scene_drawer.py.
	Your default web browser will open.
	Images will flash in the web browser.
	These images will be saved to your downloads folder.
	4672 images will be generated.
	While the images are generating:
		Do not close your browser.
		Do not move or rename the images.
	Once all images are generated, they will be moved to a folder named "img" in the current working directory.
	Once this process is complete, it is safe to close your browser and/or end the Python script.

Step 3 - Working with images:
	Use the images as you would any ".png" file.
	That's it!

Step 4 - Working with scene data:
	In the code, the contents of each image is described using a custom Python class.
	This class is called Scene.
	A list of every scene can be found in "pickle" folder in the current working directory.
	The list is called "scene_list.pickle."
	You can load this file into Python using the "SceneDrawer.load_pickle" method.
	For other uses, refer to the documentation for Python Pickle.