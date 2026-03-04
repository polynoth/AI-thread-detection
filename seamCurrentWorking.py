
import gstreamer
import os
import time
import argparse
from common import avg_fps_counter, SVG
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference
from pycoral.adapters.common import input_size
from pycoral.adapters.classify import get_classes

def generate_svg(size, text_lines):
    svg = SVG(size)
    for y, line in enumerate(text_lines, start=1):
      svg.add_text(10, y * 20, line, 20)
    return svg.finish()

def main():
    default_model_dir = '../all_models'
    default_model = '/home/nl/model_edgetpu.tflite'
    default_labels = '/home/nl/labels.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path',
                        default=os.path.join(default_model_dir,default_model))
    parser.add_argument('--labels', help='label file path',
                        default=os.path.join(default_model_dir, default_labels))
    parser.add_argument('--top_k', type=int, default=3,
                        help='number of categories with highest score to display')
    parser.add_argument('--threshold', type=float, default=0.90,
                        help='classifier score threshold')
    parser.add_argument('--videosrc', help='Which video source to use. ',
                        default='/dev/video0')
    parser.add_argument('--headless', help='Run without displaying the video.',
                        default=False, type=bool)
    parser.add_argument('--videofmt', help='Input video format.',
                        default='raw',
                        choices=['raw', 'h264', 'jpeg'])
    args = parser.parse_args()

    print('Loading {} with {} labels.'.format(args.model, args.labels))
    interpreter = make_interpreter(args.model)
    interpreter.allocate_tensors()
    labels = read_label_file(args.labels)
    inference_size = input_size(interpreter)

    # Average fps over last 30 frames.
    alarm = "/home/nl/alarm.mp3"
    fps_counter = avg_fps_counter(30)

    def user_callback(input_tensor, src_size, inference_box):
      nonlocal fps_counter
      start_time = time.monotonic()
      run_inference(interpreter, input_tensor)

      results = get_classes(interpreter, args.top_k, args.threshold)
      end_time = time.monotonic()
      text_lines = [
          ' ',
          'Inference: {:.2f} ms'.format((end_time - start_time) * 1000),
          'FPS: {} fps'.format(round(next(fps_counter))),
      ]
      good = 'good'
    
      for result in results:
        
        
        if result.id == 0 and result.score >= .90:
          #check if bad and meets threshold
          
            text_lines.append('confidence={:.2f}: {}'.format(result.score, labels.get(result.id, result.id)))
            os.system("gst123 "+ alarm)
        else:
            
            text_lines.append(good)
        print(' '.join(text_lines))
      
      
      return generate_svg(src_size, text_lines)

    result = gstreamer.run_pipeline(user_callback,
                                    src_size=(640, 480),
                                    appsink_size=inference_size,
                                    videosrc=args.videosrc,
                                    videofmt=args.videofmt,
                                    headless=args.headless)

if __name__ == '__main__':
    main()

## This file contains libraries (c) 2019 Google under the Apache licence distributed with the Google Coral Dev board. 
