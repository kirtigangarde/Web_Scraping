import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape product information
def scrape_amazon_products(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Lists to store product information
    products = []

    # Find all product containers
    for item in soup.find_all("div", class_="s-result-item"):
        try:
            # Extract product name
            name = item.find("span", class_="a-text-normal").text.strip()

            # Extract product price
            price = item.find("span", class_="a-price-whole")
            price = price.text.strip() if price else "N/A"

            # Extract product rating
            rating = item.find("span", class_="a-icon-alt")
            rating = rating.text.strip() if rating else "N/A"

            # Append product details to the list
            products.append({
                "Name": name,
                "Price": price,
                "Rating": rating
            })
        except AttributeError:
            continue

    return products

# Function to save data to a CSV file
def save_to_csv(data, filename="products.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function
def main():
    # URL of the Amazon search results page (replace with the desired URL)
    url = "https://www.amazon.com/s?k=laptops"

    # Scrape product information
    products = scrape_amazon_products(url)

    # Save the data to a CSV file
    save_to_csv(products)

if __name__ == "__main__":
    main()