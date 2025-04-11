from html_telegraph_poster import TelegraphPoster

async def meme_type(message):
    if message:
        try:
            if message.photo:
                return "Photo"
            if message.audio:
                return "Audio"
            if message.voice:
                return "Voice"
            if message.video_note:
                return "Round Video"
            if message.gif:
                return "Gif"
            if message.sticker:
                mime = message.document.mime_type
                if mime == "application/x-tgsticker":
                    return "Animated Sticker"
                if mime == "video/webm":
                    return "Video Sticker"
                return "Static Sticker"
            if message.video:
                return "Video"
            if message.document:
                mime = message.document.mime_type
                if mime != "image/gif" and mime.split("/")[0] == "image":
                    return "Photo"
                if mime == "image/gif":
                    return "Gif"
                if mime.split("/")[0] == "video":
                    return "Video"
                if mime == "application/x-tgsticker":
                    return "Animated Sticker"
                return "Document"
        except AttributeError:
            return await file_type(message)
    return None


async def media_type(message):
    if message:
        try:
            if message.photo:
                return "Photo"
            if message.audio:
                return "Audio"
            if message.voice:
                return "Voice"
            if message.video_note:
                return "Round Video"
            if message.gif:
                return "Gif"
            if message.sticker:
                return "Sticker"
            if message.video:
                return "Video"
            if message.document:
                return "Document"
        except AttributeError:
            media = await file_type(message)
            if media and media in [
                "Video Sticker",
                "Animated Sticker",
                "Static Sticker",
            ]:
                return "Sticker"
            return media
    return None

async def post_to_telegraph(page_title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "JoKeRUB"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=page_title,
        author=auth_name,
        author_url="https://t.me/jepthon",
        text=html_format_content,
    )
    return post_page["url"]
