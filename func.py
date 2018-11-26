from PIL import Image,ImageDraw, ImageFilter
import cv2

def get_rect(coordinates_list): #paramater is a list
    x = []
    y = []
    for coordinate in coordinates_list:
        x.append(coordinate[0])
        y.append(coordinate[1])
    x.sort()
    y.sort()
    return ( (x[0],y[0]) , (x[-1],y[-1]) )

def landmarks_rectangle(face_landmarks): #parameter is a dict
    #returns coordinates of ((left,top),(right,bottom))
    d = {}
    for l in face_landmarks:
        d[l] = get_rect(face_landmarks[l])
    return d

def get_face_rect(lm_rect): #parameter is a dict
    x = [] #returns a list of lists [ [left,top],[right,bottom] ]
    for a in lm_rect:
        x.extend(lm_rect[a])
    rect = list(get_rect(x))
    rect.append(list(rect[0]))
    rect.append(list(rect[1]))
    rect.pop(0)
    rect.pop(0)
    return rect

def fil(org_im, draw, top,right,bottom,left,key, face_landmarks_list, n):
    lm_rect = landmarks_rectangle(face_landmarks_list[n])
    face_rect = get_face_rect(lm_rect)
    height = face_rect[1][1] - face_rect[0][1]
    width = face_rect[1][0] - face_rect[0][0]
    new_height = round(1.45 * height)
    face_rect[0][1] -= (new_height-height) #new top
    face_rect[0] = tuple(face_rect[0])
    face_rect[1] = tuple(face_rect[1])
    face_box = org_im.crop(box=(face_rect[0][0],face_rect[0][1],\
                                face_rect[1][0],face_rect[1][1]))
    if key == 0:
        return None
    elif key == ord('1'):
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        name = "THIS IS YOU"
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        return None
    elif key == ord('2'):
        # Blur the box around face
        overlay = face_box.filter(ImageFilter.GaussianBlur(radius=10))
        org_im.paste(overlay, box=(face_rect[0][0],face_rect[0][1],\
                                face_rect[1][0],face_rect[1][1]))
        return None
    elif key == ord('3'):
        #self-explanatory
        draw.polygon(face_landmarks_list[n]['left_eyebrow'],fill = (0,0,255))
        draw.polygon(face_landmarks_list[n]['right_eyebrow'],fill = (0,0,255))
        #draw.polygon(face_landmarks_list[n]['nose_bridge'],fill = (0,0,255))
        #draw.polygon(face_landmarks_list[n]['nose_tip'],fill = (0,0,255))
        draw.polygon(face_landmarks_list[n]['left_eye'],fill = (0,0,255))
        draw.polygon(face_landmarks_list[n]['right_eye'],fill = (0,0,255))
        draw.polygon(face_landmarks_list[n]['top_lip'],fill = (0,0,255))
        draw.polygon(face_landmarks_list[n]['bottom_lip'],fill = (0,0,255))
        #draw.polygon(face_landmarks_list[n]['chin'],fill = (255,255,255))
        return None
    elif key == ord('4'):
        #draw a rectangle on each of the given face landmarks
        for x in ('left_eyebrow','right_eyebrow','left_eye', \
                  'right_eye', 'top_lip', 'bottom_lip'):
            draw.rectangle((lm_rect[x][0],lm_rect[x][1]), outline = (0,0,255))
        return None
    elif key == ord('5'):
        draw.rectangle((face_rect[0],face_rect[1]), outline = (0,0,255))
    elif key == ord('6'):
        overlay = Image.open("mask.png")
        #draw.rectangle( (face_rect[0], face_rect[1]), outline = (0,0,255)
        overlay = overlay.resize((width, new_height))
        org_im.paste(overlay, face_rect[0], overlay)
        return None
