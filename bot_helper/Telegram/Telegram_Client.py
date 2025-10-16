"""
Telegram Bot - Upload & Download Handler
Professional refactored version with improved error handling and logging
"""

from config.config import Config
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeVideo
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import PeerFloodError, UserIsBlockedError
from pyrogram import Client as PyrogramClient
from pyrogram.errors import UserIsBlocked, PeerIdInvalid
from bot_helper.Others.Helper_Functions import (
    get_video_duration, 
    get_human_size, 
    get_readable_time,
    verify_rclone_account
)
from bot_helper.Telegram.Fast_Telethon import upload_file, download_file
from bot_helper.Database.User_Data import get_data
from bot_helper.Process.Running_Process import check_running_process
from bot_helper.Others.Names import Names
from bot_helper.FFMPEG.FFMPEG_Processes import FFMPEG
from bot_helper.Rclone.Rclone_Upload import upload_single_drive

from time import time
from os.path import isdir, getsize, exists
from os import makedirs
from typing import Optional, List, Tuple
from enum import Enum


# ==================== Constants ====================
class UploadMethod(Enum):
    """Upload methods enumeration"""
    TELETHON = "Telethon"
    PYROGRAM = "Pyrogram"
    USER_CLIENT = "UserClient"


class FileSize:
    """File size constants in bytes"""
    TWO_GB = 2097151000  # 2GB limit for regular accounts
    FOUR_GB = 4194304000  # 4GB limit for premium accounts


LOGGER = Config.LOGGER


# ==================== Helper Functions ====================
def create_directory(directory: str) -> None:
    """
    Create directory if it doesn't exist
    
    Args:
        directory: Path to directory
    """
    if not isdir(directory):
        makedirs(directory)
        LOGGER.info(f"Created directory: {directory}")


async def get_size_limit() -> int:
    """
    Get upload size limit based on user account type
    
    Returns:
        Size limit in bytes (2GB for regular, 4GB for premium)
    """
    size_limit = FileSize.TWO_GB
    
    if Telegram.TELETHON_USER_CLIENT:
        try:
            user = await Telegram.TELETHON_USER_CLIENT.get_me()
            if user.premium:
                size_limit = FileSize.FOUR_GB
                LOGGER.info("Premium account detected, using 4GB limit")
        except Exception as e:
            LOGGER.error(f"Error checking user premium status: {e}")
    
    return size_limit


async def get_split_size(user_id: int) -> Optional[int]:
    """
    Get split size for video splitting based on user settings
    
    Args:
        user_id: User ID
        
    Returns:
        Split size in bytes or None if splitting disabled
    """
    user_data = get_data().get(user_id, {})
    
    if not user_data.get('upload_tg', False):
        return None
    
    split_option = user_data.get('split', '2GB')
    
    if split_option == '2GB':
        return FileSize.TWO_GB
    else:
        return await get_size_limit()


def build_file_caption(filename: str, additional_info: str = "") -> str:
    """
    Build formatted file caption
    
    Args:
        filename: Name of the file
        additional_info: Additional information to include
        
    Returns:
        Formatted caption string
    """
    caption = f"**📁 Nama File**: `{filename}`"
    if additional_info:
        caption += f"\n{additional_info}"
    return caption


def build_log_caption(filename: str, user_name: str, user_id: int) -> str:
    """
    Build formatted log caption for channel
    
    Args:
        filename: Name of the file
        user_name: User's first name
        user_id: User's ID
        
    Returns:
        Formatted log caption
    """
    return (
        f"✅ **Pekerjaan Selesai**\n\n"
        f"**📁 File**: `{filename}`\n"
        f"**👤 Oleh**: {user_name} (`{user_id}`)\n"
        f"**🕐 Waktu**: {time()}"
    )


