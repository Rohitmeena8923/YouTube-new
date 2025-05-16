import asyncio
import time
from typing import Dict, List, Optional
from pytube import YouTube, Search, Stream
from pytube.exceptions import PytubeError
from telegram import Update
from telegram.ext import ContextTypes

class YouTubeService:
    """Handles all YouTube-related operations"""
    
    @staticmethod
    async def search_videos(query: str, max_results: int = 10) -> List[Dict]:
        try:
            search_results = Search(query).results[:max_results]
            return [
                {
                    "id": video.video_id,
                    "title": video.title,
                    "thumbnail": video.thumbnail_url,
                    "channel": video.author,
                }
                for video in search_results
            ]
        except Exception as e:
            raise Exception(f"YouTube search failed: {e}")

    @staticmethod
    async def get_video_info(video_id: str) -> Optional[Dict]:
        try:
            yt = YouTube(f"https://youtube.com/watch?v={video_id}")
            return {
                "id": video_id,
                "title": yt.title,
                "duration": str(yt.length),
                "thumbnail": yt.thumbnail_url,
            }
        except Exception as e:
            raise Exception(f"Failed to get video info: {e}")

    @staticmethod
    async def download_video(
        video_url: str,
        quality: str,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> Optional[str]:
        try:
            yt = YouTube(video_url)
            chat_id = update.effective_chat.id

            def progress_callback(stream, chunk, bytes_remaining):
                total_size = stream.filesize
                bytes_downloaded = total_size - bytes_remaining
                percent = (bytes_downloaded / total_size) * 100
                
                if percent % 5 < 0.1 or bytes_remaining == 0:
                    speed = (bytes_downloaded / (time.time() - start_time)) / 1024
                    progress_bar = "[" + "=" * int(percent // 10) + ">" + " " * (10 - int(percent // 10)) + "]"
                    message = (
                        f"Downloading: {progress_bar} {percent:.1f}%\n"
                        f"Speed: {speed:.1f} KB/s\n"
                        f"Size: {bytes_downloaded/1024/1024:.1f}MB / {total_size/1024/1024:.1f}MB"
                    )
                    
                    asyncio.run_coroutine_threadsafe(
                        context.bot.edit_message_text(
                            message,
                            chat_id=chat_id,
                            message_id=progress_message.message_id,
                        ),
                        context.application.create_task,
                    )

            yt.register_on_progress_callback(progress_callback)

            if quality == "audio":
                stream = yt.streams.get_audio_only()
            else:
                stream = yt.streams.filter(res=quality, progressive=True).first()
                if not stream:
                    stream = yt.streams.get_highest_resolution()

            if not stream:
                raise Exception("No suitable stream found")

            progress_message = await context.bot.send_message(chat_id, "Starting download...")
            global start_time
            start_time = time.time()

            file_path = stream.download(output_path="data/downloads")
            return file_path

        except Exception as e:
            raise Exception(f"Download failed: {e}")