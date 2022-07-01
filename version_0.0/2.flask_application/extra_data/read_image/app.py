

from flask import Flask, render_template_string, request, make_response,render_template
import cv2
import numpy as np
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("capture.html", width=320, height=240)

def send_file_data(data, mimetype='image/jpeg', filename='output.jpg'):
    # https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database/11017839

    response = make_response(data)
    response.headers.set('Content-Type', mimetype)
    response.headers.set('Content-Disposition', 'attachment', filename=filename)

    return response

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #print(request.files)  # it slowdown video
        #print(request.data)   # it slowdown video
        #fs = request.files['snap'] # it raise error when there is no `snap` in form
        print("Sweet poetry")
        fs = request.files.get('snap')
        if fs:
            #print('FileStorage:', fs)
            #print('filename:', fs.filename)

            # https://stackoverflow.com/questions/27517688/can-an-uploaded-image-be-loaded-directly-by-cv2
            # https://stackoverflow.com/a/11017839/1832058
            img = cv2.imdecode(np.frombuffer(fs.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            height, width = img.shape[:2]
            #print('Shape:', img.shape)
            # rectangle(image, start_point, end_point, color, thickness)
            img = cv2.rectangle(img, (20, 20), (width-20, height-20), (0, 0, 255), 2)

            text = datetime.datetime.now().strftime('%Y.%m.%d %H.%M.%S.%f')
            img = cv2.putText(img, text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            #cv2.imshow('image', img)
            #cv2.waitKey(1)

            # https://jdhao.github.io/2019/07/06/python_opencv_pil_image_to_bytes/
            ret, buf = cv2.imencode('.jpg', img)

            #return f'Got Snap! {img.shape}'
            return send_file_data(buf.tobytes())
        else:
            #print('You forgot Snap!')
            return 'You forgot Snap!'

    return 'Hello World!'


if __name__ == '__main__':
    # camera can work with HTTP only on 127.0.0.1
    # for 0.0.0.0 it needs HTTPS so it needs `ssl_context='adhoc'` (and in browser it need to accept untrusted HTTPS
    #app.run(host='127.0.0.1', port=5000)#, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')