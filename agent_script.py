from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/")

    while True:
        quotes = page.query_selector_all(".quote")
        for quote in quotes:
            text = quote.query_selector(".text").inner_text()
            author = quote.query_selector(".author").inner_text()
            print(f"{text} — {author}")

        next_button = page.query_selector("li.next > a")

        if next_button:
            print("\n--- Page suivante ---\n")
            next_button.click()
            page.wait_for_selector(".quote")
        else:
            break

    print("\nScraping terminé.")
    browser.close()