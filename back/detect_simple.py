import argparse
import os
import platform
from re import X
import sys
from pathlib import Path
from tkinter import Y
import pandas as pd
import imutils
import numpy as np

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

hsv_blue_min = np.array([50, 100, 20], np.uint8)
hsv_blue_max = np.array([90, 255, 255],np.uint8)


from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode
@smart_inference_mode()


       
def run(
        weights=ROOT / 'best.pt',  # model path or triton URL
        source=ROOT / '2',  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / 'data/customdata.yaml',  # dataset.yaml path
        imgsz=(720, 1280),  # inference size (height, width)
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        line_thickness=1,  # bounding box thickness (pixels)
        vid_stride=2,  # video frame-rate stride
):
    source = str(source)
    #save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    screenshot = source.lower().startswith('screen')
    if is_url and is_file:
        source = check_file(source)  # download


    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, data=data)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    

    # Dataloader
    bs = 1  # batch_size
    if webcam:
        view_img = check_imshow()
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot:
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    vid_path, vid_writer = [None] * bs, [None] * bs
    
    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

       
        pred = model(im)
            
       
        
        # NMS
        with dt[2]:
            pred = non_max_suppression(pred)
           
        
        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
            
                

            p = Path(p)  # to Path
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            
                        
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
                

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                    

                # Write results
                for *xyxy, conf, cls in reversed(det):
                      # Write to file
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                        
                

                    c = int(cls)  # integer class
                    annotator.box_label(xyxy, color=colors(c, True))
                        
            #puntos =[(25,80)]
            # puntos = [(40,50)]
            # def dibuja_punto(frame, x, y):
            #     for punto in puntos:
            #         #print(f'Punto: {punto[0]}')
            #         cv2.circle(frame, (punto[0],punto[1]), 10, (0,255,0), 2)

            # Stream results
            im0 = annotator.result()
            # hsv = cv2.cvtColor(im0, cv2.COLOR_BGR2HSV)
            # mask = cv2.inRange(hsv, hsv_blue_min,hsv_blue_max)
            # mask = cv2.erode(mask, None, iterations=2)
            # mask = cv2.dilate(mask, None, iterations=2)

            # cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
            # centro = None
            # hay_sniffer = False
            # if len(cnts) > 0:
            #         c = max(cnts, key=cv2.contourArea)
            #         ((_, _), radius) = cv2.minEnclosingCircle(c)
            #         M = cv2.moments(c)
            #         centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            #         if radius > 7:
            #                 cv2.circle(im0, centro, 3, (0, 0, 255), -1)
            #                 hay_sniffer = True   
            # # Stream results
            # im0 = annotator.result()
            # #print(im0.shape)
            # for *xyxy,conf,cls in reversed(det):
            #     x1 = int(xyxy[0].item())
            #     y1 = int(xyxy[1].item())
            #     def _map(x, in_min, in_max, out_min, out_max):
            #         return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

            #     x=_map(x1,1,480,1,720)
            #     y=_map(y1,1,640,1,1280)
                
            #     if hay_sniffer:
            #         print(f'{x},{y}')
            #         exit()

            #     for punto in puntos:
            #         cv2.circle(im0, (punto[0]+x1,punto[1]+y1), 10, (0,255,0), 2)
                
            #     #cv2.circle(im0, (x1,y1), 10, (0,255,0), 2)
              
            #         #im0 = imutils.resize(im0, width=900)
            # #print(punto[0])
            cv2.imshow('img',im0)
            cv2.waitKey(1)
        


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'neveraiz.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default=ROOT / '2', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default=ROOT / 'data/customdata.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[200], help='inference size h,w')

    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt

    
def main(opt):
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
