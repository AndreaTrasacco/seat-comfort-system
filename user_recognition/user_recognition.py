from deepface import DeepFace

recognition = DeepFace.find(img_path = "img.jpg", db_path = "../data/user_faces_db")
