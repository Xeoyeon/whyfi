from db import CustomChroma

def load_chroma():
    chroma = CustomChroma()
    chroma.load(data_path='./word_dict.csv')