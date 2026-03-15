from playwright.sync_api import Page, expect
from shiny.playwright import controller
from shiny.pytest import create_app_fixture
from shiny.run import ShinyAppProc

app = create_app_fixture(["../src/app.py"])

def go_dashboard(page):
    page.get_by_role("tab", name="Dashboard").click()
    page.wait_for_timeout(400)

# Test year slider

def test_year_slider(page: Page, app: ShinyAppProc):
    """Test that the year range slider updates correctly."""
    page.goto(app.url)
    go_dashboard(page)
    year = controller.InputSlider(page, "year")
    year.expect_value(("2017", "2024"))