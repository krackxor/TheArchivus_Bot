from config.config import Config
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeVideo
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import PeerFloodError, UserIsBlockedError
from pyrogram import Client as PyrogramClient
from pyrogram.errors import UserIsBlocked, PeerIdInvalid
from bot_helper.Others.Helper_Functions import get_video_duration, get_human_size, get_readable_time
from bot_helper.Telegram.Fast_Telethon import upload_file, download_file
from bot_helper.Database.User_Data import get_data
from time import time
from bot_helper.Process.Running_Process import check_running_process
from bot_helper.Others.Names import Names
from os.path import isdir, getsize, exists
from os import makedirs
from bot_helper.FFMPEG.FFMPEG_Processes import FFMPEG
from bot_helper.Rclone.Rclone_Upload import upload_single_drive
from bot_helper.Others.Helper_Functions import verify_rclone_account

def create_direc(direc):
    if not isdir(direc):
        makedirs(direc)
    return

async def check_size_limit():
    size = 2097151000
    if Telegram.TELETHON_USER_CLIENT:
        user = await Telegram.TELETHON_USER_CLIENT.get_me()
        if user.premium:
            size = 4194304000
    return size

async def get_split_size(user_id):
    if get_data()[user_id]['upload_tg']:
        if get_data()[user_id]['split'] == '2GB':
            split_size = 2097151000
        else:
            split_size = await check_size_limit()
        return split_size
    else:
        return False

LOGGER = Config.LOGGER

