from imutils.convenience import resize
import numpy as np
import cv2
import os
import imutils
import logging
import pickle

from os import path
from imutils import paths
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument(
    "-i", "--dataset", required=True, help="path to input directory of faces + images"
)
ap.add_argument(
    "-e",
    "--embeddings",
    required=True,
    help="path to output serialized db of facial embeddings",
)
ap.add_argument(
    "-c",
    "--confidence",
    type=float,
    default=0.5,
    help="minimum probability to filter weak detections",
)
args = ap.parse_args()

logging.basicConfig(level=logging.INFO)
logging.info("Started...")

logging.info("Loading face detector...")
protoPath = "resources/detector/deploy.prototxt"
modelPath = "resources/detector/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

logging.info("Loading face recognizer")
embedder = cv2.dnn.readNetFromTorch("resources/embedder/nn4.small2.v1.t7")

logging.info("Quantifying faces...")
imgPaths = list(paths.list_images(args.dataset))

knownEmbeddings = []
knownNames = []

total = 0

for i, imgP in enumerate(imgPaths):
    logging.info(f"Processing image {i + 1}/{len(imgPaths)}")
    name = path.split(imgP)[-2]

    img = cv2.imread(imgP)
    img = resize(img, width=600)
    h, w = img.shape[:2]

    imgBlob = cv2.dnn.blobFromImage(
        cv2.resize(img, (300, 300)),
        1.0,
        (300, 300),
        (104.0, 177.0, 123.0),
        swapRB=False,
        crop=False,
    )
    detector.setInput(imgBlob)
    detections = detector.forward()

    if len(detections) > 0:
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        if confidence > args.confidence:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            startX, startY, endX, endY = box.astype("int")

            face = img[startY:endY, startX, endX]
            fH, fW = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(
                face, 1 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False
            )
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            knownNames.append(name)
            knownEmbeddings.append(vec.flatten())
            total += 1

logging.info(f"Serializing {total} encodings...")
data = {"embeddings": knownEmbeddings, "names": knownNames}
with open(args.embeddings, "wb") as f:
    f.write(pickle.dumps(data))
