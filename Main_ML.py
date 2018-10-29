#!/usr/bin/python
'''
'''

#Import the OpenCV and dlib libraries
import cv2
import dlib
import time
import CallMicrosoftAPI
import VideoDisplay
from random import randint
import model


#Initialize a face cascade using the frontal face haar cascade provided with
#the OpenCV library
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#The deisred output width and height
OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600

def detectAndTrackLargestFace():
    #Open the first webcame device
    capture = cv2.VideoCapture(0)

    #Create two opencv named windows
    cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)

    #Position the windows next to eachother
    cv2.moveWindow("base-image",0,100)
    cv2.moveWindow("result-image",400,100)

    #Start qthe window thread for the two windows we are using
    #cv2.startWindowThread()

    #Create the tracker we will use
    tracker = dlib.correlation_tracker()

    #The variable we use to keep track of the fact whether we are
    #currently using the dlib tracker
    trackingFace = 0

    #The color of the rectangle we draw around the face
    rectangleColor = (0,165,255)


    try:
        while True:
            #Retrieve the latest image from the webcam
            rc,fullSizeBaseImage = capture.read()

            #Resize the image to 320x240
            baseImage = cv2.resize( fullSizeBaseImage, ( 320, 240))


            #Check if a key was pressed and if it was Q, then destroy all
            #opencv windows and exit the application
            pressedKey = cv2.waitKey(2)
            if pressedKey == ord('Q'):
                cv2.destroyAllWindows()
                exit(0)



            #Result image is the image we will show the user, which is a
            #combination of the original image from the webcam and the
            #overlayed rectangle for the largest face
            resultImage = baseImage.copy()






            #If we are not tracking a face, then try to detect one
            if not trackingFace:

                #For the face detection, we need to make use of a gray
                #colored image so we will convert the baseImage to a
                #gray-based image
                gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
                #Now use the haar cascade detector to find all faces
                #in the image
                faces = faceCascade.detectMultiScale(gray, 1.3, 5)

                #In the console we can show that only now we are
                #using the detector for a face
                print("Using the cascade detector to detect face")


                #For now, we are only interested in the 'largest'
                #face, and we determine this based on the largest
                #area of the found rectangle. First initialize the
                #required variables to 0
                maxArea = 0
                x = 0
                y = 0
                w = 0
                h = 0


                #Loop over all faces and check if the area for this
                #face is the largest so far
                #We need to convert it to int here because of the
                #requirement of the dlib tracker. If we omit the cast to
                #int here, you will get cast errors since the detector
                #returns numpy.int32 and the tracker requires an int
                for (_x,_y,_w,_h) in faces:
                    if  _w*_h > maxArea:
                        x = int(_x)
                        y = int(_y)
                        w = int(_w)
                        h = int(_h)
                        maxArea = w*h
                
                x1=x-20
                y1=y-30
                x2=x+w+20
                y2=y+h+30

                if len(faces)>0:
                    roi = resultImage.copy()
                    roi = roi[y1:y2,x1:x2]
                    #roi=cv2.resize( roi,( OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))
                    cv2.imwrite("Face.jpg",roi)
                    #time.sleep(1)
                    try:
                        age,gender,facialHair_beard,facialHair_moustache,facialHair_sideburns,makeup_eyeMakeup,makeup_lipMakeup=CallMicrosoftAPI.call_mico_api("D:/Vision/Face/FACE_LATEST/Face.jpg")
                        print(age,gender,facialHair_beard,facialHair_moustache)
                        predicted_output=model.predict(gender,smile,hair,age)
                        if predicted_output==0:
                            #'Clothing & Accessories L'
                            VideoDisplay.videoDisplay("C:/Users/mg75/Desktop/target marketing using facial detection/videos/Face_latest.mp4")
                        elif predicted_output==1:
                            #'Clothing & Accessories M'
                            VideoDisplay.videoDisplay("C:/Users/mg75/Desktop/target marketing using facial detection/videos/Face_latest.mp4")
                        elif predicted_output==2:
                            #'Entertainment',
                            VideoDisplay.videoDisplay("C:/Users/mg75/Desktop/target marketing using facial detection/videos/Face_latest.mp4")
                        elif predicted_output==3:
                            #'Health'
                            VideoDisplay.videoDisplay("C:/Users/mg75/Desktop/target marketing using facial detection/videos/Face_latest.mp4")
                        elif predicted_output==4:
                            #'Kids & Learning'
                            VideoDisplay.videoDisplay("C:/Users/mg75/Desktop/target marketing using facial detection/videos/Face_latest.mp4")
                        elif predicted_output==5:
                            #'Lifestyle'
                            VideoDisplay.videoDisplay("C:/Users/mg75/Desktop/target marketing using facial detection/videos/Face_latest.mp4")
                        else:
                            VideoDisplay.videoDisplay("C:/Users/mg75/Desktop/target marketing using facial detection/videos/Face_latest.mp4")
                            

                            
                        #select_num = randint(1,3)
