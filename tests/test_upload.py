from os.path import join
import numpy as np
import cv2
import io


def test_upload_sample(cli):
    imgname = "thefellowship.jpg"
    data = {"image": (open(join("samples", imgname), "rb"), imgname)}
    response = cli.post("/upload", data=data)
    assert response.status_code == 201
    assert "img_id" in response.json.keys()


def test_upload_big_image(cli):
    noise = np.random.randint(0, 255, (6144, 6144, 3), dtype=np.uint8)
    enc_noise = cv2.imencode(".jpg", noise)[1].tobytes()
    data = {"image": (io.BytesIO(enc_noise), "noise.jpg")}
    response = cli.post("/upload", data=data)
    assert response.status_code == 413
    assert "error" in response.json.keys()
    assert "File is too large" == response.json["error"]
