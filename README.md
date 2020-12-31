# Cynapto_Task

> **AIM**: To Read a given 720p video in `.mp4` format, then count and display the number of unique faces detected on the current frame. Then Save the newly created 
         video in 720p, 20 FPS in `.mp4` format.
         
> **File Structure**:
All files marked with * are directly related to the assignment's problem statement.

      |- Scripts
         |- cythonized_version
                  |
                  |- build
                  |- efficient_face_recognition.c*
                  |- efficient_face_recognition.pyd*
                  |- efficient_face_recognition.pyx*
                  |- efficient_face_recognition.html
                  |- main_file.py*
                  |- setup.py*
        |
        |- efficient_face_recognition.py
      |
      |- Videos
        |- Input_video.mp4*
        |- Input_video2.mp4*
        |- Output_video.mp4*
      |
        
> **Explaining directory structure**:

 * There are a 2 major parent directories named Scripts and Videos.
         
 * Video contain the Input video that is name *Input_video.mp4* and *Input_video2.mp4* the final output video is also saved in this directory with the name Output_video.mp4*.
         
* All the scripts are stored inside a Scripts folder. Which has 1 folder called *cythonized_version* and few python scripts that are the original version of the assignment scripts written in python.
         
- *cythonized_version*: 

         - To convert the python scripts into C, I have used a cython compiler. I'll explain how I did in brief.
         
         * The original python script is saved as "efficient_face_recognition.pyx" which is imported as module in 
         "main_file.py" to be executed.
         
         * In order to compiler the "efficient_face_recognition.pyx" to "efficient_face_recognition.c" I have written "setup.py" 
           which compiles the "efficient_face_recognition" into "efficient_face_recognition.c" and also produce 
           a "efficient_face_recognition.html" that is visual representation of which parts of the script uses python objects 
           as variable types.
           
         * To re-build the "efficient_face_recognition.c" run the following command in "cythonized_version" directory:
         > `python setup.py build_ext --inplace`
         
         * Then finally to execute the cythonize verizon, I.e the "efficient_face_recognition.c" run the following command:
         > `python main_file.py`

- *efficient_face_recognition.py* (The python version):

         * One can run the `efficient_face_recognition.py` with any Python 3.X interpreter to produce the output video provided 
         they have the required libraries installed in the environment.
         
         * To change the Input video path, or output video path, once can find the variables mentioned inside the script along 
         with more details on them.
         
> ** Setting up dlib and face_recognition with/without CUDA:** In your virtual environment (if any):

* $ `pip install dlib`
* $ 'git clone https://github.com/davisking/dlib.git'
* $ `cd dlib`
* $ `mkdir build`
* $ `cd build`
* $ `cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1`
* $ `cmake --build .`
* $ `cd ..`
* $ `python setup.py install --set USE_AVX_INSTRUCTIONS --set DLIB_USE_CUDA` "For cuda installation

More detailed installation can be found here: https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
          
> **Here is the general approach towards achieving the primary objective of the assignment**:

1. `efficient_face_recognition.py` is the main python script that performs the said AIM of the assignment. 
2. It reads the `Input_video.mp4` video file frame by frame then stores it into a `numpy` list of BGR image sequences of each frame of the video.
3. After getting total number of frames read from the video, the entire array is distributed into n "chunks" where n = #CPU cores.
4. By distributing the work into individual CPU cores, we call a worker function that uses the `face_recognition` library to find `face_encodings` and `bounding_boxes`of all      the faces in the current frame.
5. `face_encoding` is a 128 dimensional representation of the faces in frame. `bounding_boxes` contains the *left_top* and *right_bottom* coordinates of the bounding              boxes for      the face.
6. For each frame, we take in all the face_encoding and see if the total number of distinct face_encoding matches the #bounding_boces.
7. *If yes*: That means all the faces on the frame are distinct.
   *If No*: we count the difference between #face_encodings and #bounding_boxes. That gives us 3 basic possibilities of how the face may be repeated.
8. Step 7 is important as it ensures that only "unique" faces are counted (Which means counting twins/triplets as a single unique face).
9. The number of Faces is then returned and displayed on the frame.
10. After all the frames are processed, the video is reassembled, and saved as `Output_video.mp4` at 720p 20 FPS as mentioned in the problem statement.
11. `efficient_face_recognition.pyx` is the cython file of the same script. 
12. `setup.py`  is used to build a cythonize version of the original script. This allows the script to be executed with much more efficiency using a cython compiler, which allows for faster execution of instructions if we perform type declaration of the original python script variables.
13. It also produces the required `c` and `pyd` files, cython actually compiles the `efficient_face_recognition.c` file where the major speed boost comes from pre-declaring variable and return types..

* `Input_video.mp4` is the 25 secs input video chosen for processing. Which after processing will save a file named `Output_video.mp4`.
* All files related to cython and C conversion of the script are inside the `cythonized_version` directory.



> Environment details:

         - Conda virtual environment: *4.7.12*
         - Python *3.7*
         - cython *0.29.21*
         - Library Information is available in the script.




