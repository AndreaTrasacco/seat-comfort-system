from deepface import DeepFace

analysis = DeepFace.analyze(img_path="img.jpg", actions=["emotion"])
print(analysis)
