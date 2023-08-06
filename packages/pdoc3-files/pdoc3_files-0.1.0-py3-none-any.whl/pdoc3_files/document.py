#!/usr/bin/env python
# coding: utf-8

"""Script pour l'extraction de DocString des fichier pythons pour la documentation générale.
Nécessite pdoc3:

`conda install -c conda-forge pdoc3`
"""

from pathlib import Path
import os
import pdoc
import codecs
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="""Bulk Python file documentation generator using pdoc3.

By default, if no argument other than the input dir is specified, a folder `doc/` is created in the current folder, with an HTML documentation file per python file.

- To output to reStructuredText format:
    `$ python document.py -t rst`

- To change the output dir path:
    `$ python document.py -o output_path`
""",
        formatter_class=argparse.RawTextHelpFormatter,
        )
    parser.add_argument(
        "input",
        type=Path,
        help="Root dir of project",
        metavar="PATH",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output dir",
        default="doc",
        metavar="PATH",
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=['html', 'rst'],
        default="html",
        metavar="TYPE",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
    )

    args = vars(parser.parse_args())

    py_files = []

    for path, directories, files in os.walk(str(args['input'].absolute())):
        p = [Path(path).joinpath(f) for f in files]
        py_files += [e.absolute() for e in p if e.exists() and e.suffix == ".py"]

    if args['verbose']:
        print("Found files:")
        print("\n".join([str(p.relative_to(os.getcwd())) for p in py_files]))

    context = pdoc.Context()

    modules = [pdoc.Module(pdoc.import_module(str(f)), context=context) for f in py_files]

    pdoc.link_inheritance(context)

    def recursive_htmls(mod, parent=""):
        yield parent + mod.name, mod.html(), mod.text()
        for submod in mod.submodules():
            yield from recursive_htmls(submod, parent + ".")


    args['output'].mkdir(exist_ok=True, parents=True)


    for mod in modules:
        for module_name, html, text in recursive_htmls(mod):
            if args['verbose']:
                print(f"Outputing documentation for module {module_name}")
                
            if args['type'] == 'html':
                with codecs.open(args['output'].joinpath(module_name + ".html"), "w", "utf-8") as f:
                    f.write(html)
            if args['type'] == 'rst':
                with codecs.open(args['output'].joinpath(module_name + ".rst"), "w", "utf-8") as f:
                    f.write(text)

if __name__ == "__main__":
    main()