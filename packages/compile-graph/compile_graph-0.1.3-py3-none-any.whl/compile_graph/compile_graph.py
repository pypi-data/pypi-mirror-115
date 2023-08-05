from typing import *
from collections import defaultdict
from . import wrapviz as wv
import re
import os

# matches <MATCH HERE>
SYS_HEADERS = re.compile(r"(?<=\<).*(?=\>)")

# matches "MATCH HERE"
USR_HEADERS = re.compile(r"(?<=\").*(?=\")")

# matches symbols from object dump
SYMBOLS = re.compile(r"(?<=\<)[^\.][^0-9][A-z0-9]*(?=\>)")


def extract_included_files(fp: "TextIO") -> Dict[str, tuple]:
    """
    Get headers included in source file.

    `#include <stdio.h>` : system header

    `#include "node.h"`  : user header
    """
    lines = "".join(line for line in fp.readlines() if line.startswith("#include"))
    sys_headers = tuple(dict((key, key) for key in SYS_HEADERS.findall(lines)))
    usr_headers = tuple(dict((key, key) for key in USR_HEADERS.findall(lines)))
    return {
        "sys": sys_headers,
        "usr": usr_headers,
    }


def extract_defined_symbols(fp: "TextIO") -> Tuple[str]:
    return tuple(  # type: ignore
        dict((key, key) for key in SYMBOLS.findall("".join(fp.read()))).keys()
    )


def files_in_directory(directory) -> DefaultDict[str, list]:
    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    data = defaultdict(list)
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext == ".c" or ext == ".cpp":
            data["sources"].append(f)
        elif ext == ".h" or ext == ".hpp":
            data["headers"].append(f)
        elif ext == ".o":
            data["objects"].append(f)

    return data


SOURCE_COLOR = "#00E9FF"
HEADER_COLOR = "#DE21C6"


def create_graph(directory, libs=None):
    wv.Digraph.reset()
    filedata = files_in_directory(directory)

    graph = wv.Digraph(label="Compile time", compound="true")

    shortcut = wv.Digraph(
        graph,
        label=f"g++ -g -Wall {' '.join(src for src in filedata['sources'])}",
    )

    header_nodes = {}

    exists = lambda fname: os.path.exists(os.path.join(directory, fname))

    object_nodes = []
    link_requirements = []

    for source in filedata["sources"]:
        src_node = wv.Node(
            graph, label=source, shape="rect", style="filled", fillcolor="#00E9FF"
        )

        unit_name, ext = os.path.splitext(source)
        preprocd_file = f"{unit_name}.i"

        preproc_node = wv.Node(
            shortcut,
            label=f"cpp {source} > {unit_name}.i",
            shape="cds",
            style="filled",
            fillcolor="white" if exists(preprocd_file) else "lightgreen",
        )

        object_file = f"{unit_name}.o"

        if exists(object_file):
            link_requirements.append(object_file)
        else:
            link_requirements.append(source)

        src_node.connect(preproc_node)

        with open(os.path.join(directory, source), "r") as fp:
            header_files = extract_included_files(fp)
        for sys_header in header_files["sys"]:
            if sys_header not in header_nodes:
                header = header_nodes[sys_header] = wv.Node(
                    graph,
                    label=sys_header,
                    shape="rect",
                    style="filled",
                    fillcolor=HEADER_COLOR,
                )
            else:
                header = header_nodes[sys_header]
            header.connect(preproc_node)

        for usr_header in header_files["usr"]:
            if usr_header not in header_nodes:
                header = header_nodes[usr_header] = wv.Node(
                    graph,
                    label=usr_header,
                    shape="rect",
                    style="filled",
                    fillcolor=HEADER_COLOR if exists(usr_header) else "lightgrey",
                )
            else:
                header = header_nodes[usr_header]
            header.connect(preproc_node)

        cc = "g++" if ext == ".cpp" else "gcc"

        translation_unit_graph = wv.Digraph(
            shortcut, label=f"translation unit: '{unit_name}'"
        )

        preprocd_name = f"{unit_name}.i"
        preprocd_node = preproc_node.connect(
            wv.Node(
                translation_unit_graph,
                label=preprocd_name,
                shape="rect",
                style="filled",
                fillcolor="yellow" if exists(preprocd_name) else "lightgrey",
            )
        )

        compile_fill_color = "white"
        if exists(preprocd_name) and not exists(object_file):
            compile_fill_color = "lightgreen"

        compile_command = preprocd_node.connect(
            wv.Node(
                translation_unit_graph,
                label=f"{cc} -g -Wall -c {preprocd_name if exists(preprocd_name) else source}",
                shape="cds",
                style="filled",
                fillcolor=compile_fill_color,
            )
        )
        object_file_node = compile_command.connect(
            wv.Node(
                translation_unit_graph,
                label=object_file,
                shape="rect",
                style="filled",
                fillcolor="yellow" if exists(object_file) else "lightgrey",
            )
        )

        object_nodes.append((object_file, object_file_node))

    linker_graph = wv.Digraph(shortcut, label="Linking")

    linker_command = wv.Node(
        linker_graph,
        label=f"g++ {' '.join(link for link in link_requirements)}",
        shape="cds",
        style="filled",
        fillcolor="lightgreen"
        if all(exists(d[0]) for d in object_nodes) and not exists("a.out")
        else "white",
    )

    output_node = wv.Node(
        graph,
        label="a.out",
        shape="rect",
        style="filled",
        fillcolor="yellow" if exists("a.out") else "lightgrey",
    )

    graph.graph.edge(linker_command.id, output_node.id)

    for _, node in object_nodes:
        shortcut.graph.edge(
            node.id,
            linker_command.id,
        )

    return graph


def main():
    import docopt
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    args = docopt.docopt("Usage: compile-graph [ <directory> ] [ -i | --interactive ]")
    directory = args["<directory>"] if args["<directory>"] is not None else os.getcwd()

    create_graph(directory).render()
    if args["-i"]:

        class Watcher(FileSystemEventHandler):
            def on_created(self, event):
                create_graph(directory).render()

            def on_deleted(self, event):
                create_graph(directory).render()

        observer = Observer()
        observer.schedule(Watcher(), directory)
        observer.start()
        observer.join()


if __name__ == "__main__":
    main()
