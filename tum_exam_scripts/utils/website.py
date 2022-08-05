"""
Anything related to Selenium and the printing page.
"""
from click import echo

from helium import Button, click, refresh, start_chrome, wait_until, write


def open_website_internal(user_name: str, password: str) -> None:
    """
    Use selenium to open the printing page.
    """
    start_chrome("https://ucentral.in.tum.de/cgi-bin/index.cgi")
    click("Login")
    write(user_name, "User:")
    write(password, "Password:")
    click("Login")
    click("Xerox Printing")
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