# ==================== Main Telegram Class ====================
class Telegram:
    """Main Telegram client handler"""
    
    # Initialize clients
    TELETHON_CLIENT = TelegramClient(
        Config.NAME, 
        Config.API_ID, 
        Config.API_HASH
    )
    
    PYROGRAM_CLIENT = PyrogramClient(
        f"Pyrogram_{Config.NAME}",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.TOKEN
    )
    
    # Optional user client for premium features
    TELETHON_USER_CLIENT = None
    if Config.USE_SESSION_STRING == "True":
        TELETHON_USER_CLIENT = TelegramClient(
            StringSession(Config.SESSION_STRING), 
            Config.API_ID, 
            Config.API_HASH
        )

    @staticmethod
    async def _upload_file_telethon(
        file_path: str,
        filename: str,
        process_id: str,
        process_status,
        start_time: float,
        status: str,
        use_user_client: bool = False
    ) -> Optional[object]:
        """
        Upload file using Telethon
        
        Args:
            file_path: Path to file
            filename: Name of file
            process_id: Process ID for tracking
            process_status: Process status object
            start_time: Upload start time
            status: Status message
            use_user_client: Whether to use user client (for files > 2GB)
            
        Returns:
            Uploaded file object or None
        """
        try:
            client = (Telegram.TELETHON_USER_CLIENT if use_user_client 
                     else Telegram.TELETHON_CLIENT)
            
            client_type = "UserClient" if use_user_client else "Telethon"
            
            with open(file_path, "rb") as f:
                uploaded_file = await upload_file(
                    client=client,
                    file=f,
                    name=filename,
                    check_data=process_id,
                    progress_callback=lambda c, t: process_status.telegram_update_status(
                        c, t, "Mengunggah", filename, start_time, status, client_type
                    )
                )
            
            LOGGER.info(f"File uploaded successfully via {client_type}: {filename}")
            return uploaded_file
            
        except Exception as e:
            LOGGER.error(f"Telethon upload error for {filename}: {e}")
            raise

    @staticmethod
    async def _send_file_to_user(
        user_id: int,
        uploaded_file: object,
        thumbnail: str,
        caption: str,
        duration: int,
        client,
        use_pyrogram: bool = False,
        file_path: str = None,
        process_status = None,
        start_time: float = None,
        status: str = None
    ):
        """
        Send file to user's PM
        
        Args:
            user_id: User's ID
            uploaded_file: Uploaded file object (for Telethon)
            thumbnail: Path to thumbnail
            caption: File caption
            duration: Video duration
            client: Client to use
            use_pyrogram: Whether to use Pyrogram
            file_path: File path (for Pyrogram)
            process_status: Process status object (for Pyrogram)
            start_time: Start time (for Pyrogram)
            status: Status message (for Pyrogram)
            
        Returns:
            Sent message object
        """
        try:
            if use_pyrogram:
                message = await Telegram.PYROGRAM_CLIENT.send_video(
                    chat_id=user_id,
                    video=file_path,
                    caption=caption,
                    duration=duration,
                    thumb=thumbnail,
                    progress=process_status.telegram_update_status,
                    progress_args=("Mengunggah", file_path.split("/")[-1], 
                                 start_time, status, "Pyrogram", 
                                 Telegram.PYROGRAM_CLIENT)
                )
            else:
                message = await client.send_file(
                    user_id,
                    file=uploaded_file,
                    thumb=thumbnail,
                    caption=caption,
                    attributes=(DocumentAttributeVideo(duration, 0, 0),),
                    force_document=False
                )
            
            LOGGER.info(f"File sent to user {user_id} successfully")
            return message
            
        except Exception as e:
            LOGGER.error(f"Error sending file to user {user_id}: {e}")
            raise

    @staticmethod
    async def _send_file_to_log_channel(
        log_channel_id: int,
        message_from_pm,
        log_caption: str,
        uploaded_file = None,
        thumbnail: str = None,
        duration: int = None
    ) -> bool:
        """
        Send file to log channel
        
        Args:
            log_channel_id: Log channel ID
            message_from_pm: Message object from PM
            log_caption: Caption for log
            uploaded_file: Uploaded file object (optional)
            thumbnail: Path to thumbnail (optional)
            duration: Video duration (optional)
            
        Returns:
            True if successful, False otherwise
        """
        if log_channel_id == 0:
            return False
        
        try:
            # Method 1: Forward message (fastest, preserves media type)
            await message_from_pm.forward_to(log_channel_id)
            
            # Method 2: Send with custom caption (if needed)
            # Uncomment if you want different caption in log channel
            # if uploaded_file:
            #     await Telegram.TELETHON_CLIENT.send_file(
            #         log_channel_id,
            #         file=uploaded_file,
            #         thumb=thumbnail,
            #         caption=log_caption,
            #         attributes=(DocumentAttributeVideo(duration, 0, 0),),
            #         force_document=False
            #     )
            # else:
            #     await Telegram.TELETHON_CLIENT.send_file(
            #         log_channel_id,
            #         file=message_from_pm.media,
            #         caption=log_caption,
            #         force_document=False
            #     )
            
            LOGGER.info(f"File sent to log channel {log_channel_id} successfully")
            return True
            
        except Exception as e:
            LOGGER.error(f"Failed to send file to log channel {log_channel_id}: {e}")
            return False

    @staticmethod
    async def _handle_oversized_file(
        process_status,
        file_path: str,
        filename: str,
        status: str
    ) -> bool:
        """
        Handle file upload via Rclone for oversized files
        
        Args:
            process_status: Process status object
            file_path: Path to file
            filename: Name of file
            status: Status message
            
        Returns:
            True if successful, False otherwise
        """
        user_id = process_status.user_id
        user_data = get_data().get(user_id, {})
        
        rclone_config = f'./userdata/{user_id}_rclone.conf'
        drive_name = user_data.get('drive_name')
        
        if not user_data.get('auto_drive', False):
            LOGGER.warning(f"Auto drive disabled for user {user_id}")
            return False
        
        if not exists(rclone_config):
            LOGGER.error(f"Rclone config not found: {rclone_config}")
            return False
        
        if not verify_rclone_account(rclone_config, drive_name):
            LOGGER.error(f"Invalid Rclone account for user {user_id}")
            return False
        
        try:
            await upload_single_drive(
                process_status,
                file_path,
                status,
                rclone_config,
                drive_name,
                filename
            )
            LOGGER.info(f"File uploaded to drive successfully: {filename}")
            return True
        except Exception as e:
            LOGGER.error(f"Rclone upload failed for {filename}: {e}")
            return False

    @staticmethod
    async def upload_videos_on_telegram(process_status):
        """
        Main upload handler for videos to Telegram
        
        Args:
            process_status: Process status object containing all process info
        """
        # Extract process information
        total_files = len(process_status.send_files)
        files = process_status.send_files
        user_id = process_status.user_id
        chat_id = process_status.chat_id
        event = process_status.event
        process_id = process_status.process_id
        thumbnail = process_status.thumbnail or "./thumb.jpg"
        log_channel_id = Config.LOG_CHANNEL_ID
        
        user_data = get_data().get(user_id, {})
        upload_method = user_data.get('tgupload', 'Telethon')
        size_limit = await get_size_limit()
        
        upload_successful = False
        
        LOGGER.info(f"Starting upload process for {total_files} files (User: {user_id})")

        for index, file_path in enumerate(files, start=1):
            # Check if process is still running
            if not check_running_process(process_id):
                await event.reply("🔒 **Tugas dibatalkan oleh pengguna.**")
                LOGGER.info(f"Process {process_id} cancelled by user")
                break

            # File information
            start_time = time()
            filename = file_path.split("/")[-1]
            file_size = getsize(file_path)
            duration = get_video_duration(file_path)
            status = f"{Names.STATUS_UPLOADING} [{index}/{total_files}]"
            
            file_caption = build_file_caption(
                filename, 
                f"**📊 Ukuran**: {get_human_size(file_size)}"
            )
            log_caption = build_log_caption(
                filename,
                process_status.user_first_name,
                user_id
            )
            
            LOGGER.info(f"Processing file {index}/{total_files}: {filename} ({get_human_size(file_size)})")

            message_in_pm = None
            uploaded_file = None

            try:
                # Handle oversized files with Rclone
                if file_size > size_limit:
                    LOGGER.warning(f"File {filename} exceeds size limit, attempting Rclone upload")
                    success = await Telegram._handle_oversized_file(
                        process_status, file_path, filename, status
                    )
                    if success:
                        upload_successful = True
                    else:
                        await event.reply(
                            f"❌ **File terlalu besar**: `{filename}`\n"
                            f"**Ukuran**: {get_human_size(file_size)}\n"
                            f"**Limit**: {get_human_size(size_limit)}\n\n"
                            f"Rclone upload gagal. Pastikan konfigurasi Rclone Anda benar."
                        )
                    continue

                # Upload files within size limit
                if file_size <= FileSize.TWO_GB:
                    # Use regular bot account
                    if upload_method == "Telethon":
                        uploaded_file = await Telegram._upload_file_telethon(
                            file_path, filename, process_id, process_status,
                            start_time, status, use_user_client=False
                        )
                        message_in_pm = await Telegram._send_file_to_user(
                            user_id, uploaded_file, thumbnail, file_caption,
                            duration, Telegram.TELETHON_CLIENT
                        )
                    else:  # Pyrogram
                        message_in_pm = await Telegram._send_file_to_user(
                            user_id, None, thumbnail, file_caption, duration,
                            Telegram.PYROGRAM_CLIENT, use_pyrogram=True,
                            file_path=file_path, process_status=process_status,
                            start_time=start_time, status=status
                        )
                        
                elif Telegram.TELETHON_USER_CLIENT:
                    # Use user client for files > 2GB (requires premium)
                    uploaded_file = await Telegram._upload_file_telethon(
                        file_path, filename, process_id, process_status,
                        start_time, status, use_user_client=True
                    )
                    message_in_pm = await Telegram._send_file_to_user(
                        user_id, uploaded_file, thumbnail, file_caption,
                        duration, Telegram.TELETHON_USER_CLIENT
                    )
                else:
                    await event.reply(
                        f"⚠️ **File terlalu besar untuk diunggah**: `{filename}`\n"
                        f"**Ukuran**: {get_human_size(file_size)}\n"
                        f"Diperlukan akun premium atau konfigurasi Rclone."
                    )
                    continue

                # Send to log channel if upload successful
                if message_in_pm:
                    upload_successful = True
                    
                    # Send to log channel
                    log_sent = await Telegram._send_file_to_log_channel(
                        log_channel_id,
                        message_in_pm,
                        log_caption,
                        uploaded_file,
                        thumbnail,
                        duration
                    )
                    
                    if not log_sent and log_channel_id != 0:
                        await event.reply(
                            f"⚠️ Berhasil mengirim ke PM, tapi gagal ke channel log."
                        )

            except (UserIsBlocked, UserIsBlockedError):
                error_msg = (
                    f"⚠️ **{process_status.user_first_name}**, Anda telah memblokir bot!\n\n"
                    f"Silakan buka blokir bot di PM untuk menerima hasil."
                )
                await event.reply(error_msg)
                LOGGER.warning(f"User {user_id} has blocked the bot")
                break
                
            except PeerIdInvalid:
                start_button = [
                    Button.url("🚀 Mulai Bot", f"https://t.me/{Config.BOT_USERNAME}?start=start")
                ]
                error_msg = (
                    f"⚠️ **{process_status.user_first_name}**, Anda belum memulai bot!\n\n"
                    f"Silakan klik tombol di bawah untuk memulai bot di PM."
                )
                await event.reply(error_msg, buttons=start_button)
                LOGGER.warning(f"User {user_id} hasn't started the bot")
                break
                
            except Exception as e:
                error_msg = str(e)
                await event.reply(
                    f"❌ **Gagal mengunggah**: `{filename}`\n"
                    f"**Error**: `{error_msg[:500]}`"
                )
                LOGGER.error(f"Upload error for {filename}: {error_msg}", exc_info=True)
                break

        # Send completion notification to group
        if upload_successful and event.is_group:
            try:
                notification = (
                    f"✅ **Tugas Selesai!**\n\n"
                    f"**👤 User**: {process_status.user_first_name}\n"
                    f"**📁 Files**: {total_files}\n"
                    f"**📬 Hasil**: Dikirim via PM"
                )
                if log_channel_id != 0:
                    notification += " & Channel Log"
                
                await event.reply(notification)
                LOGGER.info(f"Upload process completed for user {user_id}")
                
            except Exception as e:
                LOGGER.warning(f"Failed to send completion notification to group {chat_id}: {e}")

    @staticmethod
    async def download_tg_file(process_status, variables, dw_index: int) -> bool:
        """
        Download file from Telegram
        
        Args:
            process_status: Process status object
            variables: Variables containing event/message info
            dw_index: Download index
            
        Returns:
            True if successful, False otherwise
        """
        start_time = time()
        status = f"{Names.STATUS_DOWNLOADING} [{dw_index}]"
        new_event = variables[0]
        user_id = process_status.user_id
        user_data = get_data().get(user_id, {})
        download_method = user_data.get('tgdownload', 'Telethon')
        
        # Extract file information
        try:
            file_name = new_event.message.file.name
            file_location = new_event.message.document
            file_id = new_event.message.id
        except AttributeError:
            file_name = new_event.file.name
            file_location = new_event.document
            file_id = new_event.id
        
        # Create directory and set download location
        create_directory(process_status.dir)
        download_location = f"{process_status.dir}/{file_name}"
        process_status.append_dw_files(file_name)
        
        LOGGER.info(f"Starting download: {file_name} via {download_method}")

        try:
            if download_method == "Telethon":
                # Download using Telethon
                with open(download_location, "wb") as f:
                    await download_file(
                        client=Telegram.TELETHON_CLIENT,
                        location=file_location,
                        out=f,
                        check_data=process_status.process_id,
                        progress_callback=lambda current, total: 
                            process_status.telegram_update_status(
                                current, total, "Diunduh", file_name,
                                start_time, status, "Telethon"
                            )
                    )
                LOGGER.info(f"Downloaded successfully via Telethon: {file_name}")
                
            else:  # Pyrogram
                # Determine correct chat ID for download
                download_chat_id = (
                    Config.AUTH_GROUP_ID 
                    if process_status.event.is_group and Config.AUTH_GROUP_ID 
                    else process_status.chat_id
                )
                
                LOGGER.info(f"Downloading from chat ID: {download_chat_id}")
                
                # Get message from correct chat
                message_to_download = await Telegram.PYROGRAM_CLIENT.get_messages(
                    download_chat_id, 
                    file_id
                )
                
                # Download media
                await Telegram.PYROGRAM_CLIENT.download_media(
                    message=message_to_download,
                    file_name=download_location,
                    progress=process_status.telegram_update_status,
                    progress_args=(
                        "Diunduh", file_name, start_time, status,
                        "Pyrogram", Telegram.PYROGRAM_CLIENT
                    )
                )
                
                # Check if process was cancelled
                if not check_running_process(process_status.process_id):
                    await new_event.reply("🔒 **Tugas dibatalkan oleh pengguna.**")
                    LOGGER.info(f"Download cancelled for {file_name}")
                    return False
                
                LOGGER.info(f"Downloaded successfully via Pyrogram: {file_name}")
                
        except Exception as e:
            error_msg = str(e)
            
            if error_msg == "Cancelled":
                await new_event.reply("🔒 **Tugas dibatalkan oleh pengguna.**")
                LOGGER.info(f"Download cancelled: {file_name}")
            else:
                await new_event.reply(
                    f"❌ **Error Download {download_method}**\n\n"
                    f"**File**: `{file_name}`\n"
                    f"**Error**: `{error_msg[:500]}`\n\n"
                    f"💡 **Tips**: Pastikan bot adalah admin di chat dengan ID: `{process_status.chat_id}`"
                )
                LOGGER.error(f"Download error for {file_name}: {error_msg}", exc_info=True)
            
            return False
        
        # Move file to processed list
        process_status.move_dw_file(file_name)
        return True

    @staticmethod
    async def upload_videos(process_status):
        """
        Upload videos with optional splitting
        
        Args:
            process_status: Process status object
        """
        user_id = process_status.user_id
        user_data = get_data().get(user_id, {})
        
        # Check if video splitting is enabled
        if user_data.get('split_video', False):
            split_size = await get_split_size(user_id)
            
            if split_size:
                LOGGER.info(f"Video splitting enabled for user {user_id} (size: {get_human_size(split_size)})")
                send_files = process_status.send_files.copy()
                
                for output_file in process_status.send_files:
                    file_size = getsize(output_file)
                    
                    if file_size > split_size:
                        send_files.remove(output_file)
                        file_name = output_file.split('/')[-1]
                        
                        # Update status message
                        process_status.update_process_message(
                            f"✂️ **Memecah Video**\n"
                            f"`{file_name}`\n\n"
                            f"{process_status.get_task_details()}"
                        )
                        
                        LOGGER.info(f"Splitting file: {file_name} ({get_human_size(file_size)})")
                        
                        # Split video
                        splitted_files = await FFMPEG.split_video_file(
                            output_file,
                            split_size,
                            process_status.dir,
                            process_status.event
                        )
                        
                        if splitted_files:
                            send_files.extend(splitted_files)
                            LOGGER.info(f"File split into {len(splitted_files)} parts")
                        else:
                            LOGGER.error(f"Failed to split file: {file_name}")
                
                # Update send files list
                process_status.replace_send_list(send_files)
                LOGGER.info(f"Final file list: {send_files}")
        
        # Upload videos
        await Telegram.upload_videos_on_telegram(process_status)
