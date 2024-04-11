from taipy.gui import Gui
# ----
from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
import cv2


labels = {0: u'bathtub', 1: u'c', 2: u'geyser', 3: u'mirror', 4: u'showerhead', 5: u'sink', 6: u'toilet', 7: u'towel', 8: u'washbasin', 9: u'wc', 10: u'none'}
scores ={0: 70,  # Bathtub
        1: 50,  # 'c' idk wtf is this
        2: 60,  # Geyser is imp
        3: 80,  # Mirrors are op
        4: 60,  # Showerhead is ok, but not imp when shitting
        5: 90,  # Sink is a S+
        6: 100,  # Not imp
        7: 40,  # Towels
        8: 80,  # Washbasin
        9: 100,  # 'wc'
        10: 0}  # 'none'

model = YOLO("model/best.pt")

def calculate_score(results):
        score = 0
        for key, value in labels.items():
            if value in results:
                score = score + scores[key]

        score = (score*100.0)/730.0
        return score

def predict_image(model, path_to_img):
    img = Image.open(path_to_img)
    results = model(img)

    class_id = results[0].boxes.cls.numpy()
    
    classes = set()
    for i in class_id:
        classes.add(labels[i])

    top_prob = calculate_score(classes)
    top_pred = classes
    
    return top_prob, top_pred


content = ""
img_path = "input.png"
prob = 0
pred = ""

# <|{"input.png"}|image|width=25vw|>
index = """
<|text-center|

Select the image from your file system: 
<|{content}|file_selector|extensions=.png|>


<|{pred}|>

<|{img_path}|image|>

Score of the Toilet: 

<|{prob}|indicator|value={prob}|min=0|max=100|width=25vw|>

>
"""


def on_change(state, var_name, var_val):
    if var_name == "content":
        top_prob, top_pred = predict_image(model, var_val)
        # top_prob, top_pred = 0.1, 'hello'
        state.prob = top_prob
        state.pred = "Image contains: " + str(top_pred)
        state.img_path = var_val

 
app = Gui(page=index)

if __name__ == "__main__":
    app.run(use_reloader=True,title="TAIPY demo")