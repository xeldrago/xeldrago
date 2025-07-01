from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')
prompt = "tell your name"
result = generator(prompt, max_length=100)
print(result[0]['generated_text'])
