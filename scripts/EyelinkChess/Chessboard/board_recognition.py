import cv2
import numpy as np
import imutils
import math

debug = True


class Line:

    def __init__(self, x1, x2, y1, y2):
        '''
		Creates a Line object
		'''

        # Endpoints
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        # Change in x and y
        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1

        # Orientation
        if abs(self.dx) > abs(self.dy):
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'

    def find_intersection(self, other):
        '''
		Finds intersection of this line and other. One line must be horizontal
		and the other must be vertical
		'''

        # Determinant for finding points of intersection
        x = ((self.x1 * self.y2 - self.y1 * self.x2) * (other.x1 - other.x2) - (self.x1 - self.x2) * (
                other.x1 * other.y2 - other.y1 * other.x2)) / (
                    (self.x1 - self.x2) * (other.y1 - other.y2) - (self.y1 - self.y2) * (other.x1 - other.x2))
        y = ((self.x1 * self.y2 - self.y1 * self.x2) * (other.y1 - other.y2) - (self.y1 - self.y2) * (
                other.x1 * other.y2 - other.y1 * other.x2)) / (
                    (self.x1 - self.x2) * (other.y1 - other.y2) - (self.y1 - self.y2) * (other.x1 - other.x2))
        x = int(x)
        y = int(y)

        return x, y


