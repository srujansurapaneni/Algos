import Algorithmia
import numpy as np
from skimage.transform import resize
import caffe
import urllib2
import base64
import re
import subprocess
import pickle
import urlparse
import hashlib
import os
import uuid

caffe.set_mode_cpu()

def initialize_model():
    client = Algorithmia.client()
    
    mean_uri = "data://deeplearning/Places365Classifier/places365CNN_mean.binaryproto"
    model_uri = "data://deeplearning/Places365Classifier/deploy_alexnet_places365.prototxt"
    weights_uri = "data://deeplearning/Places365Classifier/alexnet_places365.caffemodel"
    label_uri = "data://deeplearning/Places365Classifier/categories_places365.txt"
    
    MODEL_FILE = client.file(model_uri).getFile().name
    PRETRAINED = client.file(weights_uri).getFile().name
    MEAN_FILE = client.file(mean_uri).getFile().name
    LABEL_FILE = client.file(label_uri).getFile().name
    
    # convert mean file into readible format
    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open(MEAN_FILE, 'rb' ).read()
    blob.ParseFromString(data)
    arr = np.array( caffe.io.blobproto_to_array(blob) )
    arr = arr.squeeze(0) # squeeze first axis
    m_min, m_max = arr.min(), arr.max()
    normal_mean = (arr - m_min) / (m_max - m_min)
    arr = caffe.io.resize_image(normal_mean.transpose((1,2,0)), (227, 227, 3)).transpose((2,0,1)) * (m_max - m_min) + m_min
    np.save('places365CNN_mean.npy', arr)
    
    labels = np.loadtxt(LABEL_FILE, str, delimiter='\t')
    
    net = caffe.Classifier(MODEL_FILE, PRETRAINED,
			    mean=np.load('places365CNN_mean.npy'),
    			channel_swap=(2,1,0),
    			raw_scale=226,
    			image_dims=(227, 227))
    
    return (net, labels)

net, labels = initialize_model()




def parseInput(input):
    if isinstance(input, basestring) or isinstance(input, bytearray):
        return [input]
    elif isinstance(input, dict):
        if "numResults" not in input and "image" not in input:
            raise AlgorithmError("Please provide a valid input.")
        elif "image" in input:
            if "numResults" in input:
                if not isinstance(input["numResults"], int):
                    raise AlgorithmError("numResults must be an integer.")
                return [input["image"], input["numResults"]]
            else:
                return [input["image"]]
        else:
            raise AlgorithmError("Please provide a valid input.")
    else:
        raise AlgorithmError("Please provide a valid input.")
        
        
def checkFormat(file):
    proc = subprocess.Popen(['file', file], stdout=subprocess.PIPE)
    out, _ = proc.communicate()
    body = out.split(': ')[1].split(',')[0]
    if body.startswith("TIFF") or body.startswith('JPEG') or body.startswith('PNG') or body.startswith('GIF') or body.startswith('BMP'):
        return True
    else:
        return False


def apply(input):
    
    random_uuid = str(uuid.uuid4())
    
    client = Algorithmia.client()
    
    parsed_input = parseInput(input)

    image = parseImage(parsed_input[0])
    
    filename = getFileName(parsed_input[0])
    
    image_content = open(image, 'r').read()
    
    try:
        if parsed_input[1] > len(labels):
            numResults = len(labels)
        else:
            numResults = parsed_input[1]
    except Exception:
        numResults = 5
    
    # check if cache exists
    cacheURI = "data://.algo/perm/" + filename + "," + str(numResults) + ","  + hashlib.md5(image_content).hexdigest()
    
    if client.file(cacheURI).exists():
        cached_image = client.file(cacheURI).getFile().name
        
        with open(cached_image, "rb") as f:
            rVal = pickle.load(f)
        
        return {"predictions": rVal}
        
    input_image = caffe.io.load_image(image)
    resized_image = caffe.io.resize_image(input_image, (227, 227))
    
    prediction = net.predict([resized_image])  # predict takes any number of images, and formats them for the Caffe net automatically
    
    top_inds = prediction[0].argsort()[::-1][:numResults]
    
    top_output_prob = map(lambda x: float(x), prediction[0][top_inds])
    
    top_labels = map(lambda x: "/".join(str(x).split(" ")[0].split("/")[2:]), labels[top_inds])
    
    tmp = zip(top_labels, top_output_prob)
    
    rVal = map(lambda x: {"class": x[0], "prob": x[1]}, tmp)
    
    # cache result
    with open("/tmp/cache_file_" + random_uuid, "wb") as f:
        pickle.dump(rVal, f)
    
    client.file(cacheURI).putFile("/tmp/cache_file_" + random_uuid)
    
    return {"predictions": rVal}
    
class AlgorithmError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

def parseImage(urlData):
    if isinstance(urlData, basestring):
        if urlData.startswith("http://") or urlData.startswith("https://"):
            response = urllib2.urlopen(urlData)
            FILE = open("/tmp/image.jpg", "wb")
            FILE.write(response.read())
            FILE.close()
            if checkFormat('/tmp/image.jpg'):
                return "/tmp/image.jpg"
            else:
                raise AlgorithmError("Please provide a valid image format, we accept the following image formats: PNG, JPG, BMP, GIF and TIFF")
        #elif urlData.startswith("data://"):
        elif not isinstance(re.match("[\\w\\+]+://.+", urlData), type(None)):
            client = Algorithmia.client()
            return client.file(urlData).getFile().name
        elif urlData.startswith("data:image/png;base64"):
            urlData = urlData.replace("data:image/png;base64,", "")
            with open("/tmp/image.png", 'wb') as output:
                output.write(base64.b64decode(urlData))
            return "/tmp/image.png"
        elif urlData.startswith("data:image/jpg;base64"):
            urlData = urlData.replace("data:image/jpg;base64,", "")
            with open("/tmp/image.jpg", 'wb') as output:
                output.write(base64.b64decode(urlData))
            return "/tmp/image.jpg"
        elif urlData.startswith("data:image/jpeg;base64"):
            urlData = urlData.replace("data:image/jpeg;base64,", "")
            with open("/tmp/image.jpeg", 'wb') as output:
                output.write(base64.b64decode(urlData))
            return "/tmp/image.jpeg"
        elif urlData.startswith("data:image/gif;base64"):
            urlData = urlData.replace("data:image/gif;base64,", "")
            with open("/tmp/image.gif", 'wb') as output:
                output.write(base64.b64decode(urlData))
            return "/tmp/image.gif"
        else:
            raise AlgorithmError("Please provide a valid data://, http:// or https:// URL.")
    elif isinstance(urlData, bytearray):
        with open("/tmp/image.jpg", 'wb') as output:
            output.write(urlData)
        return "/tmp/image.jpg"
    else:
        raise AlgorithmError("Please provide a valid input.")

def getFileName(urlData):
    if isinstance(urlData, basestring):
        if not isinstance(re.match("[\\w\\+]+://.+", urlData), type(None)):
            outName = urlData.split('/')[-1]
            filename, _ = os.path.splitext(outName)
            return filename + ".png"
        elif urlData.startswith("data:image/"):
            return "output.png"
        else:
            raise AlgorithmError("Please provide a valid url.")
    elif isinstance(urlData, bytearray):
        return "output.png"
    else:
        raise AlgorithmError("Please provide a proper input")
