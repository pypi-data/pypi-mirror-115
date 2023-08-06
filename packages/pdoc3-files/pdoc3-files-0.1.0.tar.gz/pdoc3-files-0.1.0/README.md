# pdoc3-files

Bulk Python file documentation generator using pdoc3.

By default, if no argument other than the input dir is specified, a folder `doc/` is created in the current folder, with an HTML documentation file per python file.

- To output to reStructuredText format:
    `$ python document.py -t rst`

- To change the output dir path:
    `$ python document.py -o output_path`