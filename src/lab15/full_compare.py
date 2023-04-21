from sentence_transformers import SentenceTransformer, util
import statistics

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

line_numbers_1 = [3, 4, 5]
line_numbers_2 = [9, 10, 11, 12, 13]

with open('src/lab15/response.txt', 'r') as file:
    lines = file.readlines()
    response_1 = [lines[i-1].strip() for i in line_numbers_1]
    response_2 = [lines[i-1].strip() for i in line_numbers_2]

values = []

if len(line_numbers_2) <= len(line_numbers_1):
    for i in range(0, len(line_numbers_2)):
        max_val = 0.0
        for j in range(0, len(line_numbers_1)):
            embedding_1 = model.encode(response_1[j], convert_to_tensor=True)
            embedding_2 = model.encode(response_2[i], convert_to_tensor=True)

            if util.pytorch_cos_sim(embedding_1, embedding_2).item() > max_val: 
                max_val = util.pytorch_cos_sim(embedding_1, embedding_2).item()
        values.append(max_val)
else:
    for i in range(0, len(line_numbers_1)):
        max_val = 0.0
        for j in range(0, len(line_numbers_2)):
            embedding_1 = model.encode(response_1[i], convert_to_tensor=True)
            embedding_2 = model.encode(response_2[j], convert_to_tensor=True)

            if util.pytorch_cos_sim(embedding_1, embedding_2).item() > max_val: 
                max_val = util.pytorch_cos_sim(embedding_1, embedding_2).item()
        values.append(max_val)

similarity = statistics.fmean(values)

print(similarity)

# This code finds the response with the shorter number of sentences, compares each sentence in one with every sentence in the other,
# and finds the maximum similarity for that sentence. it repeats this for each sentence in the short prompt, and then averages these
# maximums together into a single value. that value is the overall similarity of the two prompts.