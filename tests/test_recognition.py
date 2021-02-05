from os.path import join


def upload_sample(cli):
    imgname = "thefellowship.jpg"
    data = {"image": (open(join("samples", imgname), "rb"), imgname)}
    response = cli.post("/upload", data=data)
    assert response.status_code == 201
    assert "img_id" in response.json.keys()


def test_get_faces(cli):
    upload_sample(cli)

    response = cli.get(f"/recognize/{'thefellowship.jpg'}")
    assert response.status_code == 200
    assert "img_id" in response.json.keys()
    assert "faces" in response.json.keys()

    sample_face = response.json()["faces"][0]
    assert "bbox" in sample_face.keys()
    assert "character" in sample_face.keys()
