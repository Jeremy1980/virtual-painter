#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cv2
from handtracking import HandTracking
import mediapipe as mp
import numpy as np
 
"""
 @brief Find hands in the current frame
 @return Status of fingers -- up or down
         List of 21 landmarks for the one hand
"""
def getHandInfo(img ,left_hand ,right_hand):
    _, hand = detector.detect(img ,left_hand ,right_hand) 
    
    if hand:
        lmList = hand["lmList"]  
        _, fingers = detector.fingersUp()
        return fingers, lmList
    else:
        return None
    
"""
    @brief Initialize a list of colors to represent each possible item in collection separately.
    @return ndarray.tolist() are converted to the nearest compatible builtin Python type, via the item function.
"""
def getColors(stock_length):
    return np.random.randint(5 ,255 ,size=(stock_length ,3) ,dtype="uint8").tolist()

def colorIt(points):
    colors = getColors(len(points))
    k = 0
    step = 6
    for n in range(step,len(points),step):
        curved_line = points[n-step:n]
        for m in range(0,len(curved_line)):
            pt1 = curved_line[m]
            pt2 = curved_line[m+1] if m+1 < len(curved_line) else curved_line[m]
            cv2.line(captured,pt1,pt2,colors[k],10)

        k += 1
  
# MediaPipe tools
mp_utils = mp.solutions.drawing_utils

# The MediaPipe Holistic pipeline integrates separate models
# for pose ,face and hand components ,each of which are optimized for their particular domain.
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    static_image_mode=False
    ,enable_segmentation=False
    ,model_complexity=1
    ,min_detection_confidence=0.5
    ,min_tracking_confidence=0.5)  
 

canvas=None
captured=None
prev_pos= None
figure_points = []

cap = cv2.VideoCapture(0 ,cv2.CAP_V4L)
 
# Initialize the HandDetector class with the given parameters
detector = HandTracking()
detector.fliped = True


cv2.namedWindow("Canvas")        # Create a named window
cv2.moveWindow("Canvas", 40,30)  # Move it to (40,30)

# Continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
    success, img = cap.read()

    if not success:
    # If loading a video, use 'break' instead of 'continue'.
        continue

    if detector.fliped:
        img = cv2.flip(img, 1)

    # It is necessary re-initiate 'preview' for human hand display 
    preview = np.zeros_like(img)

    # Create place to paint with the same shape as frame, if is first loop
    if captured is None:
        captured = np.zeros_like(img)
    if canvas is None:
        canvas = np.zeros_like(img)

    # ...and the magic begin
    results = holistic.process(img)
 
    # if detector.fliped set to True:
    # :: variable 'left_hand' has data of right human hand
    # :: variable 'right_hand' has data of left human hand
    left_hand = results.left_hand_landmarks.landmark if results.left_hand_landmarks else []
    right_hand = results.right_hand_landmarks.landmark if results.right_hand_landmarks else []
 
    # Draw anatomic structure of human hand
    if results.left_hand_landmarks:
        mp_utils.draw_landmarks(preview, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

    info = getHandInfo(img ,left_hand ,right_hand)
    if info:
        fingers, lmList = info
 
        current_pos= None
        if fingers == [0, 0, 0, 0, 0]:
            captured = np.zeros_like(img)
            
        if fingers == [1, 1, 1, 1, 1]:
            colorIt(figure_points)
            figure_points = []
            canvas = np.zeros_like(img)

        if fingers == [0, 1, 0, 0, 0] or fingers == [1, 1, 0, 0, 0]:
            current_pos = lmList[8][0:2]
            if prev_pos is None: prev_pos = current_pos
            cv2.line(canvas,current_pos,prev_pos,(255,0,255),10)
            figure_points.append(current_pos)

        prev_pos = current_pos
 
    # Display all images in one window using
    # np.concatenate for grouping and cv2.addWeighted for merging images horizontally
    cv2.imshow("Canvas", np.concatenate((cv2.addWeighted(canvas, 0.5, preview, 1.0 - 0.5, 0.0),captured), axis=1))
 
    # Keep the window open and update it for each frame; wait for 5 millisecond between frames
    if cv2.waitKey(5) & 0xFF == 27:
            break

cv2.destroyAllWindows() 