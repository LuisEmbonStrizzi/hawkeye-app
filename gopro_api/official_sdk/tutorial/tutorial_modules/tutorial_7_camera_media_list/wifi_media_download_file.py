# wifi_media_download_file.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:05 PM

import sys
import argparse
from typing import Optional

import requests

from tutorial_modules import GOPRO_BASE_URL, get_media_list, logger


def main() -> None:
    # Get the media list
    media_list = get_media_list()

# Find the last photo with .jpg extension
    video: Optional[str] = None
    videos = [x["n"] for x in media_list["media"][0]["fs"] if x["n"].lower().endswith(".mp4")]

    if videos:
        video = videos[-1]  # Select the last photo with .jpg extension
    else:
        raise RuntimeError("Couldn't find a photo on the GoPro")

    # Resto del código es igual

    assert video is not None
    # Build the URL to get the thumbnail data for the video
    logger.info(f"Downloading {video}")
    url = GOPRO_BASE_URL + f"/videos/DCIM/100GOPRO/{video}"
    logger.info(f"Sending: {url}")
    with requests.get(url, stream=True, timeout=10) as request:
        request.raise_for_status()
        file = video.split(".")[0] + ".mp4"
        with open(file, "wb") as f:
            logger.info(f"receiving binary stream to {file}...")
            for chunk in request.iter_content(chunk_size=8192):
                f.write(chunk)

    # media_list = get_media_list()

    # # Find a photo. We're just taking the first one we find.
    # photo: Optional[str] = None
    # print(len([x["n"] for x in media_list["media"][0]["fs"]]))

    # for i, media_file in enumerate([x["n"] for x in media_list["media"][0]["fs"]]):
    #     print(i)
    #     if media_file.lower().endswith(".jpg"):
    #         logger.info(f"found a photo: {media_file}")
    #         photo = media_file
    #         break
    # else:
    #     raise RuntimeError("Couldn't find a photo on the GoPro")

    # assert photo is not None
    # # Build the url to get the thumbnail data for the photo
    # logger.info(f"Downloading {photo}")
    # url = GOPRO_BASE_URL + f"/videos/DCIM/100GOPRO/{photo}"
    # logger.info(f"Sending: {url}")
    # with requests.get(url, stream=True, timeout=10) as request:
    #     request.raise_for_status()
    #     file = photo.split(".")[0] + ".jpg"
    #     with open(file, "wb") as f:
    #         logger.info(f"receiving binary stream to {file}...")
    #         for chunk in request.iter_content(chunk_size=8192):
    #             f.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find a photo on the camera and download it to the computer.")
    parser.parse_args()

    try:
        main()
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
