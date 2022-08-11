"""
Anything related to Selenium and the printing page.
"""
from click import echo
from click.exceptions import Exit

from helium import (
    Button,
    click,
    refresh,
    start_chrome,
    start_firefox,
    wait_until,
    write,
)
from tum_exam_scripts.enums import Browser


def open_website_internal(user_name: str, password: str, browser: Browser) -> None:
    """
    Use selenium to open the printing page.
    """
    url = "https://ucentral.in.tum.de/cgi-bin/index.cgi"
    if browser == Browser.CHROME:
        start_chrome(url)
    elif browser == Browser.FIREFOX:
        start_firefox(url)
    else:
        echo(f"Browser {browser} is not supported!")
        raise Exit(1)
    click("Login")
    write(user_name, "User:")
    write(password, "Password:")
    click("Login")
    wait_until(Button("Logout").exists, timeout_secs=5)
    click("Xerox Printing")
    wait_until(Button("Laden").exists, timeout_secs=5)
    refresh()
    try:
        wait_until(
            Button("Diesen Rechner zum Drucken freischalten").is_enabled, timeout_secs=5
        )
        click("Diesen Rechner zum Drucken freischalten")
        refresh()
        click("Diesen Rechner zum Drucken freischalten")
    except LookupError:
        echo("We can already print from this machine")
    echo("NOTE: Keep the browser window open!")
