import os
import cv2
import numpy as np
from PIL import Image
import pytube
import time


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '


def covertVideoToAscii(fileName, cols, scale, moreLevels):
    global gscale1, gscale2

    image = Image.open(fileName).convert('L')

    W, H = image.size[0], image.size[1]

    w = W / cols

    h = w / scale

    rows = int(H / h)

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    aimg = []

    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        if j == rows - 1:
            y2 = H

        aimg.append("")

        for i in range(cols):

            x1 = int(i * w)
            x2 = int((i + 1) * w)

            if i == cols - 1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))

            avg = int(getAverageL(img))

            if moreLevels:
                gsval = gscale1[int((avg * 69) / 255)]
            else:
                gsval = gscale2[int((avg * 9) / 255)]

            aimg[j] += gsval

    return aimg


def getAverageL(image):
    im = np.array(image)

    w, h = im.shape

    return np.average(im.reshape(w * h))


def main(imgFile, scale=0.43, outFile="out.txt", cols=80, moreLevels=None):
    aimg = covertVideoToAscii(imgFile, cols, scale, moreLevels)

    f = open(outFile, 'w')

    for row in aimg:
        f.write(row + '\n')

    f.close()


def start(videotitle=None):
    cls()
    print("            _____  _____ _____ _____         _                       \n"
          "     /\    / ____|/ ____|_   _|_   _|       | |                      \n"
          "    /  \  | (___ | |      | |   | |    _ __ | | __ _ _   _  ___ _ __ \n"
          "   / /\ \  \___ \| |      | |   | |   | '_ \| |/ _` | | | |/ _ \ '__|\n"
          "  / ____ \ ____) | |____ _| |_ _| |_  | |_) | | (_| | |_| |  __/ |   \n"
          " /_/    \_\_____/ \_____|_____|_____| | .__/|_|\__,_|\__, |\___|_|   \n"
          "                                      | |             __/ |          \n"
          "                                      |_|            |___/           \n"
          )
    print("do you want to play a video from youtube or from your PC [YouTube]/[PC] Y/P")
    choice = input()

    if choice.lower() == "y":
        url = input("Paste url here!\n")
        try:
            print("video is downloading")
            youtube = pytube.YouTube(url)
            video = youtube.streams.first()
            videotitle = video.title + ".mp4"
            video.download()
        except:
            print("Url is not valid")


    else:
        videotitle = input("Type video title here! (Video must be in the same directory as this program!)\n")

    print("Video is starting in 5 seconds pres Ctrl + C to stop it")
    time.sleep(5)

    cap = cv2.VideoCapture(videotitle)

    while True:
        ret, frame = cap.read()

        cv2.imwrite("frame.png", frame)
        main(imgFile="frame.png")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cls()
        with open("out.txt", "r")as f:
            data = f.read()
            print(data)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start()