class Square:

    def __init__(self, image, c1, c2, c3, c4, position, state=''):
        # Corners
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4

        # Position
        self.position = position

        # npArray of corners
        self.contour = np.array([c1, c2, c4, c3], dtype=np.int32)

        # Center of square
        M = cv2.moments(self.contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # ROI for image differencing
        self.roi = (cx, cy)
        self.radius = 7

        self.emptyColor = self.roiColor(image)

        self.state = state
        self.has_piece = False

    def draw(self, image, color, thickness=2):
        # Formattign npArray of corners for drawContours
        ctr = np.array(self.contour).reshape((-1, 1, 2)).astype(np.int32)
        cv2.drawContours(image, [ctr], 0, color, 3)

    def drawROI(self, image, color, thickness=1):
        cv2.circle(image, self.roi, self.radius, color, thickness)

    def roiColor(self, image):
        # Initialise mask
        maskImage = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        # Draw the ROI circle on the mask
        cv2.circle(maskImage, self.roi, self.radius, (255, 255, 255), -1)
        # Find the average color
        average_raw = cv2.mean(image, mask=maskImage)[::-1]
        # Need int format so reassign variable
        average = (int(average_raw[1]), int(average_raw[2]), int(average_raw[3]))

        return average

    def classify(self, image):
        rgb = self.roiColor(image)

        sum = 0
        for i in range(0, 3):
            sum += (self.emptyColor[i] - rgb[i]) ** 2

        cv2.putText(image, self.position, self.roi, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)


def clean_Image(image):
    # resize image
    img = imutils.resize(image, width=400, height=400)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Setting all pixels above the threshold value to white and those below to black
    # Adaptive thresholding is used to combat differences of illumination in the picture
    adaptiveThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 125, 1)
    if debug:
        # Show thresholded image
        cv2.imshow("Adaptive Thresholding", adaptiveThresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return adaptiveThresh, img


def initialize_mask(adaptiveThresh, img):
    # Find contours (closed polygons)
    contours, hierarchy = cv2.findContours(adaptiveThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create copy of original image
    imgContours = img.copy()

    for c in range(len(contours)):
        # Area
        area = cv2.contourArea(contours[c])
        # Perimenter
        perimeter = cv2.arcLength(contours[c], True)
        # Filtering the chessboard edge / Error handling as some contours are so small so as to give zero division
        # For test values are 70-40, for Board values are 80 - 75 - will need to recalibrate if change
        # the largest square is always the largest ratio
        if c == 0:
            Lratio = 0
        if perimeter > 0:
            ratio = area / perimeter
            if ratio > Lratio:
                largest = contours[c]
                Lratio = ratio
                Lperimeter = perimeter
                Larea = area
        else:
            pass

    # Draw contours
    cv2.drawContours(imgContours, [largest], -1, (0, 0, 0), 1)
    if debug:
        # Show image with contours drawn
        cv2.imshow("Chess Boarder", imgContours)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Epsilon parameter needed to fit contour to polygon
    epsilon = 0.1 * Lperimeter
    # Approximates a polygon from chessboard edge
    chessboardEdge = cv2.approxPolyDP(largest, epsilon, True)

    # Create new all black image
    mask = np.zeros((img.shape[0], img.shape[1]), 'uint8') * 125
    # Copy the chessboard edges as a filled white polygon size of chessboard edge
    cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
    # Assign all pixels that are white (i.e the polygon, i.e. the chessboard)
    extracted = np.zeros_like(img)
    extracted[mask == 255] = img[mask == 255]
    # remove strip around edge
    extracted[np.where((extracted == [125, 125, 125]).all(axis=2))] = [0, 0, 20]

    if debug:
        # Show image with mask drawn
        cv2.imshow("mask", extracted)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return extracted


def findEdges(image):
    # Find edges
    edges = cv2.Canny(image, 100, 200, None, 3)
    if debug:
        # Show image with edges drawn
        cv2.imshow("Canny", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Convert edges image to grayscale
    colorEdges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return edges, colorEdges


def findLines(edges, colorEdges):
    # Infer lines based on edges
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, np.array([]), 100, 80)

    # Draw lines
    a, b, c = lines.shape
    for i in range(a):
        cv2.line(colorEdges, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 255, 0), 2,
                 cv2.LINE_AA)

    if debug:
        # Show image with lines drawn
        cv2.imshow("Lines", colorEdges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Create line objects and sort them by orientation (horizontal or vertical)
    horizontal = []
    vertical = []
    for l in range(a):
        [[x1, y1, x2, y2]] = lines[l]
        newLine = Line(x1, x2, y1, y2)
        if newLine.orientation == 'horizontal':
            horizontal.append(newLine)
        else:
            vertical.append(newLine)

    return horizontal, vertical


def findCorners(horizontal, vertical, colorEdges):
    # Find corners (intersections of lines)
    corners = []
    for v in vertical:
        for h in horizontal:
            s1, s2 = v.find_intersection(h)
            corners.append([s1, s2])

    # remove duplicate corners
    dedupeCorners = []
    for c in corners:
        matchingFlag = False
        for d in dedupeCorners:
            if math.sqrt((d[0] - c[0]) * (d[0] - c[0]) + (d[1] - c[1]) * (d[1] - c[1])) < 20:
                matchingFlag = True
                break
        if not matchingFlag:
            dedupeCorners.append(c)

    for d in dedupeCorners:
        cv2.circle(colorEdges, (d[0], d[1]), 10, (0, 0, 255))

    if debug:
        # Show image with corners circled
        cv2.imshow("Corners", colorEdges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return dedupeCorners


def findSquares(corners, colorEdges):
    '''
    Finds the squares of the chessboard
    '''

    # sort corners by row
    corners.sort(key=lambda x: x[0])
    rows = [[], [], [], [], [], [], [], [], []]
    r = 0
    for c in range(0, 81):
        if c > 0 and c % 9 == 0:
            r = r + 1

        rows[r].append(corners[c])

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
    Squares = []

    # sort corners by column
    for r in rows:
        r.sort(key=lambda y: y[1])

    # initialize squares
    for r in range(0, 8):
        for c in range(0, 8):
            c1 = rows[r][c]
            c2 = rows[r][c + 1]
            c3 = rows[r + 1][c]
            c4 = rows[r + 1][c + 1]

            position = letters[r] + numbers[7 - c]
            position_daniel = str(r) + str(7 - c)
            newSquare = Square(colorEdges, c1, c2, c3, c4, position_daniel)
            newSquare.draw(colorEdges, (0, 0, 255), 2)
            newSquare.drawROI(colorEdges, (255, 0, 0), 2)
            newSquare.classify(colorEdges)
            Squares.append(newSquare)

    if debug:
        # Show image with squares and ROI drawn and position labelled
        cv2.imshow("Squares", colorEdges)
        key = cv2.waitKey(0)
        if key == ord("s"):
            cv2.imwrite("squares.jpg", colorEdges)

        cv2.destroyAllWindows()

    return Squares


def detect_objects(squares, mask):
    board = 0
    cv2.imwrite("board_check.jpg", mask)
    for i in squares:
        img = mask[i.c1[1]:i.c4[1], i.c1[0]:i.c4[0]]
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(7,7),0)
        edges = cv2.Canny(image=img, threshold1=80, threshold2=200)
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 45,
                                   param1=50, param2=10, minRadius=0, maxRadius=50)
        if circles is not None:
            i.has_piece = True
            print("piece!")
            circles = np.uint16(np.around(circles))
            for j in circles[0, :]:
                center = (j[0], j[1])
                # circle center
                cv2.circle(img, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = j[2]
                cv2.circle(img, center, radius, (255, 0, 255), 3)
        cv2.imshow("Squares", img)
        print(i.position)

        cv2.waitKey(0)
    return squares

def alter_detect_objects(img_raw):
    bilateral_filtered_image = cv2.bilateralFilter(img_raw, 5, 175, 175)
    cv2.imshow('Bilateral', bilateral_filtered_image)
    cv2.waitKey(0)

    edge_detected_image = cv2.Canny(bilateral_filtered_image, 20, 200)
    cv2.imshow('Edge', edge_detected_image)
    cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
            contour_list.append(contour)

    cv2.drawContours(img_raw, contour_list, -1, (255, 0, 0), 2)
    cv2.imshow('Objects Detected', img_raw)
    cv2.waitKey(0)


def board_recognition(image):
    adaptiveThresh, img = clean_Image(image)
    # Black out all pixels outside the border of the chessboard
    mask = initialize_mask(adaptiveThresh, img)
    # Find edges
    edges, colorEdges = findEdges(mask)
    # Find lines
    horizontal, vertical = findLines(edges, colorEdges)
    # Find corners
    corners = findCorners(horizontal, vertical, colorEdges)
    # Find squares
    squares = findSquares(corners, img)
    # detect objects
    squares = detect_objects(squares, mask)
    cv2.destroyAllWindows()
    return squares