import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def get_book_details(book_url):
    """
    Fetches details (stock, category) from an individual book's page.
    Args:
        book_url (str): The full URL to the book's page.
    Returns:
        tuple: (stock_quantity (int), category (str))
    """
    try:
        # Fetch the book page
        response = requests.get(book_url)
        response.raise_for_status()

        # Parse the HTML
        book_soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Stock Availability
        stock_element = book_soup.find('p', class_='instock')
        if not stock_element:
            stock_element = book_soup.find('p', class_='outofstock')
        
        stock_text = stock_element.text.strip() if stock_element else "Availability not found"
        
        # Use regex to find a number in the stock text
        stock_match = re.search(r'\((\d+) available\)', stock_text)
        if stock_match:
            stock_quantity = int(stock_match.group(1))
        else:
            stock_quantity = 0 if 'outofstock' in stock_text.lower() else None

        # Extract Category from the breadcrumb navigation
        breadcrumb = book_soup.find('ul', class_='breadcrumb')
        if breadcrumb:
            categories = [li.a.text.strip() for li in breadcrumb.find_all('li') if li.a]
            category = categories[-1] if categories else "Uncategorized"
        else:
            category = "Uncategorized"

        return stock_quantity, category

    except requests.exceptions.RequestException as e:
        print(f"  Error fetching {book_url}: {e}")
        return None, "Error"
    except Exception as e:
        print(f"  Error parsing {book_url}: {e}")
        return None, "Error"

def scrape_books():
    base_url = "https://books.toscrape.com/"
    all_books = []
    page_num = 1
    has_next_page = True

    print("Starting to scrape books.toscrape.com...")
    
    while has_next_page:
        # Build the URL for the current page
        if page_num == 1:
            url = base_url + "catalogue/category/books_1/index.html"
        else:
            url = base_url + f"catalogue/category/books_1/page-{page_num}.html"
        print(f"\nScraping page {page_num}: {url}")

        # Fetch the page
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve page {page_num}. Stopping. Error: {e}")
            break

        # Parse the page
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        # Check if we've reached the end
        if not books:
            print("No more books found. Stopping.")
            has_next_page = False
            break

        # Process each book on the page
        for i, book in enumerate(books, 1):
            title = book.h3.a['title']
            price_text = book.find('p', class_='price_color').text
            price = float(re.sub(r'[^\d.]', '', price_text))
            
            # Map rating text to number
            rating_class = book.p['class']
            rating_text = rating_class[1] if len(rating_class) > 1 else 'Zero'
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Zero': 0}
            rating = rating_map.get(rating_text, 0)

            # Build the full book URL
            relative_link = book.h3.a['href']
            if page_num == 1:
                book_link = base_url + 'catalogue/' + relative_link.replace('../', '')
            else:
                book_link = base_url + 'catalogue/' + relative_link.replace('../../', '')

            # Get additional details
            print(f"  ({i}/{len(books)}) Getting details for: {title[:50]}...")
            stock, category = get_book_details(book_link)
            
            # Store the book data
            all_books.append({
                'title': title,
                'price': price,
                'rating': rating,
                'stock': stock,
                'category': category,
                'source': 'BooksToScrape'
            })

            # Be polite - delay between requests
            time.sleep(0.3)

        # Move to next page
        page_num += 1
        
        

    # Save the data
    if all_books:
        df = pd.DataFrame(all_books)
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        filename = f'../raw_data/books_raw_{timestamp}.csv'
        df.to_csv(filename, index=False)
        print(f"\nSuccess! Scraped {len(df)} books.")
        print(f"Data saved to: {filename}")
    else:
        print("\nNo books were scraped.")

if __name__ == '__main__':
    scrape_books()