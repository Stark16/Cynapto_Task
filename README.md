# Cynapto_Task

**AIM**: To Read a given 720p video in `.mp4` format, then count and display the number of unique faces detected on current frame. Then Save the newly created 
         video in 720p, 20 FPS in `.mp4` format.
         
File Structure:

         |- efficient_face_recognition.py*
         |- Input_video.mp4*
         |- README.md*
         |- Experimenting_with_cython 
                  |
                  |- build
                  |- efficient_face_recognition.c*
                  |- efficient_face_recognition.cp37-win_amd64.pyd*
                  |- efficient_face_recognition.pyx*
                  |- efficient_face_recognition.html*

Here is the general approach towards achieving the primary objective of the assignment:

         1. `efficient_face_recognition.py` is the main python script that performs the said AIM of the assignment. 
         2. It reads the video file frame by frame then stores it into a `numpy` list of BGR image sequnce of each frame of the video.
         3. 
