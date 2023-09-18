import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

URL_TEMPLATE = "https://musclefit.info/otzhimaniya-ot-pola/"
EXERCISE_NAMES = "test.csv"

r = requests.get(URL_TEMPLATE)

soup = bs(r.text, "html.parser")
exercise_name = soup.find('h1').text

exercise_description = ""
description_elements = soup.find('div', class_='post-text').find_all('p')
for element in description_elements:
    exercise_description += element.text + "\n"

exercise_info = exercise_name + "\n" + exercise_description

exercise_list = [{'Exercise name': exercise_name, 'Description': exercise_description}]

df = pd.DataFrame(exercise_list)
df.to_csv(EXERCISE_NAMES, index=False)
