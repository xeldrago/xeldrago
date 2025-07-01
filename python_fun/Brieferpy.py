import openai
import pandas as pd

# 1. Set your OpenAI API key
openai.api_key = "your-api-key-here"

# 2. Load your Excel file
df = pd.read_excel("your_input.xlsx")  # Use full path if needed

# 3. Create a list to store GPT verdicts
verdicts = []

# 4. Loop through each row
for index, row in df.iterrows():
    # Combine all columns into one formatted prompt
    row_text = "\n".join([f"{col}: {row[col]}" for col in df.columns])
    
    # Final prompt to GPT
    prompt_text = (
        f"Based on the following details, give a concise 3–4 line verdict:\n\n"
        f"{row_text}\n\n"
        "Verdict:"
    )

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or gpt-3.5-turbo if cost/speed is a concern
        messages=[{"role": "user", "content": prompt_text}],
        temperature=0.5,
        max_tokens=200
    )

    # Extract GPT's reply
    reply = response['choices'][0]['message']['content'].strip()
    verdicts.append(reply)

# 5. Add GPT verdicts to the DataFrame
df['GPT_Verdict'] = verdicts

# 6. Save the updated data to a new Excel file
df.to_excel("gpt_output.xlsx", index=False)
