import pandas as pd
import numpy as np
import glob
import os

def clean_books_data():
    """Load and clean the raw books data."""
    try:
        # Find the most recent raw data file
        raw_files = glob.glob('../raw_data/books_raw_*.csv')
        if not raw_files:
            raise FileNotFoundError("No raw data files found in ../raw_data/")
        
        latest_file = max(raw_files, key=os.path.getctime)
        print(f"Loading raw data from: {latest_file}")
        
        # Load the data
        df = pd.read_csv(latest_file)
        print(f"Original data shape: {df.shape}")
        
        # 1. Handle missing values
        print("Handling missing values...")
        print(f"Missing values before cleaning:")
        print(df.isnull().sum())
        
        df['category'] = df['category'].fillna('Unknown')
        df['stock'] = df['stock'].fillna(0)
        
        # 2. Clean text data
        print("Cleaning text data...")
        df['title'] = df['title'].str.strip().str.title()
        df['category'] = df['category'].str.strip()
        
        # 3. Ensure correct data types
        print("Ensuring correct data types...")
        df['rating'] = df['rating'].astype(int)
        df['stock'] = df['stock'].astype(int)
        
        # 4. Fix pd.cut() - Handle edge cases for price bins
        print("Creating price categories...")
        
        # Check if we have any price data
        if df['price'].isnull().all():
            print("Warning: No price data found!")
            df['price_category'] = 'Unknown'
        else:
            # Handle NaN prices
            df['price'] = df['price'].fillna(df['price'].median())
            
            # Create bins that work with your data range
            price_min = df['price'].min()
            price_max = df['price'].max()
            
            # Dynamic bin creation based on actual data range
            if price_max > 100:
                bins = [0, 10, 25, 50, 100, price_max + 1]
                labels = ['Cheap', 'Affordable', 'Expensive', 'Premium', 'Luxury']
            else:
                # If prices are lower, adjust bins
                bins = [0, 5, 15, 30, 50, price_max + 1]
                labels = ['Very Cheap', 'Cheap', 'Affordable', 'Expensive', 'Premium']
            
            df['price_category'] = pd.cut(df['price'], bins=bins, labels=labels, include_lowest=True)
        
        # 5. Create availability column
        df['availability'] = np.where(df['stock'] > 0, 'In Stock', 'Out of Stock')
        
        # 6. Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['title'])
        final_count = len(df)
        print(f"Removed {initial_count - final_count} duplicate entries.")
        
        # 7. Save cleaned data
        output_path = '../cleaned_data/cleaned_books_data.csv'
        df.to_csv(output_path, index=False)
        print(f"Cleaning complete! Data saved to: {output_path}")
        print(f"Final dataset shape: {df.shape}")
        print(f"Missing values after cleaning:")
        print(df.isnull().sum())
        
        return df
        
    except Exception as e:
        print(f"Error during data cleaning: {e}")
        print("Trying alternative loading method...")
        return clean_books_data_simple()

def clean_books_data_simple():
    """Simplified version for troubleshooting"""
    try:
        # Try to find any CSV file in raw_data
        raw_files = glob.glob('../raw_data/*.csv')
        if not raw_files:
            raise FileNotFoundError("No CSV files found in raw_data folder")
        
        # Just use the first file found
        input_file = raw_files[0]
        print(f"Loading data from: {input_file}")
        
        df = pd.read_csv(input_file)
        print(f"Loaded data shape: {df.shape}")
        
        # Basic cleaning
        df = df.fillna({'category': 'Unknown', 'stock': 0, 'rating': 0})
        df['title'] = df['title'].str.strip().str.title()
        
        # Save cleaned data
        output_path = '../cleaned_data/cleaned_books_data.csv'
        df.to_csv(output_path, index=False)
        print(f"Simple cleaning complete! Data saved to: {output_path}")
        
        return df
        
    except Exception as e:
        print(f"Error in simple cleaning: {e}")
        return None

if __name__ == '__main__':
    clean_books_data()