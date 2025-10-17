from telethon import events
from telethon.tl.custom import Button
from config.config import Config
from bot_helper.Others.Helper_Functions import delete_all, get_config, get_env_dict, export_env_file
from bot_helper.Database.User_Data import get_data, new_user, saveconfig, saveoptions, resetdatabase
from os.path import exists
from bot_helper.Telegram.Telegram_Client import Telegram

#////////////////////////////////////Variables////////////////////////////////////#
sudo_users = Config.SUDO_USERS
encoders_list = ['libx265', 'libx264']
# CRF kustom
crf_list = ['22', '24', '26', 'Kustom']
wsize_list =['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
presets_list =  ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
bool_list = [True, False]
# Posisi watermark baru dengan ikon
ws_name = {
    '5:5': '↖', 
    '(main_w-overlay_w)/2:5': '⬆', 
    'main_w-overlay_w-5:5': '↗',
    '5:(main_h-overlay_h)/2': '⬅',
    '(main_w-overlay_w)/2:(main_h-overlay_h)/2': '⏺',
    'main_w-overlay_w-5:(main_h-overlay_h)/2': '➡',
    '5:main_h-overlay_h-5': '↙',
    '(main_w-overlay_w)/2:main_h-overlay_h-5': '⬇',
    'main_w-overlay_w-5:main_h-overlay_h-5': '↘'
}
ws_value = {v: k for k, v in ws_name.items()}
TELETHON_CLIENT = Telegram.TELETHON_CLIENT
punc = ['!', '|', '{', '}', ';', ':', "'", '=', '"', '\\', ',', '<', '>', '/', '?', '@', '#', '$', '%', '^', '&', '*', '~', "  ", "\t", "+", "b'", "'"]
SAVE_TO_DATABASE = Config.SAVE_TO_DATABASE
LOGGER = Config.LOGGER


#////////////////////////////////////Callbacks////////////////////////////////////#
@TELETHON_CLIENT.on(events.CallbackQuery)
async def callback(event):
        txt = event.data.decode()
        chat_id = event.chat.id
        user_id = event.sender.id
        if user_id not in get_data():
            await new_user(user_id, SAVE_TO_DATABASE)
        
        if txt.startswith("settings"):
            text = f"⚙ Hi {get_mention(event)} Choose Your Settings"
            await event.edit(text, buttons=[
            [Button.inline('#️⃣ General', 'general_settings')],
            [Button.inline('❣ Telegram', 'telegram_settings')],
            [Button.inline('📝 Progress Bar', 'progress_settings')],
            [Button.inline('🏮 Compression', 'compression_settings')],
            [Button.inline('🛺 Watermark', 'watermark_settings')],
            [Button.inline('🍧 Merge', 'merge_settings')],
            [Button.inline('🚜 Convert', 'convert_settings')],
            [Button.inline('🚍 HardMux', 'hardmux_settings')],
            [Button.inline('🎮 SoftMux', 'softmux_settings')],
            [Button.inline('🛩SoftReMux', 'softremux_settings')],
            [Button.inline('⭕Close Settings', 'close_settings')]
        ])
            return
        
        elif txt=="close_settings":
            await event.delete()
            return
        
        elif txt.startswith("resetdb"):
            new_position = eval(txt.split("_", 1)[1])
            if new_position:
                reset = await resetdatabase(SAVE_TO_DATABASE)
                if reset:
                    text = f"✔Database Reset Successfull"
                else:
                    text = f"❌Database Reset Failed"
                await event.answer(text, alert=True)
            else:
                await event.answer(f"Why You Wasting My Time.", alert=True)
            return
        
        
        elif txt.startswith("env"):
            position = txt.split("_", 1)[1]
            value_result = await get_text_data(chat_id, user_id, event, 120, f"Send New Value For Variable {position}")
            if value_result:
                if exists("./userdata/botconfig.env"):
                    config_dict = get_env_dict('./userdata/botconfig.env')
                else:
                    config_dict = get_env_dict('config.env')
                config_dict[position] = value_result.message.message
                export_env_file("./userdata/botconfig.env", config_dict)
                await value_result.reply(f"✅{position} Value Changed Successfully, Restart Bot To Reflect Changes.")
            return
        
        
        elif txt.startswith("renew"):
            new_position = eval(txt.split("_", 1)[1])
            if new_position:
                if exists(Config.DOWNLOAD_DIR):
                    await delete_all(Config.DOWNLOAD_DIR)
                    text = f"✔Successfully Deleted {Config.DOWNLOAD_DIR}"
                    try:
                            await event.answer(text, alert=True)
                    except:
                        await event.edit(text)
                else:
                    await event.answer(f"Nothing to clear 🙄", alert=True)
                    return
            else:
                await event.answer(f"Why You Wasting My Time.", alert=True)
                return
        
        
        elif txt.startswith("general"):
            await general_callback(event, txt, user_id, chat_id)
            return
        
        elif txt.startswith("telegram"):
            await telegram_callback(event, txt, user_id, chat_id)
            return
        
        elif txt.startswith("progress"):
            await progress_callback(event, txt, user_id)
            return
        
        
        elif txt.startswith("compression"):
            await compress_callback(event, txt, user_id, True)
            return

        elif txt.startswith("convert"):
            await convert_callback(event, txt, user_id, True)
            return
        
        elif txt.startswith("hardmux"):
            await hardmux_callback(event, txt, user_id, True)
            return
        
        elif txt.startswith("softmux"):
            await softmux_callback(event, txt, user_id, True)
            return
        
        elif txt.startswith("softremux"):
            await softremux_callback(event, txt, user_id, True)
            return
        
        elif txt.startswith("merge"):
            await merge_callback(event, txt, user_id)
            return
        
        
        elif txt.startswith("watermark"):
            await watermark_callback(event, txt, user_id, True)
            return
        
        
        elif txt=="nik66bots":
            await event.answer(f"⚡Bot By Sahil⚡", alert=True)
            return
        
        
        elif txt.startswith("change"):
            if "_queue_size" in txt:
                queue_size_input= await get_text_data(chat_id, user_id, event, 120, "Send Queue Size")
                if queue_size_input:
                    try:
                        queue_size = int(queue_size_input.message.message)
                    except:
                        await queue_size_input.reply("❗Invalid Input")
                        return
                    if txt=="change_compress_queue_size":
                        await saveconfig(user_id, 'compress', 'queue_size', str(queue_size), SAVE_TO_DATABASE)
                        await compress_callback(event, "compression_settings", user_id, False)
                    elif txt=="change_watermark_queue_size":
                        await saveconfig(user_id, 'watermark', 'queue_size', str(queue_size), SAVE_TO_DATABASE)
                        await watermark_callback(event, "watermark_settings", user_id, False)
                    elif txt=="change_convert_queue_size":
                        await saveconfig(user_id, 'convert', 'queue_size', str(queue_size), SAVE_TO_DATABASE)
                        await convert_callback(event, "convert_settings", user_id, False)
                    elif txt=="change_hardmux_queue_size":
                        await saveconfig(user_id, 'hardmux', 'queue_size', str(queue_size), SAVE_TO_DATABASE)
                        await hardmux_callback(event, "hardmux_settings", user_id, False)
            return
        
        
        elif txt=="custom_metedata":
            cmetadata = get_data()[user_id]['metadata']
            await event.answer(f"✅Current Metadata: {str(cmetadata)}", alert=True)
            return
        
        
        return


#////////////////////////////////////Functions////////////////////////////////////#
def get_mention(event):
    return "["+event.sender.first_name+"](tg://user?id="+str(event.sender.id)+")"

def gen_keyboard(values_list, current_value, callvalue, items, hide):
    boards = []
    lists = len(values_list)//items
    if lists!=len(values_list)/items:
        lists +=1
    current_list = []
    for x in values_list:
        if len(current_list)==items:
            boards.append(current_list)
            current_list = []
        value = f"{str(callvalue)}_{str(x)}"
        if str(current_value) != str(x):
            if callvalue!="watermarkposition":
                text = f"{str(x)}"
            else:
                text = f"{str(ws_name[x])}"
        else:
            if not hide:
                if callvalue!="watermarkposition":
                    text = f"{str(x)} 🟢"
                else:
                    text = f"{str(ws_name[x])} 🟢"
            else:
                text = f"🟢"
        keyboard = Button.inline(text, value)
        current_list.append(keyboard)
    boards.append(current_list)
    return boards


async def get_metadata(chat_id, user_id, event, timeout, message):
    async with TELETHON_CLIENT.conversation(chat_id) as conv:
            handle = conv.wait_event(events.NewMessage(chats=chat_id, incoming=True, from_users=[user_id], func=lambda e: e.message.message), timeout=timeout)
            ask = await event.reply(f'*️⃣ {str(message)} [{str(timeout)} secs]')
            try:
                new_event = await handle
            except Exception as e:
                await ask.reply('🔃Timed Out! Tasked Has Been Cancelled.')
                LOGGER.info(e)
                return False
            metadata = new_event.message.message
            for ele in punc:
                if ele in metadata:
                        metadata = metadata.replace(ele, '')
            return metadata


async def get_text_data(chat_id, user_id, event, timeout, message):
    async with TELETHON_CLIENT.conversation(chat_id) as conv:
            handle = conv.wait_event(events.NewMessage(chats=chat_id, incoming=True, from_users=[user_id], func=lambda e: e.message.message), timeout=timeout)
            ask = await event.reply(f'*️⃣ {str(message)} [{str(timeout)} secs]')
            try:
                new_event = await handle
            except Exception as e:
                await ask.reply('🔃Timed Out! Tasked Has Been Cancelled.')
                LOGGER.info(e)
                return False
            return new_event


#////////////////////////////////////Callbacks_Functions////////////////////////////////////#


###############------General------###############
async def telegram_callback(event, txt, user_id, chat_id):
            new_position = txt.split("_", 1)[1]
            if txt.startswith("telegramupload"):
                await saveoptions(user_id, 'tgupload', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Telegram Upload Client - {str(new_position)}")
            elif txt.startswith("telegramdownload"):
                await saveoptions(user_id, 'tgdownload', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Telegram Download Client - {str(new_position)}")
            telegram_upload = get_data()[user_id]['tgupload']
            telegram_download = get_data()[user_id]['tgdownload']
            KeyBoard = []
            KeyBoard.append([Button.inline(f'🔼Telegram Upload Client - {str(telegram_upload)}', 'nik66bots')])
            for board in gen_keyboard(["Telethon", "Pyrogram"], telegram_upload, "telegramupload", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🔽Telegram Download Client - {str(telegram_download)}', 'nik66bots')])
            for board in gen_keyboard(["Telethon", "Pyrogram"], telegram_download, "telegramdownload", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            try:
                await event.edit("⚙ Telegram Settings", buttons=KeyBoard)
            except:
                pass
            return

###############------General------###############
async def general_callback(event, txt, user_id, chat_id):
            new_position = txt.split("_", 1)[1]
            r_config = f'./userdata/{str(user_id)}_rclone.conf'
            check_config = exists(r_config)
            drive_name = get_data()[user_id]['drive_name']
            edit = True
            if txt.startswith("generalselectstream"):
                await saveoptions(user_id, 'select_stream', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Auto Select Audio - {str(new_position)}")
            elif txt.startswith("generalstream"):
                await saveoptions(user_id, 'stream', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Select Audio - {str(new_position)}")
            elif txt.startswith("generalsplitvideo"):
                await saveoptions(user_id, 'split_video', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Split Video - {str(new_position)}")
            elif txt.startswith("generalsplit"):
                await saveoptions(user_id, 'split', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Split Size - {str(new_position)}")
            elif txt.startswith("generalcustomthumbnail"):
                await saveoptions(user_id, 'custom_thumbnail', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Dynamic Thumbnail - {str(new_position)}")
            elif txt.startswith("generalcustommetadata"):
                if eval(new_position):
                        metadata = await get_metadata(chat_id, user_id, event, 120, "Send Metadata Title")
                        if metadata:
                            await saveoptions(user_id, 'metadata', metadata, SAVE_TO_DATABASE)
                            edit = False
                        else:
                            return
                await saveoptions(user_id, 'custom_metadata', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Custom Metadata - {str(new_position)}")
            elif txt.startswith("generaluploadtg"):
                if not eval(new_position):
                    if not (check_config and drive_name):
                        await event.answer(f"❗First Save Rclone ConfigFile/Account", alert=True)
                        return
                await saveoptions(user_id, 'upload_tg', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Upload On TG - {str(new_position)}")
            elif txt.startswith("generaldrivename"):
                await saveoptions(user_id, 'drive_name', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Rclone Account - {str(new_position)}")
            elif txt.startswith("generalautodrive"):
                if eval(new_position):
                    if not (check_config and drive_name):
                        await event.answer(f"❗First Save Rclone ConfigFile/Account", alert=True)
                        return
                await saveoptions(user_id, 'auto_drive', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Auto Upload Big File To Drive - {str(new_position)}")
            elif txt.startswith("generalgenss"):
                await saveoptions(user_id, 'gen_ss', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Generate Screenshots - {str(new_position)}")
            elif txt.startswith("generalssno"):
                await saveoptions(user_id, 'ss_no', int(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅No Of Screenshots - {str(new_position)}")
            elif txt.startswith("generalgensample"):
                await saveoptions(user_id, 'gen_sample', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Generate Sample Video - {str(new_position)}")
            elif txt.startswith("generaluploadall"):
                await saveoptions(user_id, 'upload_all', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Upload Every Multi Task File - {str(new_position)}")
            elif txt.startswith("generalmultitasks"):
                await saveoptions(user_id, 'multi_tasks', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Multi Tasks - {str(new_position)}")
            select_stream = get_data()[user_id]['select_stream']
            stream = get_data()[user_id]['stream']
            split_video = get_data()[user_id]['split_video']
            split = get_data()[user_id]['split']
            upload_tg = get_data()[user_id]['upload_tg']
            custom_metadata = get_data()[user_id]['custom_metadata']
            custom_thumbnail = get_data()[user_id]['custom_thumbnail']
            drive_name = get_data()[user_id]['drive_name']
            auto_drive = get_data()[user_id]['auto_drive']
            gen_ss = get_data()[user_id]['gen_ss']
            ss_no = get_data()[user_id]['ss_no']
            gen_sample = get_data()[user_id]['gen_sample']
            multi_tasks = get_data()[user_id]['multi_tasks']
            upload_all = get_data()[user_id]['upload_all']
            # rclone = get_data()[user_id]['rclone']
            KeyBoard = []
            KeyBoard.append([Button.inline(f'🥝Auto Select Audio - {str(select_stream)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, select_stream, "generalselectstream", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍭Select Audio - {str(stream)}', 'nik66bots')])
            for board in gen_keyboard(['ENG', 'HIN'], stream, "generalstream", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🪓Split Video - {str(split_video)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, split_video, "generalsplitvideo", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🛢Split Size - {str(split)}', 'nik66bots')])
            for board in gen_keyboard(['2GB', '4GB'], split, "generalsplit", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🖼Dynamic Thumbnail - {str(custom_thumbnail)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, custom_thumbnail, "generalcustomthumbnail", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🪀Custom Metadata - {str(custom_metadata)} [Click To See]', 'custom_metedata')])
            for board in gen_keyboard(bool_list, custom_metadata, "generalcustommetadata", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🧵Upload On TG - {str(upload_tg)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, upload_tg, "generaluploadtg", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🕹Auto Upload Big File To Drive - {str(auto_drive)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, auto_drive, "generalautodrive", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'📷Generate Screenshots - {str(gen_ss)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, gen_ss, "generalgenss", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🎶No Of Screenshots - {str(ss_no)}', 'nik66bots')])
            for board in gen_keyboard([3,5,7,10], ss_no, "generalssno", 4, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🎞Generate Sample Video - {str(gen_sample)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, gen_sample, "generalgensample", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🛰Multi Tasks - {str(multi_tasks)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, multi_tasks, "generalmultitasks", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'⏹Upload Every Multi Task File - {str(upload_all)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, upload_all, "generaluploadall", 2, False):
                KeyBoard.append(board)
            if check_config:
                accounts = await get_config(r_config)
                if accounts:
                    KeyBoard.append([Button.inline(f'🔮Rclone Account - {str(drive_name)}', 'nik66bots')])
                    for board in gen_keyboard(accounts, drive_name, "generaldrivename", 2, False):
                        KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            if edit:
                try:
                    await event.edit("⚙ General Settings", buttons=KeyBoard)
                except:
                    pass
            else:
                await TELETHON_CLIENT.send_message(chat_id, "⚙ General Settings", buttons=KeyBoard)
            return

###############------Progress------###############
async def progress_callback(event, txt, user_id):
            new_position = txt.split("_", 1)[1]
            KeyBoard = []
            if txt.startswith("progressdetailedprogress"):
                await saveoptions(user_id, 'detailed_messages', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Show Detailed Messages - {str(new_position)}")
            elif txt.startswith("progressshowstats"):
                await saveoptions(user_id, 'show_stats', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Show Stats - {str(new_position)}")
            elif txt.startswith("progressupdatetime"):
                await saveoptions(user_id, 'update_time', int(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Progress Update Time - {str(new_position)} secs")
            elif txt.startswith("progressffmpegsize"):
                await saveoptions(user_id, 'ffmpeg_size', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Show FFMPEG Output File Size - {str(new_position)}")
            elif txt.startswith("progressffmpegptime"):
                await saveoptions(user_id, 'ffmpeg_ptime', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Show Process Time - {str(new_position)}")
            elif txt.startswith("progressshowtime"):
                await saveoptions(user_id, 'show_time', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Show Current Time - {str(new_position)}")
            detailed_messages = get_data()[user_id]['detailed_messages']
            show_stats = get_data()[user_id]['show_stats']
            update_time = get_data()[user_id]['update_time']
            ffmpeg_size = get_data()[user_id]['ffmpeg_size']
            ffmpeg_ptime = get_data()[user_id]['ffmpeg_ptime']
            show_time = get_data()[user_id]['show_time']
            KeyBoard.append([Button.inline(f'📋Show Detailed Messages - {str(detailed_messages)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, detailed_messages, "progressdetailedprogress", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'📊Show Stats - {str(show_stats)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, show_stats, "progressshowstats", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'📀Show FFMPEG Output File Size - {str(ffmpeg_size)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, ffmpeg_size, "progressffmpegsize", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'⏲Show Process Time- {str(ffmpeg_ptime)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, ffmpeg_ptime, "progressffmpegptime", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'⌚Show Current Time- {str(show_time)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, show_time, "progressshowtime", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'⏱Progress Update Time - {str(update_time)} secs', 'nik66bots')])
            for board in gen_keyboard([5, 6, 7, 8, 9, 10], update_time, "progressupdatetime", 3, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            try:
                await event.edit("⚙ Progress Bar Settings", buttons=KeyBoard)
            except:
                pass
            return

###############------Compress------###############
async def compress_callback(event, txt, user_id, edit):
            new_position = txt.split("_", 1)[1]
            KeyBoard = []
            if txt.startswith("compressionencoder"):
                await saveconfig(user_id, 'compress', 'encoder', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Compress Encoder - {str(new_position)}")
            elif txt.startswith("compressionpreset"):
                await saveconfig(user_id, 'compress', 'preset', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Compress Preset - {str(new_position)}")
            elif txt.startswith("compressioncopysub"):
                await saveconfig(user_id, 'compress', 'copy_sub', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Compress Copy Subtitles - {str(new_position)}")
            elif txt.startswith("compressionmap"):
                await saveconfig(user_id, 'compress', 'map', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Compress Map - {str(new_position)}")
            elif txt.startswith("compressioncrf"):
                if new_position == "Kustom":
                    crf_input = await get_text_data(event.chat.id, user_id, event, 120, "Masukkan nilai CRF kustom (0-51)")
                    if crf_input:
                        try:
                            crf_value = int(crf_input.message.message)
                            if 0 <= crf_value <= 51:
                                await saveconfig(user_id, 'compress', 'crf', str(crf_value), SAVE_TO_DATABASE)
                                await event.answer(f"✅Compress CRF Kustom - {crf_value}")
                            else:
                                await crf_input.reply("❗Nilai CRF harus antara 0 dan 51.")
                        except ValueError:
                            await crf_input.reply("❗Input tidak valid, masukkan angka.")
                else:
                    await saveconfig(user_id, 'compress', 'crf', new_position, SAVE_TO_DATABASE)
                    await event.answer(f"✅Compress CRF - {str(new_position)}")
            elif txt.startswith("compressionusequeuesize"):
                await saveconfig(user_id, 'compress', 'use_queue_size', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Compress Use Queue Size - {str(new_position)}")
            elif txt.startswith("compressionsync"):
                await saveconfig(user_id, 'compress', 'sync', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Compress Use SYNC - {str(new_position)}")
            compress_encoder = get_data()[user_id]['compress']['encoder']
            compress_preset = get_data()[user_id]['compress']['preset']
            compress_crf = get_data()[user_id]['compress']['crf']
            compress_map = get_data()[user_id]['compress']['map']
            compress_copysub = get_data()[user_id]['compress']['copy_sub']
            compress_use_queue_size = get_data()[user_id]['compress']['use_queue_size']
            compress_queue_size = get_data()[user_id]['compress']['queue_size']
            compress_sync = get_data()[user_id]['compress']['sync']
            KeyBoard.append([Button.inline(f'🍬Encoder - {str(compress_encoder)}', 'nik66bots')])
            for board in gen_keyboard(encoders_list, compress_encoder, "compressionencoder", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍄Copy Subtitles - {str(compress_copysub)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, compress_copysub, "compressioncopysub", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍓Map  - {str(compress_map)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, compress_map, "compressionmap", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'📻Use FFMPEG Queue Size  - {str(compress_use_queue_size)}', 'nik66bots')])
            if compress_use_queue_size:
                KeyBoard.append([Button.inline(f'🎹FFMPEG Queue Size Value  - {str(compress_queue_size)} (Click To Change)', 'change_compress_queue_size')])
            for board in gen_keyboard(bool_list, compress_use_queue_size, "compressionusequeuesize", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🌳Use SYNC - {str(compress_sync)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, compress_sync, "compressionsync", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'♒Preset - {str(compress_preset)}', 'nik66bots')])
            for board in gen_keyboard(presets_list, compress_preset, "compressionpreset", 3, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'⚡CRF  - {str(compress_crf)}', 'nik66bots')])
            for board in gen_keyboard(crf_list, compress_crf, "compressioncrf", 4, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline('🎵 Audio', 'compression_audio_settings')])
            KeyBoard.append([Button.inline('📝 Metadata', 'compression_metadata_settings')])
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            if edit:
                try:
                    await event.edit("⚙ Compression Settings", buttons=KeyBoard)
                except:
                    pass
            else:
                try:
                    await event.delete()
                except:
                    pass
                await Telegram.TELETHON_CLIENT.send_message(event.chat.id, "⚙ Compression Settings", buttons=KeyBoard)
            return

###############------Watermark------###############
async def watermark_callback(event, txt, user_id, edit):
            new_position = txt.split("_", 1)[1]
            KeyBoard = []
            if txt.startswith("watermarkencoder"):
                await saveconfig(user_id, 'watermark', 'encoder', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Encoder - {str(new_position)}")
            elif txt.startswith("watermarkencode"):
                await saveconfig(user_id, 'watermark', 'encode', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Use Encoder - {str(new_position)}")
            elif txt.startswith("watermarkposition"):
                await saveconfig(user_id, 'watermark', 'position', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Position - {str(ws_name[new_position])}")
            elif txt.startswith("watermarksize"):
                await saveconfig(user_id, 'watermark', 'size', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Size - {str(new_position)}")
            elif txt.startswith("watermarkpreset"):
                await saveconfig(user_id, 'watermark', 'preset', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Preset - {str(new_position)}")
            elif txt.startswith("watermarkcopysub"):
                await saveconfig(user_id, 'watermark', 'copy_sub', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Copy Subtitles - {str(new_position)}")
            elif txt.startswith("watermarkmap"):
                await saveconfig(user_id, 'watermark', 'map', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Map - {str(new_position)}")
            elif txt.startswith("watermarkcrf"):
                if new_position == "Kustom":
                    crf_input = await get_text_data(event.chat.id, user_id, event, 120, "Masukkan nilai CRF kustom (0-51)")
                    if crf_input:
                        try:
                            crf_value = int(crf_input.message.message)
                            if 0 <= crf_value <= 51:
                                await saveconfig(user_id, 'watermark', 'crf', str(crf_value), SAVE_TO_DATABASE)
                                await event.answer(f"✅Watermark CRF Kustom - {crf_value}")
                            else:
                                await crf_input.reply("❗Nilai CRF harus antara 0 dan 51.")
                        except ValueError:
                            await crf_input.reply("❗Input tidak valid, masukkan angka.")
                else:
                    await saveconfig(user_id, 'watermark', 'crf', new_position, SAVE_TO_DATABASE)
                    await event.answer(f"✅Watermark CRF - {str(new_position)}")
            elif txt.startswith("watermarkusequeuesize"):
                await saveconfig(user_id, 'watermark', 'use_queue_size', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Use Queue Size - {str(new_position)}")
            elif txt.startswith("watermarksync"):
                await saveconfig(user_id, 'watermark', 'sync', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Watermark Use SYNC - {str(new_position)}")
            watermark_position = get_data()[user_id]['watermark']['position']
            watermark_size = get_data()[user_id]['watermark']['size']
            watermark_encoder = get_data()[user_id]['watermark']['encoder']
            watermark_encode = get_data()[user_id]['watermark']['encode']
            watermark_preset = get_data()[user_id]['watermark']['preset']
            watermark_crf = get_data()[user_id]['watermark']['crf']
            watermark_map = get_data()[user_id]['watermark']['map']
            watermark_copysub = get_data()[user_id]['watermark']['copy_sub']
            watermark_use_queue_size = get_data()[user_id]['watermark']['use_queue_size']
            watermark_queue_size = get_data()[user_id]['watermark']['queue_size']
            watermark_sync = get_data()[user_id]['watermark']['sync']
            KeyBoard.append([Button.inline(f'🥽Position - {str(ws_name[watermark_position])}', 'nik66bots')])
            for board in gen_keyboard(list(ws_name.keys()), watermark_position, "watermarkposition", 3, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🛸Size - {str(watermark_size)}', 'nik66bots')])
            for board in gen_keyboard(wsize_list, watermark_size, "watermarksize", 6, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🎧Use Encoder - {str(watermark_encode)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, watermark_encode, "watermarkencode", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍬Encoder - {str(watermark_encoder)}', 'nik66bots')])
            for board in gen_keyboard(encoders_list, watermark_encoder, "watermarkencoder", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍄Copy Subtitles - {str(watermark_copysub)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, watermark_copysub, "watermarkcopysub", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍓Map  - {str(watermark_map)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, watermark_map, "watermarkmap", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'📻Use FFMPEG Queue Size  - {str(watermark_use_queue_size)}', 'nik66bots')])
            if watermark_use_queue_size:
                KeyBoard.append([Button.inline(f'🎹FFMPEG Queue Size Value  - {str(watermark_queue_size)} (Click To Change)', 'change_watermark_queue_size')])
            for board in gen_keyboard(bool_list, watermark_use_queue_size, "watermarkusequeuesize", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🌳Use SYNC - {str(watermark_sync)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, watermark_sync, "watermarksync", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'♒Preset - {str(watermark_preset)}', 'nik66bots')])
            for board in gen_keyboard(presets_list, watermark_preset, "watermarkpreset", 3, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'⚡CRF  - {str(watermark_crf)}', 'nik66bots')])
            for board in gen_keyboard(crf_list, watermark_crf, "watermarkcrf", 4, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline('🎵 Audio', 'watermark_audio_settings')])
            KeyBoard.append([Button.inline('📝 Metadata', 'watermark_metadata_settings')])
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            if edit:
                try:
                    await event.edit("⚙ Watermark Settings", buttons=KeyBoard)
                except:
                    pass
            else:
                try:
                    await event.delete()
                except:
                    pass
                await Telegram.TELETHON_CLIENT.send_message(event.chat.id, "⚙ Watermark Settings", buttons=KeyBoard)
            return


###############------Merge------###############
async def merge_callback(event, txt, user_id):
            new_position = txt.split("_", 1)[1]
            KeyBoard = []
            if txt.startswith("mergemap"):
                await saveconfig(user_id, 'merge', 'map', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Merge Map - {str(new_position)}")
            elif txt.startswith("mergefixblank"):
                await saveconfig(user_id, 'merge', 'fix_blank', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Merge Fix Blank - {str(new_position)}")
            merge_map = get_data()[user_id]['merge']['map']
            merge_fix_blank = get_data()[user_id]['merge']['fix_blank']
            KeyBoard.append([Button.inline(f'🍓Map  - {str(merge_map)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, merge_map, "mergemap", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🚢Fix Blank Outro  - {str(merge_fix_blank)} [Use Only When Necessary]', 'nik66bots')])
            for board in gen_keyboard(bool_list, merge_fix_blank, "mergefixblank", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline('🎵 Audio', 'merge_audio_settings')])
            KeyBoard.append([Button.inline('📝 Metadata', 'merge_metadata_settings')])
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            try:
                await event.edit("⚙ Merge Settings", buttons=KeyBoard)
            except:
                pass
            return

###############------Convert------###############
async def convert_callback(event, txt, user_id, edit):
            new_position = txt.split("_", 1)[1]
            KeyBoard = []
            if txt.startswith("convertencoder"):
                await saveconfig(user_id, 'convert', 'encoder', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Convert Encoder - {str(new_position)}")
            elif txt.startswith("convertencode"):
                await saveconfig(user_id, 'convert', 'encode', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Convert Use Encoder - {str(new_position)}")
            elif txt.startswith("convertpreset"):
                await saveconfig(user_id, 'convert', 'preset', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Convert Preset - {str(new_position)}")
            elif txt.startswith("convertcopysub"):
                await saveconfig(user_id, 'convert', 'copy_sub', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Convert Copy Subtitles - {str(new_position)}")
            elif txt.startswith("convertmap"):
                await saveconfig(user_id, 'convert', 'map', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Convert Map - {str(new_position)}")
            elif txt.startswith("convertcrf"):
                if new_position == "Kustom":
                    crf_input = await get_text_data(event.chat.id, user_id, event, 120, "Masukkan nilai CRF kustom (0-51)")
                    if crf_input:
                        try:
                            crf_value = int(crf_input.message.message)
                            if 0 <= crf_value <= 51:
                                await saveconfig(user_id, 'convert', 'crf', str(crf_value), SAVE_TO_DATABASE)
                                await event.answer(f"✅Convert CRF Kustom - {crf_value}")
                            else:
                                await crf_input.reply("❗Nilai CRF harus antara 0 dan 51.")
                        except ValueError:
                            await crf_input.reply("❗Input tidak valid, masukkan angka.")
                else:
                    await saveconfig(user_id, 'convert', 'crf', new_position, SAVE_TO_DATABASE)
                    await event.answer(f"✅Convert CRF - {str(new_position)}")
            elif txt.startswith("convertusequeuesize"):
                await saveconfig(user_id, 'convert', 'use_queue_size', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Convert Use Queue Size - {str(new_position)}")
            elif txt.startswith("convertsync"):
                await saveconfig(user_id, 'convert', 'sync', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Convert Use SYNC - {str(new_position)}")
            elif txt.startswith("convertlist"):
                await saveconfig(user_id, 'convert', 'convert_list', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Convert Qualities - {str(new_position)}")
            convert_encoder = get_data()[user_id]['convert']['encoder']
            convert_encode = get_data()[user_id]['convert']['encode']
            convert_preset = get_data()[user_id]['convert']['preset']
            convert_crf = get_data()[user_id]['convert']['crf']
            convert_map = get_data()[user_id]['convert']['map']
            convert_copysub = get_data()[user_id]['convert']['copy_sub']
            convert_use_queue_size = get_data()[user_id]['convert']['use_queue_size']
            convert_queue_size = get_data()[user_id]['convert']['queue_size']
            convert_sync = get_data()[user_id]['convert']['sync']
            convert_list = get_data()[user_id]['convert']['convert_list']
            KeyBoard.append([Button.inline(f'🎧Use Encoder - {str(convert_encode)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, convert_encode, "convertencode", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍬Encoder - {str(convert_encoder)}', 'nik66bots')])
            for board in gen_keyboard(encoders_list, convert_encoder, "convertencoder", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍄Copy Subtitles - {str(convert_copysub)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, convert_copysub, "convertcopysub", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍓Map  - {str(convert_map)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, convert_map, "convertmap", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'📻Use FFMPEG Queue Size  - {str(convert_use_queue_size)}', 'nik66bots')])
            if convert_use_queue_size:
                KeyBoard.append([Button.inline(f'🎹FFMPEG Queue Size Value  - {str(convert_queue_size)} (Click To Change)', 'change_convert_queue_size')])
            for board in gen_keyboard(bool_list, convert_use_queue_size, "convertusequeuesize", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🌳Use SYNC - {str(convert_sync)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, convert_sync, "convertsync", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🎴Convert Qualities - {str(convert_list)}', 'nik66bots')])
            for board in gen_keyboard([[720, 480, 360],[1080], [720], [540], [480], [360]], convert_list, "convertlist", 3, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'♒Preset - {str(convert_preset)}', 'nik66bots')])
            for board in gen_keyboard(presets_list, convert_preset, "convertpreset", 3, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'⚡CRF  - {str(convert_crf)}', 'nik66bots')])
            for board in gen_keyboard(crf_list, convert_crf, "convertcrf", 4, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline('🎵 Audio', 'convert_audio_settings')])
            KeyBoard.append([Button.inline('📝 Metadata', 'convert_metadata_settings')])
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            if edit:
                try:
                    await event.edit("⚙ Convert Settings", buttons=KeyBoard)
                except:
                    pass
            else:
                try:
                    await event.delete()
                except:
                    pass
                await Telegram.TELETHON_CLIENT.send_message(event.chat.id, "⚙ Convert Settings", buttons=KeyBoard)
            return

###############------Hardmux------###############
async def hardmux_callback(event, txt, user_id, edit):
            new_position = txt.split("_", 1)[1]
            KeyBoard = []
            if txt.startswith("hardmuxencoder"):
                await saveconfig(user_id, 'hardmux', 'encoder', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Hardmux Encoder - {str(new_position)}")
            elif txt.startswith("hardmuxencodevideo"):
                await saveconfig(user_id, 'hardmux', 'encode_video', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Hardmux Use Encoder - {str(new_position)}")
            elif txt.startswith("hardmuxpreset"):
                await saveconfig(user_id, 'hardmux', 'preset', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Hardmux Preset - {str(new_position)}")
            elif txt.startswith("hardmuxcrf"):
                if new_position == "Kustom":
                    crf_input = await get_text_data(event.chat.id, user_id, event, 120, "Masukkan nilai CRF kustom (0-51)")
                    if crf_input:
                        try:
                            crf_value = int(crf_input.message.message)
                            if 0 <= crf_value <= 51:
                                await saveconfig(user_id, 'hardmux', 'crf', str(crf_value), SAVE_TO_DATABASE)
                                await event.answer(f"✅Hardmux CRF Kustom - {crf_value}")
                            else:
                                await crf_input.reply("❗Nilai CRF harus antara 0 dan 51.")
                        except ValueError:
                            await crf_input.reply("❗Input tidak valid, masukkan angka.")
                else:
                    await saveconfig(user_id, 'hardmux', 'crf', new_position, SAVE_TO_DATABASE)
                    await event.answer(f"✅Hardmux CRF - {str(new_position)}")
            elif txt.startswith("hardmuxusequeuesize"):
                await saveconfig(user_id, 'hardmux', 'use_queue_size', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Hardmux Use Queue Size - {str(new_position)}")
            elif txt.startswith("hardmuxsync"):
                await saveconfig(user_id, 'hardmux', 'sync', eval(new_position), SAVE_TO_DATABASE)
                await event.answer(f"✅Hardmux Use SYNC - {str(new_position)}")
            hardmux_encode_video = get_data()[user_id]['hardmux']['encode_video']
            hardmux_encoder = get_data()[user_id]['hardmux']['encoder']
            hardmux_preset = get_data()[user_id]['hardmux']['preset']
            hardmux_crf = get_data()[user_id]['hardmux']['crf']
            hardmux_use_queue_size = get_data()[user_id]['hardmux']['use_queue_size']
            hardmux_queue_size = get_data()[user_id]['hardmux']['queue_size']
            hardmux_sync = get_data()[user_id]['hardmux']['sync']
            KeyBoard.append([Button.inline(f'🎧Use Encoder - {str(hardmux_encode_video)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, hardmux_encode_video, "hardmuxencodevideo", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🍬Encoder - {str(hardmux_encoder)}', 'nik66bots')])
            for board in gen_keyboard(encoders_list, hardmux_encoder, "hardmuxencoder", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'📻Use FFMPEG Queue Size  - {str(hardmux_use_queue_size)}', 'nik66bots')])
            if hardmux_use_queue_size:
                KeyBoard.append([Button.inline(f'🎹FFMPEG Queue Size Value  - {str(hardmux_queue_size)} (Click To Change)', 'change_hardmux_queue_size')])
            for board in gen_keyboard(bool_list, hardmux_use_queue_size, "hardmuxusequeuesize", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'🌳Use SYNC - {str(hardmux_sync)}', 'nik66bots')])
            for board in gen_keyboard(bool_list, hardmux_sync, "hardmuxsync", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'♒Preset - {str(hardmux_preset)}', 'nik66bots')])
            for board in gen_keyboard(presets_list, hardmux_preset, "hardmuxpreset", 3, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'⚡CRF  - {str(hardmux_crf)}', 'nik66bots')])
            for board in gen_keyboard(crf_list, hardmux_crf, "hardmuxcrf", 4, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline('🎵 Audio', 'hardmux_audio_settings')])
            KeyBoard.append([Button.inline('📝 Metadata', 'hardmux_metadata_settings')])
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            if edit:
                try:
                    await event.edit("⚙ Hardmux Settings", buttons=KeyBoard)
                except:
                    pass
            else:
                try:
                    await event.delete()
                except:
                    pass
                await Telegram.TELETHON_CLIENT.send_message(event.chat.id, "⚙ Hardmux Settings", buttons=KeyBoard)
            return


###############------Softmux------###############
async def softmux_callback(event, txt, user_id, edit):
            new_position = txt.split("_", 1)[1]
            KeyBoard = []
            if txt.startswith("softmuxsubcodec"):
                await saveconfig(user_id, 'softmux', 'sub_codec', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Softmux Sub Codec - {str(new_position)}")
            softmux_sub_codec = get_data()[user_id]['softmux']['sub_codec']
            KeyBoard.append([Button.inline(f'🍄Subtitles Codec - {str(softmux_sub_codec)}', 'nik66bots')])
            for board in gen_keyboard(['copy', 'mov_text'], softmux_sub_codec, "softmuxsubcodec", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            if edit:
                try:
                    await event.edit("⚙ Softmux Settings", buttons=KeyBoard)
                except:
                    pass
            else:
                try:
                    await event.delete()
                except:
                    pass
                await Telegram.TELETHON_CLIENT.send_message(event.chat.id, "⚙ Softmux Settings", buttons=KeyBoard)
            return


###############------Softremux------###############
async def softremux_callback(event, txt, user_id, edit):
            new_position = txt.split("_", 1)[1]
            KeyBoard = []
            if txt.startswith("softremuxsubcodec"):
                await saveconfig(user_id, 'softremux', 'sub_codec', new_position, SAVE_TO_DATABASE)
                await event.answer(f"✅Softremux Sub Codec - {str(new_position)}")
            softremux_sub_codec = get_data()[user_id]['softremux']['sub_codec']
            KeyBoard.append([Button.inline(f'🍄Subtitles Codec - {str(softremux_sub_codec)}', 'nik66bots')])
            for board in gen_keyboard(['copy', 'mov_text'], softremux_sub_codec, "softremuxsubcodec", 2, False):
                KeyBoard.append(board)
            KeyBoard.append([Button.inline(f'↩Back', 'settings')])
            if edit:
                try:
                    await event.edit("⚙ Softremux Settings", buttons=KeyBoard)
                except:
                    pass
            else:
                try:
                    await event.delete()
                except:
                    pass
                await Telegram.TELETHON_CLIENT.send_message(event.chat.id, "⚙ Softremux Settings", buttons=KeyBoard)
            return

###############------Audio Settings------###############
async def audio_settings_callback(event, txt, user_id, process_type):
    new_position = txt.split("_", 2)[2]
    await saveconfig(user_id, process_type, 'audio_codec', new_position, SAVE_TO_DATABASE)
    await event.answer(f"✅{process_type.capitalize()} Audio Codec - {str(new_position)}")
    
    audio_codec = get_data()[user_id][process_type]['audio_codec']
    KeyBoard = []
    KeyBoard.append([Button.inline(f'🎵 Audio Codec - {str(audio_codec)}', 'nik66bots')])
    for board in gen_keyboard(audio_codec_list, audio_codec, f"{process_type}_audio_codec", 2, False):
        KeyBoard.append(board)
    KeyBoard.append([Button.inline(f'↩Back', f'{process_type}_settings')])
    try:
        await event.edit(f"⚙ {process_type.capitalize()} Audio Settings", buttons=KeyBoard)
    except:
        pass

###############------Metadata Settings------###############
async def metadata_settings_callback(event, txt, user_id, process_type):
    if txt.endswith("_edit"):
        metadata_input = await get_metadata(event.chat.id, user_id, event, 120, "Send Metadata Title")
        if metadata_input:
            await saveconfig(user_id, process_type, 'metadata', metadata_input, SAVE_TO_DATABASE)
            await event.answer(f"✅{process_type.capitalize()} Metadata - {str(metadata_input)}")
    
    metadata = get_data()[user_id][process_type]['metadata']
    KeyBoard = []
    KeyBoard.append([Button.inline(f'📝 Metadata - {str(metadata)}', 'nik66bots')])
    KeyBoard.append([Button.inline('✏️ Edit Metadata', f'{process_type}_metadata_edit')])
    KeyBoard.append([Button.inline(f'↩Back', f'{process_type}_settings')])
    try:
        await event.edit(f"⚙ {process_type.capitalize()} Metadata Settings", buttons=KeyBoard)
    except:
        pass
