import asyncio
import csv
import json
from playwright.async_api import async_playwright

async def scrape_jumia(query="query", output_format="csv", max_pages=5):
    async with async_playwright() as p:
        try:
            # Launch the browser
            browser = await p.chromium.launch(headless=False)  # Set headless=False for debugging
            page = await browser.new_page()

            # Go to the Jumia website
            await page.goto("https://www.jumia.co.ke/")

            # Wait for the search input and enter the query
            await page.wait_for_selector('input[name="q"]')
            await page.fill('input[name="q"]', query)
            await page.press('input[name="q"]', 'Enter')

            # Wait for the results to load
            await page.wait_for_selector('article.prd')

            products = []
            page_number = 1

            while page_number <= max_pages:
                print(f"Scraping page {page_number}...")

                # Wait for product elements to be stable
                await page.wait_for_selector('article.prd')

                # Extract product data
                product_elements = await page.query_selector_all('article.prd')
                for product in product_elements:
                    try:
                        title_element = await product.query_selector('.name')
                        price_element = await product.query_selector('.prc')
                        discount_element = await product.query_selector('.bdg._dsct')
                        link_element = await product.query_selector('a.core')
                        image_element = await product.query_selector('img.img')

                        title = await title_element.inner_text() if title_element else "N/A"
                        price = await price_element.inner_text() if price_element else "N/A"
                        discount = await discount_element.inner_text() if discount_element else "No discount"
                        link = await link_element.get_attribute('href') if link_element else "N/A"
                        image = await image_element.get_attribute('src') if image_element else "N/A"

                        products.append({
                            "title": title,
                            "price": price,
                            "discount": discount,
                            "link": f"https://www.jumia.co.ke{link}",
                            "image": image
                        })
                    except Exception as e:
                        print(f"Error extracting product data: {e}")
                        continue  # Skip this product and continue with the next one

                # Check if there is a next page
                next_button = await page.query_selector('a[aria-label="Next Page"]')
                if not next_button:
                    break  # Exit if there is no next page

                # Go to the next page
                await next_button.click()
                await page.wait_for_selector('article.prd')  # Wait for the next page to load
                page_number += 1

            # Close the browser
            await browser.close()

            # Save the data to a file
            if output_format == "csv":
                with open(f"{query}_products.csv", "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["title", "price", "discount", "link", "image"])
                    writer.writeheader()
                    writer.writerows(products)
            elif output_format == "json":
                with open(f"{query}_products.json", "w", encoding="utf-8") as file:
                    json.dump(products, file, indent=4)

            print(f"Scraped {len(products)} products. Data saved to {query}_products.{output_format}")

        except Exception as e:
            print(f"An error occurred: {e}")

# Run the scraper to such gas cookers as our query
# feel free to change the query to any other product you want to scrape
asyncio.run(scrape_jumia(query="gas cooker", output_format="csv", max_pages=5))