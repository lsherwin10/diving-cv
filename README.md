# diving-cv

## Usage
After cloning the repository and installing the packages in `requirements.txt` using `pip3 install -r requirements.txt`, you can execute the program by running `python3 main.py`. You can provide any of the options shown below to modify the input or output file paths. Any directories that do not exist in the output path will be created for you. During execution, the CLI should present a progress bar while the frames are being processed.

```bash
Options:
    -i FILE --input=FILE   # Input file path in .mov format [default: diving.mov].
    -o FILE --output=FILE  # Output file path in .mov format [default: diving_analyzed.mov].
```

```bash
Examples:
    python3 main.py  # implied input: diving.mov, implied output: diving_analyzed.mov

    python3 main.py -i videos/105b.mov -o results/analyzed/105b.mov
```

## Todo List:
- Fix black box that is drawn behind the joint angles so they can be seen more clearly


## References
- [Reading and Writing Videos in OpenCV](https://learnopencv.com/reading-and-writing-videos-using-opencv/#write-videos)
- [OpenCV Drawing](https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html)
- [Swift iOS App with Photo Picker](https://www.youtube.com/watch?v=yMC16EZHwZU)
- [GitHub Repo for iOS App Guide](https://github.com/StewartLynch/My-Images-Completed/tree/main/My%20Images)
