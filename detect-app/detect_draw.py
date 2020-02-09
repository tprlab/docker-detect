import cv2 as cv

colors = [
    (250,0,0),
    (0,0,120),
    (0,0,0),
    (0,250,0),
    (220,220,0),
    (107,142,35),
    (152,251,152),
    (70,130,180),
    (220,20,60),
    (255,0,0),
    (0,0,142),
    (0,0,70),
    (0,60,100),
    (0,80,100),
    (0,0,230),
    (119,11,32),
    (70,70,70),
    (102,102,156),
    (190,153,153),
]

def get_color(idx):
    return colors[idx % len(colors)]
 

def draw_detection(img, d, draw_text=True):
    if d is None:
        return
    n = 0
    for a in d:
        clr = get_color(n)
        cv.rectangle(img, (a["x"], a["y"]), (a["x"] + a["w"], a["y"] + a["h"]), clr, thickness=2)
        word = a["name"] + "(" + str(int(100. * a["score"])) + "%)" 
        if draw_text:
            cv.putText(img, word, (a["x"] + 5, a["y"] + 25), cv.FONT_HERSHEY_SIMPLEX, 0.5, clr, 1, cv.LINE_AA)
        n += 1

