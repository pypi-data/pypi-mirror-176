import typing
from pathlib import Path

import click
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import BrowserContext
from retry import retry
from rich import print

from . import utils


@click.command()
@click.argument("handle")
@click.option("-o", "--output-dir", "output_dir", default="./")
@click.option("-w", "--wait", "wait", default=5000)
@click.option("-x", "--width", "width", default=1300)
@click.option("-y", "--height", "height", default=1600)
@click.option(
    "-f",
    "--full-page",
    "full_page",
    is_flag=True,
    default=False,
    help="Screenshot the whole page",
)
@click.option(
    "--bundle",
    "is_bundle",
    is_flag=True,
    default=False,
    help="The provided handle is a bundle",
)
def cli(
    handle: str,
    output_dir: str = "./",
    wait: str = "5000",
    width: str = "1300",
    height: str = "1600",
    full_page: bool = False,
    is_bundle: bool = False,
):
    """Screenshot the provided homepage."""
    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if is_bundle:
        site_list = utils.get_sites_in_bundle(handle)
    else:
        site_list = [utils.get_site(handle)]

    # Open the browser
    with sync_playwright() as playwright:
        # We'll load it with an extension
        context = utils._load_persistent_context(playwright, int(width), int(height))

        # Loop through all the sites
        for site in site_list:
            # Screenshot them one by one
            _screenshot(
                context,
                site,
                output_path,
                wait=int(site["wait"] or wait),
                full_page=full_page,
            )

        # Close it out
        context.close()


@retry(tries=3, delay=5, backoff=2)
def _screenshot(
    context: BrowserContext,
    site: typing.Dict,
    output_path: Path,
    wait: int = 5000,
    full_page: bool = False,
):
    """Shoot the provided site."""
    print(f":camera: Screenshotting {site['name']}")

    # Open the page

    page = utils._load_new_page_disable_javascript(
        context=context,
        url=site["url"],
        wait_seconds=int(wait / 1000),
        handle=site["handle"],
        full_page=full_page,
    )

    # Take the screenshot
    jpeg_file_path = output_path / f"{site['handle'].lower()}.jpg"
    print(f"📥 Saving image to {jpeg_file_path}")
    page.screenshot(
        quality=80,
        type="jpeg",
        path=str(jpeg_file_path),
        full_page=full_page,
    )

    # Close the page
    page.close()


if __name__ == "__main__":
    cli()
