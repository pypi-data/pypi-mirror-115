from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
import json
import os
from os.path import join

from PIL import Image
from tflite_runtime.interpreter import Interpreter

def load_labels(path):
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}
    
    
def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :]=image
    
    
def classify_image(interpreter, image, top_k=1):
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))
    
    if output_details['dtype'] == np.uint8:
        scale, zero_point = output_details['quantization']
        output = scale*(output - zero_point)
        
    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]


def load_imgpath(data_dir):
    path = []
    for i in os.listdir(data_dir):
        person_dir = join(data_dir, i)
        for j in os.listdir(person_dir):
            img_dir = join(person_dir, j)
            path.append(img_dir)
    return path



def main():
    t0 = time.time()
    json_path = '/home/pi/tflite/class_indices.json'
    json_file = open(json_path, 'r')
    class_indict = json.load(json_file)
    img_dir = '/home/pi/test_picture/'
    path = load_imgpath(img_dir)
    labels = load_labels('/home/pi/tflite/seafood.txt')
    interpreter = Interpreter('/home/pi/tflite/model_efficientnet.tflite')
    
    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    #print(height, width)
    t2 = time.time()
    t = 0
    count = 0
    string = ''
    #imgpath = '/home/pi/test_picture/Clam/2.jpg'
    #image = Image.open(imgpath).convert('RGB').resize((width, height), Image.ANTIALIAS)
    #results = classify_image(interpreter, image)
    #index, confi = results[0]
    for _, imgpath in enumerate(path):
        t3 = time.time()
        image = Image.open(imgpath).convert('RGB').resize((width, height), Image.ANTIALIAS)
        results = classify_image(interpreter, image)
        index, confi = results[0]
        t1 = time.time()
        count += 1
        t = t + t1 - t3
        string = string + str(class_indict[str(index)]) + ' '*5 + str(confi) + ' '*5 + imgpath + '\n'
    with open('/home/pi/tflite/model_test.txt', 'w') as f:
        f.write(string)
    print(t / count)
    #t1 = time.time()
    #print(class_indict[str(index)], confi)
    #print(results)
    #print(t1-t0, t1-t2)
    


if __name__ == '__main__':
    main()