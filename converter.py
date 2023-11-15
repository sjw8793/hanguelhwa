import pandas as pd

df = pd.read_json('testScript.json', encoding='utf-8').transpose()
print(df)
df.to_excel('testScript.xlsx')