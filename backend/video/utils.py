# Extract HTML content from the completion string
import base64
import io
import mimetypes
import os
import tempfile
import uuid
from typing import Any, Union, cast
# from moviepy.editor import VideoFileClip  # type: ignore  # Temporarily disabled for Ollama-only
from PIL import Image
import math


DEBUG = True
TARGET_NUM_SCREENSHOTS = (
    20  # Should be max that Claude supports (20) - reduce to save tokens on testing
)


async def assemble_claude_prompt_video(video_data_url: str) -> list[Any]:
    images = split_video_into_screenshots(video_data_url)

    # Save images to tmp if we're debugging
    if DEBUG:
        save_images_to_tmp(images)

    # Validate number of images
    print(f"Number of frames extracted from video: {len(images)}")
    if len(images) > 20:
        print(f"Too many screenshots: {len(images)}")
        raise ValueError("Too many screenshots extracted from video")

    # Convert images to the message format for Claude
    content_messages: list[dict[str, Union[dict[str, str], str]]] = []
    for image in images:

        # Convert Image to buffer
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")

        # Encode bytes as base64
        base64_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
        media_type = "image/jpeg"

        content_messages.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_data,
                },
            }
        )

    return [
        {
            "role": "user",
            "content": content_messages,
        },
    ]


# Returns a list of images/frame (RGB format)
def split_video_into_screenshots(video_data_url: str) -> list[Image.Image]:
    # Temporarily disabled for Ollama-only setup
    # This function requires moviepy which has complex dependencies
    print("Video processing temporarily disabled for Ollama-only setup")
    return []  # Return empty list as placeholder


# Save a list of PIL images to a random temporary directory
def save_images_to_tmp(images: list[Image.Image]):

    # Create a unique temporary directory
    unique_dir_name = f"screenshots_{uuid.uuid4()}"
    tmp_screenshots_dir = os.path.join(tempfile.gettempdir(), unique_dir_name)
    os.makedirs(tmp_screenshots_dir, exist_ok=True)

    for idx, image in enumerate(images):
        # Generate a unique image filename using index
        image_filename = f"screenshot_{idx}.jpg"
        tmp_filepath = os.path.join(tmp_screenshots_dir, image_filename)
        image.save(tmp_filepath, format="JPEG")

    print("Saved to " + tmp_screenshots_dir)


def extract_tag_content(tag: str, text: str) -> str:
    """
    Extracts content for a given tag from the provided text.

    :param tag: The tag to search for.
    :param text: The text to search within.
    :return: The content found within the tag, if any.
    """
    tag_start = f"<{tag}>"
    tag_end = f"</{tag}>"
    start_idx = text.find(tag_start)
    end_idx = text.find(tag_end, start_idx)
    if start_idx != -1 and end_idx != -1:
        return text[start_idx : end_idx + len(tag_end)]
    return ""
