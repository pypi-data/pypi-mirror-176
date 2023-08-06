import setuptools

long_description = """
# miskibin

this repo contains some of my scripts and tools, that i
could not find anywhere else.

## installation:

```bash
pip install miskibin
```

## description

module contains some useful functions, that i use in my projects.

## usage

### get_logger

returns highly configurable logger object.

- Every level has its own color. (If it is printed to terminal)
- Problems with logging messages from `ipynb` cells are resolved.
- Includes validation for file name and path.
- Has `disable_existing_loggers` param to disable all other loggers.
#### options:
- `logger_name` - name of the logger
- `lvl`: [logging level](https://docs.python.org/3/library/logging.html#logging-levels). Default is 10 (DEBUG).
- `file_name`: file that logs will be saved to. If None, logs will not be saved to file.
- `format`: [logging format](https://docs.python.org/3/library/logging.html#logrecord-attributes).
- `datefmt`: date format for logging formatter. Define only if `(asctime)` in format Default is "%H:%M:%S".
- `disable_existing_loggers`: if True, disable existing loggers.

"""

setuptools.setup(
    name="miskibin",
    version="1.0.8",
    author="Michał Skibiński",
    author_email="mskibinski109@gmail.com",
    description="My personal package for colored logs. Highly customizable.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    files_to_include=["miskibin"],
    url="https://github.com/michalskibinski109/miskibin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
