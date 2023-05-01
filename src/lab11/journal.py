from transformers import pipeline
import random

generator = pipeline('text-generation', model='gpt2-large')

# text = generator("I have arrived in the city of Morkomasto, it is known for", max_length=128, num_return_sequences=1)

# print(text[0]['generated_text'])

def get_journal_entry(city_name):
    prompt = []
    prompt.append("I have arrived at the city of {}, reknowned for".format(city_name))
    prompt.append("In the city of {}, known for".format(city_name))
    prompt.append("Coming to the city of {}, I feel".format(city_name))

    response = generator(prompt[random.randint(0, 2)], max_length=64, num_return_sequences=1)

    print(response[0]['generated_text'], "...")

# get_journal_entry("Gornanth")