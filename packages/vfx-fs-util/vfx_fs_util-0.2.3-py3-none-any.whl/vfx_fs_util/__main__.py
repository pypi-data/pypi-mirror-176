import os
import sys
from typing import List

from typer import Typer, Option, Argument
from rich.console import Console
from rich.tree import Tree

from vfx_fs_util.api import (
    walk_dir,
    get_human_readable,
    compress_filepaths,
)

app = Typer()
console = Console()
err_console = Console(stderr=True, style="bold red")


@app.command()
def ls(
    directory: str = Argument(os.getcwd()),
    include: List[str] = Option(
        [], "-i", "--include", help="list of regexes to include"
    ),
    exclude: List[str] = Option(
        [], "-e", "--exclude", help="list of regexes to exclude"
    ),
    size: bool = Option(False, "-s", "--size", help="size in bytes"),
    recursive: bool = Option(
        False, "-r", "--recursive", help="Recurse through directories"
    ),
    human_readable: bool = Option(
        False, "-m", "--human_readable", help="human readable size"
    ),
    format: str = Option(None, "-f", "--format", help="choose iteration set format"),
    summary: bool = Option(
        False, "--summary", help="Output summary of files and total size"
    ),
):

    summary_map = {
        "files": 0,
        "size": 0,
    }

    for compressed_path in walk_dir(
        directory, recursive=recursive, include=include, exclude=exclude
    ):
        output = compressed_path.format(format)

        if size:
            size = compressed_path.size()
            if summary:
                summary_map["size"] += size
            if human_readable:
                size = get_human_readable(size)
            output = "{:<15}{}".format(size, output)

        if summary:
            summary_map["files"] += len(compressed_path)

        console.print(output)

    if summary:
        if human_readable:
            summary_map["size"] = get_human_readable(summary_map.get("size"))
        console.print("files: {files}, size: {size}".format(**summary_map))


@app.command()
def tree(
    directory: str = Argument(os.getcwd()),
    include: List[str] = Option(
        [], "-i", "--include", help="list of regexes to include"
    ),
    exclude: List[str] = Option(
        [], "-e", "--exclude", help="list of regexes to exclude"
    ),
    # size: bool = Option(False, "-s", "--size", help="size in bytes"),
    level: int = Option(
        -1, "-l", "--level", help="How many levels to recurse into a directory."
    ),
    # human_readable: bool = Option(
    #     False, "-m", "--human_readable", help="human readable size"
    # ),
    # format: str = Option(None, "-f", "--format", help="choose iteration set format"),
    # summary: bool = Option(
    #     False, "--summary", help="Output summary of files and total size"
    # ),
):   
    tree = Tree(directory, guide_style="magenta")
    build_tree(
        tree,
        directory,
        include=include,
        exclude=exclude,
        level=0,
        target_level=level,
        format=format,
        # size=size,
        # human_readable=human_readable,
        # summary=summary,
    )
    console.print(tree)


def build_tree(
    tree, 
    directory, 
    level, 
    target_level,
    include=None, 
    exclude=None, 
    format=None, 
    # human_readable=False, 
    # size=False,
    # summary=False,
):

    if level==target_level:
        return

    files = []
    for item in os.listdir(directory):
        filepath = os.path.join(directory, item)
        if os.path.isdir(filepath):
            subtree = tree.add(item)
            level+=1
            build_tree(
                subtree,
                filepath, 
                level=level, 
                target_level=target_level,
                include=include, 
                exclude=exclude
            )
        else:
            files.append(item)

    compressed_paths = compress_filepaths(files, include=include, exclude=exclude)
    for compressed_file in compressed_paths:
        filepath_string = compressed_file.format(format)
        tree.add(filepath_string)


def main():
    try:
        app()
    except Exception as err:
        err_console.print(err)
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
