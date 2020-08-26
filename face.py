import face_recognition as fr
import cv2
import os

def face_rec():
    KNOWN_FACES_DIR = "static/known_faces"
    UNKNOWN_FACES_DIR = "static/unknown_faces"
    TOLERANCE = 0.6 # Represents the Type I Error. The standard in the field of facial recognition is ussually 0.6. 
    FRAME_THICKNESS = 3
    FONT_THICKNESS = 2
    MODEL = "cnn" 

    # First step in facial recognition is to detect the faces and then recognize the face.

    # Load all our known faces 
    print("loading known faces")

    # Make two lists for known faces and names
    known_faces = []
    known_names = []

    # For each known face we are going to take each picture for that known face, encode it, and place it in its respective list. 
    for name in os.listdir(KNOWN_FACES_DIR):
        print(f"{name} loading...")
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
            image = fr.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            encodings = fr.face_encodings(image)
            encoding = None
            if len(encodings) > 0:
                encoding = encodings[0]
            else:
                print("No faces found in the image!")
                continue
            known_faces.append(encoding)
            known_names.append(name)

    # Now we are going to loop over all the unknown faces, find the faces, and compare each face to all the known faces. Lots of looping...
    print("processing unknown faces")

    is_there_rec = False

    for filename in os.listdir(UNKNOWN_FACES_DIR):
        print(f"{filename} loading...")
        image = fr.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
        print("image load sucesss")
        locations = fr.face_locations(image, model=MODEL) # This is going to face detection and find all the faces in the given picture
        print("faces locations success")
        encodings = fr.face_encodings(image, locations) # we are going to specify where the locations are
        print("encodings success")
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # we convert it into BGR
        print("image conversion success")

        # for each of these we want to see if we find a match 
        for face_encoding, face_location in zip(encodings, locations):
            # results is going to return an array of booleans, comparing all the known faces we have to all the unknown faces in a given picture.
            results = fr.compare_faces(known_faces, face_encoding, TOLERANCE)
            match = None
            if True in results: # if we found any index to be true we get the name
                match = known_names[results.index(True)]
                print(f"Match found: {match}")

                # Now, we use cv2 to draw the iconic rectangles
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])
                color = [0, 255, 0]
                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
                # We also want to have a small rectangle to house the text
                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2]+22)
                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
                is_there_rec = True

        if is_there_rec == True:
            cv2.imwrite(os.path.join("static/uploads", "result.jpg"), image)
            
        return is_there_rec






            

