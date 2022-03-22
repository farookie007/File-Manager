# File-Manager
**A file management program, it is used mainly to sort files, rearrange files, and perform other file management operations**

The `functions` module has bunch of functions for performing different operations, such as;

- `download` function: This function takes in a download link to the zip file containing the subtitle, downloads the subtitle and unzips it in the same folder.
It also has a `keep` parameter which takes in a boolean value and is set to `True` as default which determines whether to `keep` the zip file or not.

- `move_file` function: This function takes in the `file_path` (i.e the file path) and the `destination` (i.e the destination path). This function moves the file at `file_path` to
the path specified as destination. It also has a `new_folder` parameter which accepts a boolean and is set to `True` which means to open a new folder
to put the file at the destination. This is useful in sorting movies by creating a new folder for each movie where the subtitle file is also placed to make it easily tracked

- `get_files` function: This function takes 2 arguments which are `dir_path` (i.e a path) and a `file_type` (i.e type of file e.g `videos`, `musics` e.t.c) and it
returns a list of files having that `file_type`.

There are other functions like `sort_movies`, `download_subtitle`, `sort_dir` and more.



This program has an `app.py` file that you can run to display the **Console User Interface** which launches the **menu** and prompts the user as this is convinient for non-programmers.

The user can perform operations like sorting a whole directory, downloading files, moving files, cleaning a directory, e.t.c., these makes file operations faster and convinient.
