from googletrans import Translator


def translate(text):
    translator = Translator()
    result = translator.translate(text, src='en', dest='pl')
    return result


#https://stackoverflow.com/questions/1614059/how-to-make-python-speak