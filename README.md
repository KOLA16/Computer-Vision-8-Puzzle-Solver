# 8Puzzle-Solver-OpenCV-PyTorch

Computer vision system that recognizes 8-Puzzle board and solves it using A* pathfinding algorithm.

The programme is build on the three main elements:
## Digit Recognition
I build a Convolutional Neural Network model from scratch using PyTorch and trained it on MNIST dataset to recognized digits from 0 to 9 with over 99% accuracy.
The model is then used to classify digits in the Puzzle board cells.
## Computer Vision
OpenCV is used to take feed from a webcam, identify a square board, and extract each individual cell which is then loaded to our pretrained model.
[PyImageSearch](https://www.pyimagesearch.com/) was very helpful resource and [this](https://www.pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/) blog post in particular, which was the inspiration for my project.
## Solution Finding
The whole one module is included which implements and runs the A* search algorithm to find the optimal solution to the puzzle read by a camera. Most of the code is adopted from this [repository](https://github.com/JaneHJY/8_puzzle), but significant changes are implemented to make it work in my project.

https://github.com/KOLA16/8Puzzle-Solver-OpenCV-PyTorch/blob/0caa5c897e41bf472cf3ce95e45904f3aadc2866/recordings/example.mp4
