import pandas as pd
import cohere


cohere_api_key = "SO7Y4JwCSLRoEOqk0peW9wnBekiZnBIMCawI8llb" 
co = cohere.Client('SO7Y4JwCSLRoEOqk0peW9wnBekiZnBIMCawI8llb')


input_file = "apartment_summary_sqft.csv"
try:
    data = pd.read_csv(input_file)
except FileNotFoundError:
    print(f" File not found: {input_file}")
    exit()



buyer_personas = []

for index, row in data.iterrows():
    try:
        config = row['Configuration']
        area = row['Area_Sqft']

        prompt = (
         f"What is the typical buyer persona for an apartment with these details:\n"
          f"- Configuration: {config}\n"
        f"- Saleable Area: {area} SqFt\n"
            f"Include age range, profession, lifestyle, and family type."
        )

        response = co.generate(
           model='command-light', 
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
        )
        buyer_personas.append(response.generations[0].text.strip())

    except KeyError as e:
        print(f"Missing column in row {index}: {e}")
        buyer_personas.append("Error")
    except Exception as e:
        print(f"Error for row {index} ({config}, {area}): {e}")
        buyer_personas.append("Error")


data['Buyer_Persona'] = buyer_personas


output_file = "buyer_personas_from_cohere.csv"
data.to_csv(output_file, index=False)

print(f" Buyer personas saved to: {output_file}")