from flask import Flask

# Import necessary libraries for visitor counter
import numpy as np
import cv2 as cv
import Person
import time

# Initialize Flask app
app = Flask(__name__)

# Initialize visitor count variable
cnt_down = 0

# Function to increment visitor count
def increment_visitor_count():
    global cnt_down
    cnt_down += 1

# Function to reset visitor count
def reset_visitor_count():
    global cnt_down
    cnt_down = 0

# Background visitor counter logic (you can integrate this with your existing logic)
def background_visitor_counter():
    global cnt_down
    
    # Your existing visitor counter logic here...
    # Remember to call increment_visitor_count() whenever a visitor is detected
    
    # For example, you might increment the count every time someone crosses a line:
    # if i.going_DOWN(line_down, line_up):
    #     increment_visitor_count()

# This route returns the visitor count
@app.route('/visitor_count')
def get_visitor_count():
    return str(cnt_down)

if __name__ == '__main__':
    # Start Flask app in a separate thread
    from threading import Thread
    Thread(target=app.run, kwargs={'host':'0.0.0.0', 'port': 5000}).start()
    
    # Start background visitor counter
    try:
        log = open('log.txt', "w")
    except:
        print("Cannot open log file")
    
    #Input and output counters
    prev_cnt = 0
    
    #video source
    cap = cv.VideoCapture(0)# Use webcam with device index 0
    #cap = cv.VideoCapture("test_1.mp4") 
    
    # cap.set(3, 160) #Width
    # cap.set(4, 120) #Height
    for i in range(19):
        print(i, cap.get(i))
    
    h = 480
    w = 640
    frameArea = h * w
    areaTH = frameArea / 250
    print('Area Threshold', areaTH)
    
    #Input/output lines
    line_up = int(2 * (h / 5))
    line_down = int(3 * (h / 5))
    
    up_limit = int(1 * (h / 5))
    down_limit = int(4 * (h / 5))
    
    print("Red line y:", str(line_down))
    print("Blue line y:", str(line_up))
    
    #background subtractor
    fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)
    
    #Structuring elements for morphological filters
    kernelOp = np.ones((3, 3), np.uint8)
    kernelOp2 = np.ones((5, 5), np.uint8)
    kernelCl = np.ones((11, 11), np.uint8)
    
    #Variables
    persons = []
    max_p_age = 5
    pid = 1
    
    start_time = time.time()  # Initialize start time
    
    while(cap.isOpened()):
        ret, frame = cap.read()
    
        for i in persons:
            i.age_one() #age every person one frame
    
        fgmask = fgbg.apply(frame)
        fgmask2 = fgbg.apply(frame)
    
        try:
            ret, imBin = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)
            ret, imBin2 = cv.threshold(fgmask2, 200, 255, cv.THRESH_BINARY)
            mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
            mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
            mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
            mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
        except:
            print('EOF')
            print('DOWN:', cnt_down)
            break
    
        contours0, hierarchy = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours0:
            area = cv.contourArea(cnt)
            if area > areaTH:
                M = cv.moments(cnt)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                x, y, w, h = cv.boundingRect(cnt)
    
                new = True
                if cy in range(up_limit, down_limit):
                    for i in persons:
                        if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                            new = False
                            i.updateCoords(cx, cy)
                            if i.going_UP(line_down, line_up):
                                increment_visitor_count()
                                #print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
                                log.write("ID: " + str(i.getId()) + ' crossed going up at ' + time.strftime("%c") + '\n')
                            elif i.going_DOWN(line_down, line_up):
                                #print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))
                                log.write("ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime("%c") + '\n')
                            break
                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > down_limit:
                                i.setDone()
                            elif i.getDir() == 'up' and i.getY() < up_limit:
                                i.setDone()
                        if i.timedOut():
                            index = persons.index(i)
                            persons.pop(index)
                            del i
    
                    if new:
                        p = Person.MyPerson(pid, cx, cy, max_p_age)
                        persons.append(p)
                        pid += 1
    
        current_time = time.time()
        if current_time - start_time >= 1:  # Check if one second has passed
            print("Number of Visitors:", cnt_down)
            prev_cnt = cnt_down
            start_time = current_time
    
        k = cv.waitKey(30) & 0xFF
        if k == ord('q'):  # Press 'q' to exit
            break
    
    log.flush()
    log.close()
    cap.release()
    cv.destroyAllWindows()
