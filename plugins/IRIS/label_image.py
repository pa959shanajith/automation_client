# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
#import tensorflow as tf
import os,base64
import logger
import logging
log = logging.getLogger('label_image.py')
from constants import *

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,input_height=299,input_width=299,input_mean=0,input_std=255):
    with tf.Graph().as_default():
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(file_reader, channels=3, name="png_reader")
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name="gif_reader"))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
        else:
            image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


class LabelImage():
    def start(self,view):
        try:
            if SYSTEM_OS=='Darwin':
                model_file = os.environ['AVO_ASSURE_HOME'] + '/lib/python3.7/site-packages/prediction/retrained_graph.pb'
                label_file = os.environ['AVO_ASSURE_HOME'] + '/lib/python3.7/site-packages/prediction/retrained_labels.txt'
            else:
                model_file = os.environ['AVO_ASSURE_HOME'] + '/Lib/site-packages/prediction/retrained_graph.pb'
                label_file = os.environ['AVO_ASSURE_HOME'] + '/Lib/site-packages/prediction/retrained_labels.txt'
##            input_height = 299 # for inception_v3
##            input_width = 299 # for inception_v3
            input_height = 224
            input_width = 224
            input_mean = 0
            input_std = 255
            #input_layer = "input"
            #output_layer = "InceptionV3/Predictions/Reshape_1"
            input_layer = "Placeholder"
            output_layer = "final_result"
            graph = load_graph(model_file)
            input_name = "import/" + input_layer
            output_name = "import/" + output_layer
            input_operation = graph.get_operation_by_name(input_name)
            output_operation = graph.get_operation_by_name(output_name)
            prediction_results = {}

            labels = load_labels(label_file)
            file_name = TEMP_PATH + OS_SEP + 'test.png'
            obj=view
            with tf.Session(graph=graph) as sess:
                #for obj in view:
                byte_mirror = base64.b64encode(obj['cord'].encode('utf-8'))
                b64 = base64.b64decode(byte_mirror)
                mirror = b64[2:len(b64)-1]
                with open(file_name,'wb') as f:
                    f.write(base64.b64decode(mirror))
                try:
                    t = read_tensor_from_image_file(
                      file_name,
                      input_height=input_height,
                      input_width=input_width,
                      input_mean=input_mean,
                      input_std=input_std)
                    results = sess.run(output_operation.outputs[0], {
                        input_operation.outputs[0]: t
                    })
                except:
                    log.info('Detected an older db')
                    log.debug('Detected an older db : changing tensor height/width to 299 ')
                    t = read_tensor_from_image_file(
                      file_name,
                      input_height=299,
                      input_width=299,
                      input_mean=input_mean,
                      input_std=input_std)
                    results = sess.run(output_operation.outputs[0], {
                        input_operation.outputs[0]: t
                    })
                results = np.squeeze(results)

                top_k = results.argsort()[-5:][::-1]

                result = {}
                for i in top_k:
                    result[results[i]] = labels[i]
                if(float(max(result.keys()))>0.75):
                    prediction_results[obj['custname']] = result[max(result.keys())]
                    prediction_results[obj['custname']] = prediction_results[obj['custname']][0].upper() + prediction_results[obj['custname']][1:]
                else:
                    prediction_results[obj['custname']] = 'unrecognizableobject'
            if(os.path.isfile(file_name)):
                os.remove(file_name)
        except Exception as e:
            logger.print_on_console('Error occured while labeling iris object type')
            log.error(e)
        return prediction_results
