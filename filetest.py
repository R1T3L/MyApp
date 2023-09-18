import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_exercise_info(exercise_link):
    s = requests.get(exercise_link)
    soup = bs(s.text, "html.parser")
    exercise_name = soup.find('h1').text.strip()
    exercise_description_tag = soup.find('div', class_='post-text')
    exercise_description = exercise_description_tag.text.strip() if exercise_description_tag else ''
    exercise_info = exercise_name + '\n' + exercise_description
    return exercise_info


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
                exercise_info = get_exercise_info(exercise_link)
                exercise_list.append({'Exercise names': exercise_info})

        next_page_link = soup.find('a', class_='nextpostslink')
        if next_page_link:
            url_template = next_page_link.get('href')
        else:
            break

    df = pd.DataFrame(exercise_list)
    df.to_csv(output_filename)


URL_TEMPLATE = "https://musclefit.info/category/uprazhneniya/grud/"
EXERCISE_NAMES = "test2.csv"

scrape_exercises(URL_TEMPLATE, EXERCISE_NAMES)