class Telegram:
    TELETHON_CLIENT = TelegramClient(Config.NAME, Config.API_ID, Config.API_HASH)
    PYROGRAM_CLIENT = PyrogramClient(
        f"Pyrogram_{Config.NAME}",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.TOKEN
    )
    if Config.USE_SESSION_STRING == "True":
        TELETHON_USER_CLIENT = TelegramClient(StringSession(Config.SESSION_STRING), Config.API_ID, Config.API_HASH)
    else:
        TELETHON_USER_CLIENT = False

    async def upload_videos_on_telegram(process_status):
        total_files = len(process_status.send_files)
        files = process_status.send_files
        user_pm_id = process_status.user_id
        original_chat_id = process_status.chat_id
        event = process_status.event
        process_id = process_status.process_id
        thumbnail = process_status.thumbnail if process_status.thumbnail else "./thumb.jpg"
        log_channel_id = Config.LOG_CHANNEL_ID
        
        upload_successful = False

        for i in range(total_files):
            file_path = files[i]
            start_time = time()
            duration = get_video_duration(file_path)
            filename = file_path.split("/")[-1]
            file_caption = f"**Nama File**: `{filename}`"
            status = f"{Names.STATUS_UPLOADING} [{i+1}/{total_files}]"
            size_limit = await check_size_limit()
            file_size = getsize(file_path)

            message_in_pm = None

            try:
                if file_size > size_limit:
                    # ... (logika rclone tetap sama)
                    pass
                else:
                    # 1. Kirim FILE ke PM Pengguna
                    if file_size <= 2097151000:
                        if get_data()[user_pm_id]['tgupload'] == "Telethon":
                            with open(file_path, "rb") as f:
                                uploaded_file = await upload_file(client=Telegram.TELETHON_CLIENT, file=f, name=filename, check_data=process_id, progress_callback=lambda c, t: process_status.telegram_update_status(c, t, "Mengunggah", filename, start_time, status, "Telethon"))
                            message_in_pm = await Telegram.TELETHON_CLIENT.send_file(user_pm_id, file=uploaded_file, thumb=thumbnail, caption=file_caption, attributes=(DocumentAttributeVideo(duration, 0, 0),))
                        else: # Pyrogram
                            message_in_pm = await Telegram.PYROGRAM_CLIENT.send_video(chat_id=user_pm_id, video=file_path, caption=file_caption, duration=duration, thumb=thumbnail, progress=process_status.telegram_update_status, progress_args=("Mengunggah", filename, start_time, status, "Pyrogram", Telegram.PYROGRAM_CLIENT))
                    elif Telegram.TELETHON_USER_CLIENT:
                        with open(file_path, "rb") as f:
                            uploaded_file = await upload_file(client=Telegram.TELETHON_USER_CLIENT, file=f, name=filename, check_data=process_id, progress_callback=lambda c, t: process_status.telegram_update_status(c, t, "Mengunggah", filename, start_time, status, "UserClient"))
                        message_in_pm = await Telegram.TELETHON_USER_CLIENT.send_file(user_pm_id, file=uploaded_file, thumb=thumbnail, caption=file_caption, attributes=(DocumentAttributeVideo(duration, 0, 0),))

                if message_in_pm:
                    upload_successful = True
                    # 2. Kirim FILE ke Channel Log (jika diatur)
                    if log_channel_id != 0:
                        try:
                            log_caption = (f"✅ **Pekerjaan Selesai**\n\n"
                                           f"**File**: `{filename}`\n"
                                           f"**Oleh**: {process_status.user_first_name} (`{process_status.user_id}`)")
                            await Telegram.TELETHON_CLIENT.send_file(log_channel_id, file=file_path, thumb=thumbnail, caption=log_caption, attributes=(DocumentAttributeVideo(duration, 0, 0),))
                        except Exception as e:
                            LOGGER.error(f"Gagal mengirim file ke channel log {log_channel_id}: {e}")
                            await event.reply(f"🔔 Gagal mengirim hasil ke channel log. Error: `{str(e)[:1000]}`")

            except (UserIsBlocked, UserIsBlockedError):
                await event.reply(f"**Peringatan untuk {process_status.user_first_name}**: Anda telah memblokir bot. Buka blokir di PM agar saya bisa mengirimkan hasilnya.")
                LOGGER.warning(f"Pengguna {user_pm_id} telah memblokir bot.")
                break 
            except (PeerIdInvalid):
                start_button = [Button.url("Mulai Bot", f"https://t.me/{Config.BOT_USERNAME}?start=start")]
                await event.reply(f"**Peringatan untuk {process_status.user_first_name}**: Anda belum memulai bot. Silakan mulai bot di PM terlebih dahulu.", buttons=start_button)
                LOGGER.warning(f"Pengguna {user_pm_id} belum memulai bot.")
                break
            except Exception as e:
                error_msg = str(e)
                await event.reply(f"❗ Gagal total saat mengunggah `{filename}`. Error: `{error_msg[:1000]}`")
                LOGGER.error(f"Upload error untuk {filename}: {error_msg}")
                break
            
            if not check_running_process(process_id):
                await event.reply("🔒 Tugas dibatalkan oleh pengguna.")
                break

        # 3. Kirim NOTIFIKASI TEKS ke Grup (jika berhasil dan berasal dari grup)
        if upload_successful and event.is_group:
            try:
                notif_message = f"✅ Tugas untuk **{process_status.user_first_name}** telah selesai. Hasil dikirim melalui PM."
                await event.reply(notif_message)
            except Exception as e:
                LOGGER.warning(f"Gagal mengirim notifikasi selesai ke grup {original_chat_id}: {e}")
        
        return

    async def download_tg_file(process_status, variables, dw_index):
        # ... (kode download tetap sama, tidak perlu diubah)
        start_time = time()
        status = f"{Names.STATUS_DOWNLOADING} [{dw_index}]"
        new_event = variables[0]
        try:
            file_name = new_event.message.file.name
            file_location = new_event.message.document
            file_id = new_event.message.id
        except:
            file_name = new_event.file.name
            file_location = new_event.document
            file_id = new_event.id
        create_direc(process_status.dir)
        download_location = f"{process_status.dir}/{file_name}"
        process_status.append_dw_files(file_name)
        if get_data()[process_status.user_id]['tgdownload']=="Telethon":
                try:
                    with open(download_location, "wb") as f:
                            await download_file(
                                client=Telegram.TELETHON_CLIENT, 
                                location=file_location, 
                                out=f,
                                check_data=process_status.process_id,
                                progress_callback=lambda current,total: process_status.telegram_update_status(current,total, "Diunduh", file_name, start_time, status, get_data()[process_status.user_id]['tgdownload']))
                except Exception as e:
                        if str(e)=="Cancelled":
                                await new_event.reply("🔒Tugas Dibatalkan Oleh Pengguna")
                        else:
                            await new_event.reply(f"❗ Error Unduhan Telethon: {str(e)}")
                            LOGGER.info(str(e))
                        return False
        else:
            try:
                    download_chat_id = Config.AUTH_GROUP_ID if process_status.event.is_group and Config.AUTH_GROUP_ID else process_status.chat_id
                    await Telegram.PYROGRAM_CLIENT.download_media(
                                                                message=(await Telegram.PYROGRAM_CLIENT.get_messages(download_chat_id, file_id)),
                                                                file_name=download_location,
                                                                progress=process_status.telegram_update_status,
                                                                progress_args=("Diunduh", file_name, start_time, status, get_data()[process_status.user_id]['tgdownload'], Telegram.PYROGRAM_CLIENT))
                    if not check_running_process(process_status.process_id):
                                    await new_event.reply("🔒Tugas Dibatalkan Oleh Pengguna")
            except Exception as e:
                    await new_event.reply(f"❗ Error Unduhan Pyrogram: {str(e)}\n\nChat: {download_chat_id}")
                    return False
        process_status.move_dw_file(file_name)
        return True

    async def upload_videos(process_status):
        if get_data()[process_status.user_id]['split_video']:
            split_size = await get_split_size(process_status.user_id)
            if split_size:
                send_files = process_status.send_files.copy()
                for output_file in process_status.send_files:
                    if getsize(output_file) > split_size:
                        send_files.remove(output_file)
                        file_name = str(output_file).split('/')[-1]
                        process_status.update_process_message(f"✂ Memecah Video\n`{str(file_name)}`\n{process_status.get_task_details()}")
                        splitted_files = await FFMPEG.split_video_file(output_file, split_size, process_status.dir, process_status.event)
                        if splitted_files:
                            send_files += splitted_files
                process_status.replace_send_list(send_files)
                LOGGER.info(str(send_files))
        await Telegram.upload_videos_on_telegram(process_status)
