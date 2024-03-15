import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import socket
from flask_cors import CORS
import requests


from one_frame_with_api import process_image, get_scene_graph
# from one_frame import process_image, get_scene_graph

import base64


sys.path.append('/Downloads/ECOLE_Interface')  # Replace with the actual path to the ECOLE_Interface directory

app = Flask(__name__, static_url_path='/static')
CORS(app)

def download_image(image_url, local_file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(local_file_name, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Error downloading the image. HTTP status code: {response.status_code}")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.get_json()

    base64_image = encode_image('./keyframe2.jpeg')
    image = f"data:image/jpeg;base64,{base64_image}"
    output = process_image(image)

    # output = process_image('./keyframe2.jpeg')
    
    print(output)
    scene_graph = get_scene_graph(output)
    # print('>>>>>>>>>>>>>>>>>> flask >>>>>>>>>>>>>>>>>>')
    # print(scene_graph)
    # print('>>>>>>>>>>>>>>>>>> flask end >>>>>>>>>>>>>>>>>>')

    return {'frontend:': data['msg'],'image_description': output, 'scene_graph': scene_graph}

@app.route('/image_path', methods=['GET', 'POST'])
def image_path():
    data = request.get_json()
    local_file_name = "downloaded_image.jpg"

    download_image(data['image'], local_file_name)

    base64_image = encode_image('./static/downloaded_image.jpg')
    image = f"data:image/jpeg;base64,{base64_image}"
    output = process_image(image)

    # output = process_image('./keyframe2.jpeg')
    
    print(output)
    scene_graph = get_scene_graph(output)
    # print('>>>>>>>>>>>>>>>>>> flask >>>>>>>>>>>>>>>>>>')
    # print(scene_graph)
    # print('>>>>>>>>>>>>>>>>>> flask end >>>>>>>>>>>>>>>>>>')
    os.remove('./static/downloaded_image.jpg')

    return {'frontend:': data['msg'],'image_description': output, 'scene_graph': scene_graph}

@app.route('/test', methods=['GET', 'POST'])
def test():
    return{'msg':"hello"}


if __name__ == '__main__':
    host = socket.gethostname()
    port = '7327'

    print(f"ssh -N -L {port}:{host}:{port} -l tinghui.zhang hpg.rc.ufl.edu")
    app.run(host='0.0.0.0', port=port, debug=True)
