# Design Patterns Prototype Demo

A PySide2 implementation of the prototype pattern example in the book [Design Patterns: Elements of Reusable Object-Oriented Software](https://books.google.com.tw/books?id=6oHuKQe3TjQC).

## Install

### Prerequisites

- Miniconda (or Anaconda)
- PySide2 requires Python 3.5+

### Steps

The installation process should be the same for both Windows and Linux.

1. Create a conda environment `pyside2`
    ```bash
    conda create --name pyside2 python=3.9
    ```
    NOTE: You can also use other Python versions as long as PySide2 supports it
2. Activate the `pyside` env
    ```bash
    conda activate pyside2
    ```
3. Install PySide2 in the `pyside2` conda environment
    ```bash
    pip install PySide2
    ```
4. Install the project
    ```bash
    pip install -e .
    ```

## Run

### Prerequisites

1. Activate the `pyside` env
    ```bash
    conda activate pyside2
    ```
2. Generate Python files from `.ui` files
    ```bash
    pyside2-uic -o src/ui/mainwindow.py src/ui/mainwindow.ui
    ```
3. Generate Python files from `.qrc` files
    ```bash
    pyside2-rcc -o src/resources_rc.py src/resources.qrc
    ```

### Run Main GUI

1. Activate the `pyside` env
    ```bash
    conda activate pyside2
    ```
1. Run `mainwindow.py`
    ```bash
    python src/mainwindow.py
    ```
