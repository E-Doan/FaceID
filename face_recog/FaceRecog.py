""""
Sources:
  1) Video tutorial
      https://www.youtube.com/watch?v=QSTnwsZj2yc
  2) Base: 
      https://github.com/bradtraversy/face_recognition_examples/blob/master/indentify.py
  3) Used to get headshots: 
      https://github.com/bradtraversy/face_recognition_examples/blob/master/pullfaces.py
  4) Used to get user photo from computer:
      https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
"""
import face_recognition
from PIL import Image, ImageDraw
import os
from tkinter.filedialog import askopenfilename

path = ".\img\known"
dir_list = os.listdir(path)

dir_list.remove(".DS_Store")

known_face_encodings = []
known_face_names = []

for image in dir_list:
  filename = "./img/known/" + image
  image_of_person = face_recognition.load_image_file(filename) 
  person_face_encoding = face_recognition.face_encodings(image_of_person)[0]

  #  Create arrays of encodings and names
  known_face_encodings.append(person_face_encoding)

  known_face_names.append(filename[12:-4])

# 4) show an "Open" dialog box and return the path to the selected file
group_photo = askopenfilename()

# Load test image to find faces in
test_image = face_recognition.load_image_file(group_photo)

# 2) Find faces in test image
face_locations = face_recognition.face_locations(test_image)
face_encodings = face_recognition.face_encodings(test_image, face_locations)

# 2) Convert to PIL format
pil_image = Image.fromarray(test_image)

# 2) Create a ImageDraw instance
draw = ImageDraw.Draw(pil_image)

# Loop through faces in test image
for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
  matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

  name = "Unknown Person"

  # If match
  if True in matches:                               # 2)
    first_match_index = matches.index(True)         # 2)
    name = known_face_names[first_match_index]      # 2)
  else:
    face_image = test_image[top:bottom, left:right] # 3)
    new_image = Image.fromarray(face_image)         # 3)

    new_image.show()                                # 3)

    newName = input(f"What is the name of the unknown person in the previous photo?: ")
    new_image.save(f'./img/known/{newName}.jpg')    # 3)
    name = newName
  
  # 2) Draw box
  draw.rectangle(((left, top), (right, bottom)), outline=(255,255,0))

  # 2) Draw label
  text_width, text_height = draw.textsize(name)
  draw.rectangle(((left,bottom - text_height - 10), (right, bottom)), fill=(255,255,0), outline=(255,255,0))
  draw.text((left + 6, bottom - text_height - 5), name, fill=(0,0,0))

del draw

# 2) Display image
pil_image.show()

# 2) Save image
pil_image.save('most_recent_identification.jpg')