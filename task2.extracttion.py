import pandas as pd
import os

def load_and_clean_data (building_details):
    try:
       
        df = pd.read_csv(building_details)


        df.columns = [col.strip() for col in df.columns]

        
        df = df.rename(columns={
         'Apartment Type': 'Configuration',
        'Saleable Area (in Sqmts)': 'Area_Sqm',
        'Number of Apartment': 'Units'
        })

    
        df.dropna(subset=['Configuration', 'Area_Sqm', 'Units'], inplace=True)

    
        
        df['Area_Sqft'] = df['Area_Sqm'] * 10.7639

        df['Area_Sqft'] = df['Area_Sqft'].round(2)

        return df

    except Exception as e:
        print(f" Error loading or processing data: {e}")
        return None

def extract_and_save_summary(df):
    if df is None:
        print("No data to process.")
        return


    summary = df.groupby(['Configuration', 'Area_Sqft'], as_index=False)['Units'].sum()


    output_path = os.path.abspath('apartment_summary_sqft.csv')
    summary.to_csv(output_path, index=False)

    print(f"\n Apartment summary saved to '{output_path}'.")

    print("\n Apartment Summary (in Sqft):")
    for _, row in summary.iterrows():
        print(f"{int(row['Units'])} units of {row['Configuration']} - {row['Area_Sqft']} Sqft")

def main():
    file_path = 'building_details.csv'  
    df = load_and_clean_data(file_path)
    extract_and_save_summary(df)

if __name__ == "__main__":
    main()
