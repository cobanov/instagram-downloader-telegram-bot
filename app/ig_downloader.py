import instaloader
import os
from pathlib import Path
import re
import logging

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)


class InstagramDownloader:
    def __init__(self, download_directory):
        self.loader = instaloader.Instaloader(download_video_thumbnails=False)
        self.root_dir = Path("downloads")
        self.user_dir = self.root_dir / download_directory

    def get_shortcode_from_url(self, url):
        """Extracts the shortcode from an Instagram URL."""
        match = re.search(r"instagram\.com/(?:p|reel)/([^/?]+)", url)
        if match:
            logging.warning(f"Shortcode found: {match.group(1)}")
            return match.group(1)
        else:
            logging.warning("No shortcode found in the URL.")
            return None

    def get_post_from_shortcode(self, shortcode):
        """Retrieves the post object from a shortcode."""
        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            return post
        except Exception as e:
            logging.error(f"Error retrieving post: {e}")
            return None

    def save_post(self, post):
        # Create a directory for the post
        profile_dir = self.user_dir / post.profile
        post_dir = profile_dir / post.shortcode
        post_dir.mkdir(parents=True, exist_ok=True)

        # Download the post
        self.loader.download_post(post, target=post_dir)

        # Return a list of downloaded media files
        media_files = list(post_dir.glob("*.*"))
        return media_files


def main(url):
    downloader = InstagramDownloader("downloads")
    shortcode = downloader.get_shortcode_from_url(url)
    if shortcode:
        post = downloader.get_post_from_shortcode(shortcode)
        if post:
            downloader.save_post(post)


if __name__ == "__main__":
    URL = "https://www.instagram.com/reel/Czy_sZwPsPs/"
    main(URL)
