from os.path import join

def test_upload_sample(cli):
    imgname = "thefellowship.jpg"
    data = {"image": (open(join("samples", imgname), "rb"), imgname)}
    response = cli.post("/upload", data=data)
    assert response == 400
