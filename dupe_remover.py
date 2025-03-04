import pandas
import os

def remove_duplicates():
    df = pandas.read_csv("data/champion_data.csv")
    df = df.drop_duplicates(subset=['name'], keep='first')
    df.to_csv("data/champion_data.csv", index=False)

remove_duplicates()