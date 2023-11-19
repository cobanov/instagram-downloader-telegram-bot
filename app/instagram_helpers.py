import logging
from ig_downloader import InstagramDownloader


async def download_and_send_instagram_post(url, update, context):
    username = update.message.from_user["username"]
    downloader = InstagramDownloader(username)
    shortcode = downloader.get_shortcode_from_url(url)
    if not shortcode:
        await update.message.reply_text("Invalid Instagram URL.")
        return
    else:
        await update.message.reply_text(
            "Download initiation in progress, kindly await completion."
        )
    post = downloader.get_post_from_shortcode(shortcode)
    if not post:
        await update.message.reply_text("Failed to download the post.")
        return

    file_paths = downloader.save_post(post)
    if not isinstance(file_paths, list):
        file_paths = [file_paths]

    try:
        for file_path in file_paths:
            await send_media(file_path, update, context)
        await update.message.reply_text("Downloaded and sent successfully!")
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        await update.message.reply_text("Error sending the downloaded file.")


async def send_media(file_path, update, context):
    file_path_str = str(file_path)
    with open(file_path, "rb") as file:
        if file_path_str.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)
        elif file_path_str.lower().endswith(".mp4"):
            with open(file_path, "rb") as video:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=video,
                    connect_timeout=1000,
                    read_timeout=1000,
                    write_timeout=1000,
                    pool_timeout=1000,
                )

        else:
            logging.info(f"Skipping non-image/video file: {file_path_str}")
