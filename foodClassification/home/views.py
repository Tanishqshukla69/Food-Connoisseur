from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from home.forms import UploadFileForm
from home.models import File_upload
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import requests

app_id = '22a2102b'
api_key = "cb9908fb7c0f1d777e0c794ca564f6e1"
model = load_model('./savedModel/model_v1_inceptionV3.h5')
category = {
    0: ['burger', 'Burger'], 1: ['butter_naan', 'Butter Naan'], 2: ['chai', 'Chai'],
    3: ['chapati', 'Chapati'], 4: ['chole_bhature', 'Chole Bhature'], 5: ['dal_makhani', 'Dal Makhani'],
    6: ['dhokla', 'Dhokla'], 7: ['fried_rice', 'Fried Rice'], 8: ['idli', 'Idli'], 9: ['jalegi', 'Jalebi'],
    10: ['kathi_rolls', 'Kaathi Rolls'], 11: ['kadai_paneer', 'Kadai Paneer'], 12: ['kulfi', 'Kulfi'],
    13: ['masala_dosa', 'Masala Dosa'], 14: ['momos', 'Momos'], 15: ['paani_puri', 'Paani Puri'],
    16: ['pakode', 'Pakode'], 17: ['pav_bhaji', 'Pav Bhaji'], 18: ['pizza', 'Pizza'], 19: ['samosa', 'Samosa']
}


def predict_image(img_, model):
    # img_ = image.load_img(filename, target_size=(299, 299))
    img_array = image.img_to_array(img_)
    img_processed = np.expand_dims(img_array, axis=0)
    img_processed /= 255.
    prediction = model.predict(img_processed)
    index = np.argmax(prediction)
    return category[index][1]


result = ""


def index(request):
    if request.method == 'POST':
        c_form = UploadFileForm(request.POST, request.FILES)
        if c_form.is_valid():
            my_file = request.FILES['file']
            img = Image.open(my_file)
            img.resize((299, 299))
            result = predict_image(img, model)
            factsurl = f"https://api.edamam.com/search?q={result}&app_id=22a2102b&app_key=cb9908fb7c0f1d777e0c794ca564f6e1&to=2"
            facts = requests.get(factsurl)
            facts = facts.json()
            facts = facts['hits'][0]
            ingredients = facts['recipe']['ingredientLines']
            recipeurl = facts['recipe']['url']
            imageurl = facts['recipe']['totalNutrients']
            return render(request, 'answer.html', {'result': result, 'ingredients': facts['recipe']['ingredientLines'], 'recipe': facts['recipe']['url'], 'Nutrients': facts['recipe']['totalNutrients']})
    else:
        content = {
            'forms': UploadFileForm()
        }
    return render(request, 'index.html', content)
