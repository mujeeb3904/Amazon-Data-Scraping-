import csv
from bs4 import BeautifulSoup  

# Load HTML content from file
with open("Amazon_laptop.html", 'r', encoding='utf-8') as file:
    content = file.read()

soup = BeautifulSoup(content, 'html.parser')

# Find all product containers
product_containers = soup.find_all('div', class_='puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v2fl5pkubaqu126k6zseo6li6q s-latency-cf-section puis-card-border')

# Prepare the CSV file
with open('amazon_laptops.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Title', 'Price', 'Rating', 'Past Sale', 'Image URL', 'Specifications']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Loop through each product container and extract details
    for i, container in enumerate(product_containers, start=1):
        # Find the title within the container
        title_tag = container.find('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')
        
        # Inside the <h2> tag, the title is inside an <a> tag and then a <span> tag
        if title_tag:
            title = title_tag.find('span', class_='a-size-medium a-color-base a-text-normal')
        else:
            title = None
        
        # Get the text if the title is found, otherwise set it to "Title not found"
        title_text = title.get_text(strip=True) if title else "Title not found"
        
        # Extract product price
        price_tag = container.find('span', class_='a-offscreen')
        price = price_tag.get_text(strip=True) if price_tag else "Price not found"
        
        # Extract product rating
        rating_tag = container.find('i', class_='a-icon a-icon-star-small a-star-small-4-5')
        
        # Rating is stored inside the <span> tag within the <i> tag
        if rating_tag:
            rating = rating_tag.find('span', class_='a-icon-alt')
        else:
            rating = None
        
        # Extract past sale information (if it exists)
        past_sale_tag = container.find("span", class_="a-size-base a-color-secondary")
        past_sale_text = past_sale_tag.get_text(strip=True) if past_sale_tag else "Past sale not found"

        # Extract product specification
        specification_tags = container.find_all("span", class_= "a-size-medium a-color-base a-text-normal")
        specifications = ", ".join([spec.get_text(strip=True) for spec in specification_tags]) if specification_tags else "Specifications not found"

        # Extract the image link of products
        image_tag = container.find("img", class_= "s-image")
        image_url = image_tag["src"] if image_tag else "Image not found"

        # Get the text if the rating is found, otherwise set it to "Rating not found"
        rating_text = rating.get_text(strip=True) if rating else "Rating not found"
        
        # Write the row to the CSV file
        writer.writerow({
            'Title': title_text,
            'Price': price,
            'Rating': rating_text,
            'Past Sale': past_sale_text,
            'Image URL': image_url,
            'Specifications': specifications
        })

print("Data has been saved to amazon_laptops.csv")
