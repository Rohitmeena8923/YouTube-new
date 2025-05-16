import re
import asyncio
import logging
from pytube import YouTube, Search
from pytube.exceptions import PytubeError
from telegram import Update
from telegram.ext import ContextTypes

class YouTubeService:
    @staticmethod
    def sanitize_filename(title: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "", title)[:50]

    @staticmethod
    async def search_videos(query: str, max_results: int = 10) -> list[dict]:
        try:
            results = Search(query).results[:max_results]
            return [{
                "id": video.video_id,
                "title": video.title,
                "thumbnail": video.thumbnail_url,
                "channel": video.author,
            } for video in results]
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return []

    @staticmethod
    async def download_video(video_url: str, quality: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        try:
            yt = YouTube(
                video_url,
                on_progress_callback=lambda s, c, r: 
                    YouTubeService.progress_callback(s, r, update, context)
            )
            
            stream = (
                yt.streams.get_audio_only() if quality == "audio" else
                yt.streams.filter(res=quality, progressive=True).first() or
                yt.streams.get_highest_resolution()
            )

            filename = f"{YouTubeService.sanitize_filename(yt.title)}_{quality}.mp4"
            filepath = f"data/downloads/{filename}"
            
            stream.download(filename=filepath)
            return filepath

        except PytubeError as e:
            logging.error(f"Download failed: {e}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Download error: {str(e)}"
            )
            return None

    @staticmethod
    def progress_callback(stream, remaining, update, context):
        total = stream.filesize
        downloaded = total - remaining
        percent = (downloaded / total) * 100
        
        if percent % 5 < 0.1 or remaining == 0:
            progress = "[" + "=" * int(percent//10) + ">" + " " * (10 - int(percent//10)) + "]"
            message = f"Downloading: {progress} {percent:.1f}%"
            
            asyncio.run_coroutine_threadsafe(
                context.bot.edit_message_text(
                    message,
                    chat_id=update.effective_chat.id,
                    message_id=context.user_data.get("progress_msg_id"),
                ),
                context.application.create_task,
            )