##                        if gender=="male" and (age>=20 and age<30) and (facialHair_beard>0.1 and facialHair_beard<=0.7):
##                            VideoDisplay.videoDisplay("D:/Vision/Face/FACE_LATEST/videos/Face_latest.mp4")
##                        elif gender=="male" and age>=35:
##                            VideoDisplay.videoDisplay("D:/Vision/Face/FACE_LATEST/videos/Beer15.mp4")
##                        elif gender=="female" and (age>=20 and age<30) and (makeup_eyeMakeup==True or makeup_lipMakeup==True):
##                            VideoDisplay.videoDisplay("D:/Vision/Face/FACE_LATEST/videos/Makeup15.mp4")
##                        elif gender=="female" and age>=30:
##                            VideoDisplay.videoDisplay("D:/Vision/Face/FACE_LATEST/videos/Mother15.mp4")
##                        else:
##                            VideoDisplay.videoDisplay("D:/Vision/Face/FACE_LATEST/videos/Flowers15.mp4")
                    except:
                        print("Face is not detected properly")

                    #If one or more faces are found, initialize the tracker
                    #on the largest face in the picture
                    if maxArea > 0 :

                        #Initialize the tracker
                        tracker.start_track(baseImage,
                                            dlib.rectangle( x-10,
                                                            y-20,
                                                            x+w+10,
                                                            y+h+20))

                        #Set the indicator variable such that we know the
                        #tracker is tracking a region in the image
                        trackingFace = 1

            #Check if the tracker is actively tracking a region in the image
            if trackingFace:

                #Update the tracker and request information about the
                #quality of the tracking update
                trackingQuality = tracker.update( baseImage )



                #If the tracking quality is good enough, determine the
                #updated position of the tracked region and draw the
                #rectangle
                if trackingQuality >= 8.75:
                    tracked_position =  tracker.get_position()

                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())
                    cv2.rectangle(resultImage, (t_x, t_y),
                                                (t_x + t_w , t_y + t_h),
                                                rectangleColor ,2)

                else:
                    #If the quality of the tracking update is not
                    #sufficient (e.g. the tracked region moved out of the
                    #screen) we stop the tracking of the face and in the
                    #next loop we will find the largest face in the image
                    #again
                    trackingFace = 0





            #Since we want to show something larger on the screen than the
            #original 320x240, we resize the image again
            #
            #Note that it would also be possible to keep the large version
            #of the baseimage and make the result image a copy of this large
            #base image and use the scaling factor to draw the rectangle
            #at the right coordinates.
            largeResult = cv2.resize(resultImage,
                                     (OUTPUT_SIZE_WIDTH,OUTPUT_SIZE_HEIGHT))

            #Finally, we want to show the images on the screen
            #cv2.rectangle(baseImage, (t_x, t_y),
            #                                   (t_x + t_w , t_y + t_h),
             #                                   rectangleColor ,2)
            cv2.imshow("base-image", baseImage)
            cv2.imshow("result-image", largeResult)
            #save the file
            #cv2.imwrite("test.png",fullSizeBaseImage)
            print(trackingFace)




    #To ensure we can also deal with the user pressing Ctrl-C in the console
    #we have to check for the KeyboardInterrupt exception and destroy
    #all opencv windows and exit the application
    except KeyboardInterrupt as e:
        cv2.destroyAllWindows()
        exit(0)


if __name__ == '__main__':
    detectAndTrackLargestFace()
