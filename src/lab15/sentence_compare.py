from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

line_numbers = [4, 11]

with open('src/lab15/response.txt', 'r') as file:
    lines = file.readlines()
    sentences = [lines[i-1].strip() for i in line_numbers]

print(sentences)

embedding_1 = model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

print(util.pytorch_cos_sim(embedding_1, embedding_2))