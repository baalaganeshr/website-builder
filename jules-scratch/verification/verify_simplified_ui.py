from playwright.sync_api import sync_playwright, expect

def log_request(request):
    print(f">> {request.method} {request.url}")

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.on("request", log_request)

        # Navigate to the python http server on port 8081
        page.goto("http://localhost:8081", timeout=60000)

        # Wait for the main heading to be visible
        heading = page.get_by_role("heading", name="Local AI Website Builder")
        expect(heading).to_be_visible()

        # Take a screenshot of the initial UI
        page.screenshot(path="jules-scratch/verification/simplified-ui.png")

        browser.close()

if __name__ == "__main__":
    run_verification()
