import os
import shutil
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup
from typing import List

from errors import NoInternetConnectionError

BASE_URL = 'https://subscene.com'
LANGUAGE = 'English'


def __parse_title_to_url(title, separator):
	"""
	This private function parses the `title` string passed as argument into a url query format
	that can work with 'https://subscene.com'.
	:return: str[url]
	"""
	if '(' in title:
		title = title[:title.index('(')].strip(separator)
	query = '-'.join(title.split(separator)).lower()
	return f"{BASE_URL}/subtitles/{query}/{LANGUAGE.lower()}/"


def _rename_sub(filename):
	"""This rename any .srt file int the current directory into `filename`"""
	for f, e in [os.path.splitext(f) for f in os.listdir()]:
		if e == '.srt':
			os.rename(f+e, filename+e)


def download(download_link, keep=True):
	"""
	This function downloads the file to be downloaded using the `download_link`and
	unzips the content.
	Parameter `keep` determines whether the zip file downloaded if left or deleted. If True, it is left,
	otherwise, deleted.
	:param download_link: str[url]
	:param keep: bool [default: True]
	"""
	r = requests.get(download_link)
	# Writing the content of the requests object to a file in byte mode (zip file).
	sub = 'subtitle.zip'
	with open(sub, 'wb') as f:
		f.write(r.content)
	# Extracting the content of the zip file i.e the subtitle, into the current directory.
	with ZipFile(sub) as z:
		z.extractall()
	if not keep:
		os.unlink(sub)


def _get_download_link(url):
	"""
	This function gets the subtitle download links using `url` from and returns a list of the download links.
	:return: List[urls]
	"""
	r = requests.get(url).text
	soup = BeautifulSoup(r, 'html.parser')
	return BASE_URL + soup.find('a', attrs={'id': 'downloadButton'})['href']


def _get_subtitle_links(url):
	"""
	This function gets and returns a list of all the links to the subtitle file uploaded by different users.
	:return: List[url]
	"""
	r = requests.get(url).text
	soup = BeautifulSoup(r, 'html.parser')
	sub_links = [BASE_URL + tag.a['href'] for tag in soup.findAll('td', attrs={'class': 'a1'})]
	return sub_links


def remove_unwanted_files(files, index=None) -> List:
	""" Removes unwanted files from `files` by their index in `index`."""
	if index:
		for i in index:
			files[i] = False
	return [f for f in files if f]


def move_file(file_path, destination, new_folder=False):
	"""
	[:] Moves a file with `file_path` to the `destination`.
	[:] Creates a new folder for the file at the `destination` if `new_folder` is True
	:param file_path: str[PathLike]
	:param destination: str[PathLike]
	:param new_folder: bool
	:return: None
	"""
	if new_folder:
		folder_name = os.path.splitext(os.path.split(file_path)[-1])[0]
		destination = os.path.join(destination, folder_name)
		try:
			os.mkdir(destination)
		except FileExistsError:
			pass
	try:
		shutil.move(file_path, destination)
	except FileNotFoundError:
		raise
	return destination


def get_files(dir_path, file_type) -> List[str]:
	"""
	[:] Returns list of files in directory `dir_path` with type `file_type`.
	:param dir_path: str[PathLike]
	:param file_type: str ||pattern: ".[a-z]+"||
	:return: List
	"""
	formats = {
		"videos": ['.mp4', '.avi', '.mkv', '.3gp'],
		"musics": ['.mp3', '.wav', '.amr'],
		"documents": ['.pdf', '.docs', '.docx', '.doc', '.txt', '.xlsx', '.csv'],
		"pictures": ['.png', '.jpeg', '.jpg'],
		"applications": ['.exe', '.aspx'],
		"subtitles": ['.srt']
		}
	files = [f for f in os.listdir(dir_path) if os.path.splitext(f)[-1] in formats[file_type]]
	return files


def sort_movies(base_dir, destination, files, new_folder=False):
	"""
	[:] Sorts the directory `base_dir` and gets the subtitle for the files from 'https://subscene.com'
	:param base_dir: str[PathLike]
	:param destination: str[PathLike]
	:param files: List
	:param new_folder: bool
	:return:
	"""
	for file in files:
		filename, ext = os.path.splitext(file)
		fp = os.path.join(base_dir, file)
		# subtitle = re.sub(r'\.\w+$', '.srt', file)
		subtitle = filename + '.srt'
		sub = os.path.join(base_dir, subtitle)
		dest = move_file(fp, destination, new_folder)
		if subtitle in os.listdir(base_dir):    # Subtitle file is available.
			move_file(sub, destination, new_folder)
		elif ext != '.mkv':     # download the subtitle if the movie is not '.mkv'
			print('Filename:', file)
			separator = ' '      # input("Separator: ") # default separator for the title
			# This means the title must have a format of "TITLE (YEAR)..." e.g. `Game Night (2018) Netnaija.com`.
			os.chdir(dest)
			try:
				download_subtitle(file, separator, False)
				_rename_sub(filename)
			except ConnectionError:
				raise NoInternetConnectionError("[ERROR]: Check your Internet Connection")


def download_subtitle(title, separator=' ', to_downloads=True):
	"""
	A function to download the subtitle file of a movie using the title of the movie. `to_downloads` determines
	whether the subtitle is downloaded to the default download folder on Windows OS.
	:param title: str
	:param separator: str
	:param to_downloads: bool
	"""
	url = __parse_title_to_url(title, separator)
	if to_downloads:
		os.chdir('C:/Users/DELL/Downloads')
	sub_links = _get_subtitle_links(url)
	choice = sub_links[0]
	print('choice:', choice)
	d_link = _get_download_link(choice)
	print('d_link:', d_link)
	download(d_link, keep=True)


def sort_dir(base_dir, destination, files, new_folder=False):
	"""
	[:] Sorts the directory `base_dir`
	:param base_dir: str[PathLike]
	:param destination: str[PathLike]
	:param files: List
	:param new_folder: bool
	"""
	for file in files:
		fp = os.path.join(base_dir, file)
		move_file(fp, destination, new_folder)
