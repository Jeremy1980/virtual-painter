#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class HandTracking:

    def __init__(self):
        self.tipIds = [4, 8, 12, 16, 20]
        self.leftHand = None
        self.rightHand = None

        # The 'fliped' parameter mark the the image as fliped horizontaly, making it easier for some detections
        self.fliped = False

    def detect(self, img, leftLandmarks, rightLandmarks):
        h, w, _ = img.shape

        self.leftHand = None
        if leftLandmarks:
            self.leftHand = {"position":"left"}
            
            ## lmList
            mylmList = []
            xList = []
            yList = []
            for lm in leftLandmarks:
                px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                mylmList.append([px, py, pz])
                xList.append(px)
                yList.append(py)

            ## bbox
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), \
                        bbox[1] + (bbox[3] // 2)

            self.leftHand["lmList"] = mylmList
            self.leftHand["bbox"] = bbox
            self.leftHand["center"] = (cx, cy)


        self.rightHand = None
        if rightLandmarks:
            self.rightHand = {"position":"right"}
            
            ## lmList
            mylmList = []
            xList = []
            yList = []
            for lm in rightLandmarks:
                px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                mylmList.append([px, py, pz])
                xList.append(px)
                yList.append(py)

            ## bbox
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), \
                        bbox[1] + (bbox[3] // 2)

            self.rightHand["lmList"] = mylmList
            self.rightHand["bbox"] = bbox
            self.rightHand["center"] = (cx, cy)


        return (self.rightHand ,self.leftHand) if self.fliped else (self.leftHand ,self.rightHand)

    def fingersUp(self):
        """
        @brief Finds how many fingers are open and returns in a list.
                Considers left and right hands separately
        @return List of which fingers are up
        """
        left = []
        right = []

        if self.leftHand:
            myLmList = self.leftHand["lmList"]
            # Thumb
            if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                left.append(1)
            else:
                left.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    left.append(1)
                else:
                    left.append(0)
                    
        if self.rightHand:
            myLmList = self.rightHand["lmList"]
            # Thumb
            if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                right.append(1)
            else:
                right.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    right.append(1)
                else:
                    right.append(0)            

        return (right, left) if self.fliped else (left, right)    