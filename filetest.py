import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_exercise_name(exercise_link):
    s = requests.get(exercise_link)
    soup = bs(s.text, "html.parser")
    exercise_name = soup.find_all('h1')
    for name in exercise_name:
        return name.string


def scrape_exercises(url_template, output_filename):
    exercise_list = []

    while True:
        r = requests.get(url_template)
        soup = bs(r.text, "html.parser")
        exercises = soup.find_all('div', class_='title')

        for el in exercises:
            exercise_link = el.a
            if exercise_link is not None:
                exercise_link = exercise_link.get('href')
                exercise_name = get_exercise_name(exercise_link)
                exercise_list.append({'Exercise names': exercise_name})

        next_page_link = soup.find('a', class_='nextpostslink')
        if next_page_link:
            url_template = next_page_link.get('href')
        else:
            break

    df = pd.DataFrame(exercise_list)
    df.to_csv(output_filename)


URL_TEMPLATE = "https://musclefit.info/category/uprazhneniya/grud/"
EXERCISE_NAMES = "test1.csv"

scrape_exercises(URL_TEMPLATE, EXERCISE_NAMES)
