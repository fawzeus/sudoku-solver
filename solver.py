# import the necessary packages
from process import extract_digit
from process import find_puzzle
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import imutils
import cv2
from sudoku import Sudoku
def solve(image_path):

    # load the digit classifier from disk
    print("[INFO] loading classifier...")
    model = load_model("models/classifier.h5")
    # load the input image from disk and resize it
    image = cv2.imread(image_path)
    out=image
    image = imutils.resize(image, width=600)

    # find the puzzle in the image and then
    (puzzleImage, warped) = find_puzzle(image, False)
    # initialize our 9x9 Sudoku board
    board = np.zeros((9, 9), dtype="int")
    # a Sudoku puzzle is a 9x9 grid (81 individual cells), so we can
    # infer the location of each cell by dividing the warped image
    # into a 9x9 grid
    stepX = warped.shape[1] // 9
    stepY = warped.shape[0] // 9
    # initialize a list to store the (x, y)-coordinates of each cell
    # location
    cellLocs = []

    # loop over the grid locations
    for y in range(0, 9):
        # initialize the current list of cell locations
        row = []
        for x in range(0, 9):
            # compute the starting and ending (x, y)-coordinates of the
            # current cell
            startX = x * stepX
            startY = y * stepY
            endX = (x + 1) * stepX
            endY = (y + 1) * stepY
            # add the (x, y)-coordinates to our cell locations list
            row.append((startX, startY, endX, endY))
            # crop the cell from the warped transform image and then
            # extract the digit from the cell
            cell = warped[startY:endY, startX:endX]
            digit = extract_digit(cell, debug=False > 0)
            # verify that the digit is not empty
            if digit is not None:
                # resize the cell to 28x28 pixels and then prepare the
                # cell for classification
                roi = cv2.resize(digit, (28, 28))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                # classify the digit and update the Sudoku board with the
                # prediction
                pred = model.predict(roi).argmax(axis=1)[0]
                board[y, x] = pred
        # add the row to our cell locations
        cellLocs.append(row)
    # construct a Sudoku puzzle from the board
    print("[INFO] OCR'd Sudoku board:")
    puzzle = Sudoku(3, 3, board=board.tolist())
    puzzle.show()
    # solve the Sudoku puzzle
    print("[INFO] solving Sudoku puzzle...")
    solution = puzzle.solve()
    solution.show_full()
    # loop over the cell locations and board
    i,j=0,0
    for (cellRow, boardRow) in zip(cellLocs, solution.board):
        # loop over individual cell in the row
        j=0
        for (box, digit) in zip(cellRow, boardRow):
            
            # unpack the cell coordinates
            startX, startY, endX, endY = box
            # compute the coordinates of where the digit will be drawn
            # on the output puzzle image
            textX = int((endX - startX) * 0.33)
            textY = int((endY - startY) * -0.2)
            textX += startX
            textY += endY
            # draw the result digit on the Sudoku puzzle image
            if(board[i,j]==0):
                cv2.putText(puzzleImage, str(digit), (textX, textY),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            j+=1
        i+=1
    # show the output image
    #cv2.imshow("SOLVED Sudoku", puzzleImage)
    #cv2.imshow("original Image",out)

    
    return puzzleImage

#solve("images/sudoku_puzzle.jpg")
