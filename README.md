# Hole-Filling
## 

An image processor built using Python and OpenCV that fills holes in images, along
with a simple command line utility.

## Running locally

### Requirements
 - [Python - v3.12](https://www.python.org/)
 - [Poetry - v1.8.3](https://python-poetry.org/)

### Installation

```sh
cd hole-filling
poetry install
```

### Usage

![Usage](resources/usage.png)

### Example

```sh
python -m hole_filling resources/Lenna.png resources/Mask.png 3 0.01 8
```

![Source](resources/Lenna.png)
![Mask](resources/Mask.png)
![Result](resources/Filled_c8_111524_112702.png)

## Running in docker

```sh
cd hole-filling
docker build -t hole-filling .
docker run --rm -it -v HOST/PATH:/app/resources:rw hole-filling
```

## Additional Implementations

### Flood Fill

A simple flood fill algorithm iterates through each pixel and, when a hole is
detected, calculates the mean value of its neighboring non-hole pixels and
assigns this mean as the new value for the hole. Number of neighbouring pixels 
to consider can be configured. The code supports 4 and 8 and defaults to 4.

```sh
python q2_flood_fill.py ./resources/Lenna.png ./resources/Mask.png --connectivity 8
```

![Flood Fill](resources/Filled_floodFill_c8_111524_120225.png)

### OpenCV - Fast Marching Method

```sh
python q3_fmm.py ./resources/Lenna.png ./resources/Mask.png
```

![FMM](resources/Filled_fmm_111524_120325.png)

## Unittest

Uses pytest for unit-testing

```sh
poetry run pytest
```

## Lint and Formatting

Uses ruff

```sh
poetry run ruff check hole_filling/
poetry run ruff format hole_filling/
```

## Static type checking

Uses mypy

```sh
poetry run mypy hole_filling/
```
