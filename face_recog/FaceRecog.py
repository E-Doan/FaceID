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

# show an "Open" dialog box and return the path to the selected file
# https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
group_photo = askopenfilename() 
# group_photo_name_array = group_photo.split("/")

# group_photo_name = "./img/groups/" + group_photo_name_array[-1]

# Load test image to find faces in
test_image = face_recognition.load_image_file(group_photo)

# Find faces in test image
face_locations = face_recognition.face_locations(test_image)
face_encodings = face_recognition.face_encodings(test_image, face_locations)

# Convert to PIL format
pil_image = Image.fromarray(test_image)

# Create a ImageDraw instance
draw = ImageDraw.Draw(pil_image)

# Loop through faces in test image
for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
  matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

  name = "Unknown Person"

  # If match
  if True in matches:
    first_match_index = matches.index(True)
    name = known_face_names[first_match_index]
  else:
    face_image = test_image[top:bottom, left:right]
    new_image = Image.fromarray(face_image)

    new_image.show()

    newName = input(f"What is the name of the unknown person in the previous photo?: ")
    new_image.save(f'./img/known/{newName}.jpg')
    name = newName
  
  # Draw box
  draw.rectangle(((left, top), (right, bottom)), outline=(255,255,0))

  # Draw label
  text_width, text_height = draw.textsize(name)
  draw.rectangle(((left,bottom - text_height - 10), (right, bottom)), fill=(255,255,0), outline=(255,255,0))
  draw.text((left + 6, bottom - text_height - 5), name, fill=(0,0,0))

del draw

# Display image
pil_image.show()

# # Save image
pil_image.save('most_recent_identification.jpg')