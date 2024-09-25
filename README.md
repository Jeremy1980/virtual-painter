# virtual-painter
Virtual painter based on OpenCV and Mediapipe libraries

![sample effect of the virtual painter](/captured72.jpg)

The script in this version only supports the right hand as a drawing tool.

Left side ilustrate humand hand and tracking. Right side ilustrate result after coloring and parsing object on the left. Drawing and displaying is handled by OpenCV. Detecting parts of human body is handled by MediaPipe.

- All fingers straight -- creates an object on the right side of the image. 
- All fingers bent -- clears the scene on the right side of the image.
- You can draw with your index finger straight and the other fingers bent.
