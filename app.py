from flask import Flask, render_template, request
import cv2 as cv
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    def reduce_size_of_image(ksh):
        height, width = ksh.shape[:2]
        eyebrow_h = int(height / 1.6)
        width_left = int(width / 6)
        width_right = int(width / 6)
        ksh = ksh[eyebrow_h:height, width_left:(width - width_right)]
        return ksh

    e = 2.7182
    gend = request.form.get('gender')
    uploaded_file = request.files['image'] # Get the FileStorage object
    filename = 'temp.jpg'  # Set a temporary filename
    uploaded_file.save(filename)
    ksh = cv.imread(filename)
    os.remove(filename)
    eyesCascade = cv.CascadeClassifier("haarcascade_eye.xml")
    eyes = eyesCascade.detectMultiScale(ksh, scaleFactor=2.1, minNeighbors=4, minSize=(100, 100))

    if len(eyes) != 0:
        print("Number of Eyes detected = ", len(eyes))
        for (x, y, w, h) in eyes:
            eye = ksh[y:y + h, x:x + w]
            ROI = eye
            cv.imwrite("/home/bizzle/Documents/Flask3/static/ROI_1.jpg", ROI)
            ROI_reduced = cv.imread('/home/bizzle/Documents/Flask3/static/ROI_1.jpg')
            # cv.imshow('ROI_red',ROI_reduced)
            ROI_reduced = reduce_size_of_image(ROI_reduced)

            # cv.imshow('ROI', ROI)
            # cv.imshow('ROI Reduced', ROI_reduced)

            # cv.waitKey(0)
            cv.imwrite("/home/bizzle/Documents/Flask3/static/ROI_Reduced.jpg", ROI_reduced)

            ROI_reduced_1 = cv.imread('/home/bizzle/Documents/Flask3/static/ROI_Reduced.jpg')
            gray = cv.cvtColor(ROI_reduced_1, cv.COLOR_BGR2GRAY)
            nonoise = cv.GaussianBlur(gray, (7, 7), 0)
            level, bw = cv.threshold(nonoise, 0, 255, cv.THRESH_OTSU + cv.THRESH_BINARY)
            contours, hierarchy = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

            largest_contour = {}
            max_area_contour = 0
            for i in range(len(contours)):
                area = cv.contourArea(contours[i])
                if area > max_area_contour:
                    max_area_contour = area
                    largest_contour = contours[i]

            mask = np.zeros_like(ROI_reduced_1)
            cont1 = cv.drawContours(mask, [largest_contour], 0, (255, 255, 255), -1)

            masked_eye = cv.bitwise_and(ROI_reduced_1, mask)
            # cv.imshow('Image Processed Eye', masked_eye)
            # cv.imshow('GaussianBLur', nonoise)
            # cv.imshow('Contour', cont1)

            def rgb():
                arr_list = ROI_reduced_1.tolist()
                r = g = b = 0
                for row in arr_list:
                    for item in row:
                        r = r + item[2]
                        g = g + item[1]
                        b = b + item[0]
                total = r + g + b
                red = r / total * 100
                green = g / total * 100
                blue = b / total * 100


                a = [red, green, blue]


                return a

            matrix = rgb()
            red = matrix[0]
            green = matrix[1]
            blue = matrix[2]
            # print(red)
            # print(green)
            # print(blue)

            hb = ((e - 1.922) + (0.206 * red) - (0.241 * green) + (0.012 * blue)) / (1 + (e - 1.922) + (0.206 * red) - (0.241 * green) + (0.012 * blue))

            if gend == 'Female':
                newhb = (hb * 4) + 9
            else:
                newhb = (hb * 4) + 11
            # else:
            #     print('Enter valid data')
            hb = [(hb*4) + 9]
            newhb = [round(hb[0],2)]

            # return [newhb]

    # else:
    #     print('No Eyes deteced!')


    return render_template('result.html', result=newhb[0])

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Change the port number as needed
