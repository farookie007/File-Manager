from functions.functions import *


INTRO = """Enter one of the following commands:
			'a' - Move a file
			'b' - Sort a directory
			'c' - Sort downloaded movies with subtitles
			'd' - Download a video subtitle
			'q' - Quit the program

"""


def get_input(msg):
	"""Get inputs from users and strips preceeding and trailing whitespace from the input"""
	x = input(msg).strip()
	return x


def prompt_move_file():
	file_path = get_input("Enter the path of the file to be moved: ")
	destination = get_input("Enter the destination folder: ")
	new_folder = True if get_input("Create a new folder for the file? [y/n] ") == 'y' else False
	return file_path, destination, new_folder


def prompt_sort_downloaded_movies():
	destination = "C:\\Users\\DELL\\Desktop\\Files\\Videos"
	d_path = "C:\\Users\\DELL\\Downloads"

	files = get_files(d_path, 'videos')

	print("Preview of the selected files: ")
	for i, file in enumerate(files, start=1):
		print(f"[{i}] : {file}")

	print()

	if get_input("Wish to stop a file from being sorted? [y/n] ") != 'n':
		print("Enter the corresponding index of the files: ")
		choice = input("(e.g: 1, 2, 3, ...): ").split(",")
		indices = [(int(i.strip())-1) for i in choice]
		files = remove_unwanted_files(files, index=indices)
		print("Final preview: ")
		for i, file in enumerate(files, start=1):
			print(f"[{i}] : {file}")
	print()

	return d_path, destination, files, True


def prompt_download_sub():
	print("Enter the title of the movie: ")
	title = get_input(">>> ")
	return title


def prompt_sort_file():
	print("Enter the following information: ")

	d_path = get_input("Path (directory to be sorted) [default is `Downloads`]: ")
	f_type = get_input("Type (e.g. subtitles, videos, musics, documents, pictures, applications): ")
	destination = get_input("Destination folder: ")

	if not d_path:
		d_path = "C:\\Users\\DELL\\Downloads\\"

	files = get_files(d_path, f_type)

	print("Preview of the selected files: ")
	for i, file in enumerate(files, start=1):
		print(f"[{i}] : {file}")

	if get_input("Wish to stop a file from being sorted? [y/n] ") == 'y':
		print("Enter the corresponding index of the files: ")
		choice = input("(e.g: 1, 2, 3, ...): ").split(",")
		indices = [(int(i.strip())-1) for i in choice]
		files = remove_unwanted_files(files, index=indices)
		print("Final preview: ")

		for i, file in enumerate(files, start=1):
			print(f"[{i}] : {file}")

	new_folder = True if get_input("Would you like to create a new folder for each file? [y/n] ") == 'y' else False

	return d_path, destination, files, new_folder


def menu():

	commands = {
		'a': (move_file, prompt_move_file),
		'b': (sort_dir, prompt_sort_file),
		'c': (sort_movies, prompt_sort_downloaded_movies),
		'd': (download_subtitle, prompt_download_sub)
		}

	print(INTRO)
	while True:

		user_choice = get_input("[Enter 'i' to get help]\n>>> ")
		if user_choice == 'q':
			break

		if user_choice == 'c':
			warning = """[WARNING]: This is a special method for
			moving movies.It moves each movies from
			'C:/Users/DELL/Downloads' to 'C:/Users/DELL/Desktop/Files/Videos'
			creates a new folder at the destination and also
			downloads the subtitle file for each movie.
			Return to use other commands to perform similar operations.
			"""
			print(warning)
			resp = get_input("Do you wish to continue? [y/n] ")
			if resp != 'y':
				continue
		try:
			action, prompt = commands[user_choice]
			action(*prompt())
			print("Operation Successful")
		except KeyError:
			print("[ ] Wrong Command. Try Again!")
		print()
