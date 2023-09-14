import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_exercise(link):
    s = requests.get(link)
    soup = bs(s.text, "html.parser")
    exercise_name = soup.find_all('h1')
    for name in exercise_name:
        return name.string


URL_TEMPLATE = "https://musclefit.info/category/uprazhneniya/grud/"
EXERCISE_NAMES = "test.csv"
r = requests.get(URL_TEMPLATE)

soup = bs(r.text, "html.parser")
exercises = soup.find_all('div', class_='title')

exercise_list = []

for el in exercises:
    exercise_link = el.a
    if exercise_link is not None:
        exercise_link = exercise_link.get('href')
        exercise_name = get_exercise(exercise_link)
        exercise_list.append({'Exercise name': exercise_name})


df = pd.DataFrame(exercise_list)
df.to_csv(EXERCISE_NAMES)
