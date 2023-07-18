import cv2
import imutils
import numpy as np
from tkinter import *
from tkinter import messagebox
from turtle import width


app=Tk()
app.title('Human Detection and Counting')
app.geometry('600x300')
app.configure(bg='#32527B')

def detect(frame):
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1
    
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.imshow('output', frame)

    if person>=15:
        messagebox.showwarning("Alert!","Overcrowded")

    return frame

def detectByPathVideo():
    # path = r'D:\Documents(D)\Human detection project\vid1.mp4'
    path = videoPath.get()
    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path.')
        return

    print('Detecting people...')
    while video.isOpened():
        check, frame =  video.read()

        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            frame = detect(frame)
            
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()
    app.destroy()

def detectByPathImage():
    # path= r'D:\Documents(D)\Human detection project\img2.jpg'
    path = imagePath.get()
    image = cv2.imread(path)
    image = imutils.resize(image, width = min(800, image.shape[1]))    

    result_image = detect(image)
    print(result_image)
    # cv2.destroyAllWindows()

def detectByCamera(writer):   
    video = cv2.VideoCapture(0)
    print('Detecting people...')

    while True:
        check, frame = video.read()

        frame = detect(frame)
        if writer is not None:
            writer.write(frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

imagePath = StringVar()
image_Label = Label(app, text = 'Enter Image Path:', font=('bold', 10), pady=13, padx=50, bg='#32527B')
image_Label.grid(row=0, column=0, sticky=W)
img_path_entry = Entry(app, textvariable=imagePath)
img_path_entry.grid(row=0, column=1, sticky=W)

videoPath = StringVar()
video_Label = Label(app, text = 'Enter Video Path:', font=('bold', 10), pady=13, padx=50, bg='#32527B')
video_Label.grid(row=3, column=0, sticky=W)
vid_path_entry = Entry(app, textvariable=videoPath)
vid_path_entry.grid(row=3, column=1, sticky=W)

def humanDetector():

    writer = None
    
    image_btn = Button(app, text='Count people from image', width=30, bg='#A69CAC', command=detectByPathImage)
    image_btn.grid(row=1, column=1, pady=10, padx=10)

    video_btn = Button(app, text='Count people from video', width=30, bg='#A69CAC', command=detectByPathVideo)
    video_btn.grid(row=4, column=1, pady=10, padx=10)

    cam_btn = Button(app, text='Count people from webcam', width=30, bg='#A69CAC', command=lambda: detectByCamera(writer))
    cam_btn.grid(row=5, column=1, pady=10, padx=10)

if __name__ == "__main__":
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    humanDetector()

app.mainloop()