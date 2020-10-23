import pip

def check_install(package):
	try: 
		__import__(package)
	except ImportError:
		pip.main(['install', package])

requirement = ["tkinter", "re", "numpy", "matplotlib"]

for mod in requirement:
	check_install(mod)
