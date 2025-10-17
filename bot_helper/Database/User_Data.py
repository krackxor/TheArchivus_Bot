from bot_helper.Database.DB_Handler import Database
from config.config import Config
from datetime import datetime, timedelta
import time
from pytz import timezone

#////////////////////////////////////Variables////////////////////////////////////#
if Config.SAVE_TO_DATABASE:
    db = Database()
    save_id = Config.SAVE_ID
DATA = Config.DATA
LOGGER = Config.LOGGER
TASK_LIMIT = Config.RUNNING_TASK_LIMIT
TIMEZONE = timezone(Config.TIMEZONE)


#////////////////////////////////////Task_Limit////////////////////////////////////#

def get_task_limit():
    return TASK_LIMIT

def change_task_limit(new_limit):
    global TASK_LIMIT
    TASK_LIMIT = new_limit
    return

#////////////////////////////////////Database////////////////////////////////////#

def get_data():
    return DATA

async def new_user(user_id, dbsave):
        DATA[user_id] = {}
        # Pengaturan default lainnya...
        DATA[user_id]['watermark'] = {}
        DATA[user_id]['watermark']['position'] = '5:5'
        DATA[user_id]['watermark']['size'] = '15'
        DATA[user_id]['watermark']['crf'] = '23'
        DATA[user_id]['watermark']['use_queue_size'] = False
        DATA[user_id]['watermark']['queue_size'] = '9999'
        DATA[user_id]['watermark']['use_crf'] = False
        DATA[user_id]['watermark']['encode'] = True
        DATA[user_id]['watermark']['encoder'] = 'libx265'
        DATA[user_id]['watermark']['preset'] = 'ultrafast'
        DATA[user_id]['watermark']['map_audio'] = True
        DATA[user_id]['watermark']['copy_sub'] = True
        DATA[user_id]['watermark']['map'] = True
        DATA[user_id]['watermark']['sync'] = False
        DATA[user_id]['watermark']['audio_codec'] = 'copy'
        DATA[user_id]['watermark']['metadata'] = ''
        DATA[user_id]['softmux'] = {}
        DATA[user_id]['softmux']['preset'] = 'ultrafast'
        DATA[user_id]['softmux']['use_crf'] = False
        DATA[user_id]['softmux']['crf'] = '23'
        DATA[user_id]['softmux']['sub_codec'] = 'copy'
        DATA[user_id]['softmux']['map_audio'] = False
        DATA[user_id]['softmux']['map_sub'] = False
        DATA[user_id]['softmux']['map'] = False
        DATA[user_id]['softmux']['encode'] = False
        DATA[user_id]['softmux']['encoder'] = 'libx265'
        DATA[user_id]['softremux'] = {}
        DATA[user_id]['softremux']['preset'] = 'ultrafast'
        DATA[user_id]['softremux']['use_crf'] = False
        DATA[user_id]['softremux']['crf'] = '23'
        DATA[user_id]['softremux']['sub_codec'] = 'copy'
        DATA[user_id]['softremux']['map_audio'] = False
        DATA[user_id]['softremux']['map_sub'] = False
        DATA[user_id]['softremux']['map'] = False
        DATA[user_id]['softremux']['encode'] = False
        DATA[user_id]['softremux']['encoder'] = 'libx265'
        DATA[user_id]['hardmux'] = {}
        DATA[user_id]['hardmux']['preset'] = 'ultrafast'
        DATA[user_id]['hardmux']['crf'] = '23'
        DATA[user_id]['hardmux']['encode_video'] = True
        DATA[user_id]['hardmux']['encoder'] = 'libx265'
        DATA[user_id]['hardmux']['use_queue_size'] = False
        DATA[user_id]['hardmux']['queue_size'] = '9999'
        DATA[user_id]['hardmux']['sync'] = False
        DATA[user_id]['hardmux']['audio_codec'] = 'copy'
        DATA[user_id]['hardmux']['metadata'] = ''
        DATA[user_id]['compress'] = {}
        DATA[user_id]['compress']['preset'] = 'ultrafast'
        DATA[user_id]['compress']['crf'] = '23'
        DATA[user_id]['compress']['use_queue_size'] = False
        DATA[user_id]['compress']['sync'] = False
        DATA[user_id]['compress']['queue_size'] = '9999'
        DATA[user_id]['compress']['map_audio'] = True
        DATA[user_id]['compress']['map_sub'] = True
        DATA[user_id]['compress']['map'] = True
        DATA[user_id]['compress']['copy_sub'] = False
        DATA[user_id]['compress']['encoder'] = 'libx265'
        DATA[user_id]['compress']['audio_codec'] = 'copy'
        DATA[user_id]['compress']['metadata'] = ''
        DATA[user_id]['extract'] = {}
        DATA[user_id]['extract']['extract_all_audios'] = False
        DATA[user_id]['extract']['extract_all_subtitles'] = False
        DATA[user_id]['extract']['extract_all'] = False
        DATA[user_id]['compression'] = False
        DATA[user_id]['select_stream'] = False
        DATA[user_id]['stream'] = 'ENG'
        DATA[user_id]['split_video'] = False
        DATA[user_id]['split'] = '2GB'
        DATA[user_id]['upload_tg'] = True
        DATA[user_id]['rclone'] = False
        DATA[user_id]['rclone_config_link'] = False
        DATA[user_id]['drive_name'] = False
        DATA[user_id]['merge'] = {}
        DATA[user_id]['merge']['map_audio'] = True
        DATA[user_id]['merge']['map_sub'] = True
        DATA[user_id]['merge']['map'] = True
        DATA[user_id]['merge']['fix_blank'] = False
        DATA[user_id]['merge']['audio_codec'] = 'copy'
        DATA[user_id]['merge']['metadata'] = ''
        DATA[user_id]['custom_thumbnail'] = False
        DATA[user_id]['convert_video'] = False
        DATA[user_id]['convert_quality'] = [720, 480]
        DATA[user_id]['convert'] = {}
        DATA[user_id]['convert']['preset'] = 'ultrafast'
        DATA[user_id]['convert']['use_crf'] = False
        DATA[user_id]['convert']['crf'] = '23'
        DATA[user_id]['convert']['map'] = True
        DATA[user_id]['convert']['encode'] = True
        DATA[user_id]['convert']['encoder'] = 'libx265'
        DATA[user_id]['convert']['copy_sub'] = False
        DATA[user_id]['convert']['use_queue_size'] = False
        DATA[user_id]['convert']['sync'] = False
        DATA[user_id]['convert']['queue_size'] = '9999'
        DATA[user_id]['convert']['convert_list'] = [720, 480]
        DATA[user_id]['convert']['audio_codec'] = 'copy'
        DATA[user_id]['convert']['metadata'] = ''
        DATA[user_id]['custom_name'] = False
        DATA[user_id]['custom_metadata'] = False
        DATA[user_id]['metadata'] = "Nik66Bots"
        DATA[user_id]['detailed_messages'] = True
        DATA[user_id]['show_stats'] = True
        DATA[user_id]['show_botuptime'] = True
        DATA[user_id]['update_time'] = 7
        DATA[user_id]['ffmpeg_log'] = True
        DATA[user_id]['ffmpeg_size'] = True
        DATA[user_id]['ffmpeg_ptime'] = True
        DATA[user_id]['auto_drive'] = False
        DATA[user_id]['show_time'] = True
        DATA[user_id]['gen_ss'] = False
        DATA[user_id]['ss_no'] = 5
        DATA[user_id]['gen_sample'] = False
        DATA[user_id]['tgdownload'] = "Pyrogram"
        DATA[user_id]['tgupload'] = "Pyrogram"
        DATA[user_id]['multi_tasks'] = False
        DATA[user_id]['upload_all'] = True

        DATA[user_id]['skills'] = {
            'Compress': {'level': 0, 'xp': 0}, 'Watermark': {'level': 0, 'xp': 0},
            'Merge': {'level': 0, 'xp': 0}, 'Convert': {'level': 0, 'xp': 0},
            'Hardmux': {'level': 0, 'xp': 0}, 'Softmux': {'level': 0, 'xp': 0},
            'SoftReMux': {'level': 0, 'xp': 0}, 'VideoSample': {'level': 0, 'xp': 0},
            'Extract': {'level': 0, 'xp': 0},
            'GenSS': {'level': 0, 'xp': 0}, 'ChangeMetadata': {'level': 0, 'xp': 0},
            'ChangeIndex': {'level': 0, 'xp': 0}, 'Leech': {'level': 0, 'xp': 0},
            'Mirror': {'level': 0, 'xp': 0}
        }
        if dbsave:
            data = await db.save_data(str(DATA))
        else:
            data = True
        return data

async def saveoptions(user_id, dname, value, dbsave):
    try:
        if user_id not in DATA:
            DATA[user_id] = {}
            DATA[user_id][dname] = {}
            DATA[user_id][dname] = value
        else:
            DATA[user_id][dname] = value
        if dbsave:
            data = await db.save_data(str(DATA))
        else:
            data = True
        return data
    except Exception as e:
        LOGGER.info(e)
        return False
async def resetdatabase(dbsave):
    try:
        DATA.clear()
        if dbsave:
            await db.save_data(str(DATA))
        return True
    except Exception as e:
        LOGGER.info(e)
        return False
async def saveconfig(user_id, dname, pos, value, dbsave):
    try:
        if user_id not in DATA:
            DATA[user_id] = {}
            DATA[user_id][dname] = {}
            DATA[user_id][dname][pos] = value
        else:
            DATA[user_id][dname][pos] = value
        if dbsave:
            data = await db.save_data(str(DATA))
        else:
            data = True
        return data
    except Exception as e:
        LOGGER.info(e)
        return False
async def save_restart(chat_id, msg_id):
    try:
        if 'restart' not in DATA:
            DATA['restart'] = []
            DATA['restart'].append([chat_id, msg_id])
        else:
            DATA['restart'].append([chat_id, msg_id])
        await db.save_data(str(DATA))
        return
    except Exception as e:
        LOGGER.info(e)
        return False
async def clear_restart():
    try:
        DATA['restart'] = []
        await db.save_data(str(DATA))
        return
    except Exception as e:
        LOGGER.info(e)
        return False

#////////////////////////////////////Skill System////////////////////////////////////#

def get_title(skill, level):
    if level == 0:
        return "Pendatang Baru"
    titles = {
        'Convert':  ["Pemula", "Ahli", "Master", "Legenda Konversi"],
        'Hardmux':  ["Novis", "Spesialis", "Pakar", "Maestro Muxing"],
        'Compress': ["Amatir", "Teknisi", "Insinyur", "Arsitek Kompresi"],
        'Watermark':["Pemula", "Desainer", "Artis", "Master Watermark"],
        'Merge':    ["Pemula", "Penyambung", "Editor", "Master Penggabungan"],
        'Leech':    ["Pemula", "Pengunduh", "Kolektor", "Legenda Leech"],
        'Mirror':   ["Pemula", "Pencermin", "Distributor", "Legenda Mirror"],
    }
    if level >= 20: return titles.get(skill, ["-"]*4)[3]
    if level >= 10: return titles.get(skill, ["-"]*4)[2]
    if level >= 5:  return titles.get(skill, ["-"]*4)[1]
    return titles.get(skill, ["-"]*4)[0]

async def add_skill_xp(user_id, skill_name, amount):
    if user_id not in DATA or 'skills' not in DATA.get(user_id, {}):
        await new_user(user_id, Config.SAVE_TO_DATABASE)
    if skill_name not in DATA[user_id]['skills']:
        return None, None, None, None

    # Penggunaan pertama kali langsung naik ke Level 1
    if DATA[user_id]['skills'][skill_name]['level'] == 0:
        DATA[user_id]['skills'][skill_name]['level'] = 1
        new_level_achieved = 1
        xp_needed = 100 # XP dibutuhkan untuk ke level 2
        current_xp = 0
        if Config.SAVE_TO_DATABASE:
            await db.save_data(str(DATA))
        return new_level_achieved, skill_name, amount, (current_xp, xp_needed)

    # Tambahkan XP
    DATA[user_id]['skills'][skill_name]['xp'] += amount
    current_level = DATA[user_id]['skills'][skill_name]['level']
    xp_needed = current_level * 100
    new_level_achieved = None

    if DATA[user_id]['skills'][skill_name]['xp'] >= xp_needed:
        DATA[user_id]['skills'][skill_name]['level'] += 1
        DATA[user_id]['skills'][skill_name]['xp'] -= xp_needed
        new_level_achieved = DATA[user_id]['skills'][skill_name]['level']
    
    current_xp = DATA[user_id]['skills'][skill_name]['xp']
    xp_needed_for_next = DATA[user_id]['skills'][skill_name]['level'] * 100
        
    if Config.SAVE_TO_DATABASE:
        await db.save_data(str(DATA))

    return new_level_achieved, skill_name, amount, (current_xp, xp_needed_for_next)

#////////////////////////////////////VIP System////////////////////////////////////#

async def add_vip(user_id, days):
    if 'vip_users' not in DATA:
        DATA['vip_users'] = {}
    expiration_date = datetime.now(TIMEZONE) + timedelta(days=days)
    DATA['vip_users'][user_id] = expiration_date.timestamp()
    if Config.SAVE_TO_DATABASE:
        await db.save_data(str(DATA))
    return expiration_date.strftime("%Y-%m-%d %H:%M:%S")

async def remove_vip(user_id):
    user_id = int(user_id)
    if 'vip_users' in DATA and user_id in DATA['vip_users']:
        del DATA['vip_users'][user_id]
        if Config.SAVE_TO_DATABASE:
            await db.save_data(str(DATA))
        return True
    return False

async def is_vip(user_id):
    if 'vip_users' not in DATA:
        return False, None
    user_id = int(user_id)
    if user_id not in DATA['vip_users']:
        return False, None
    
    expiration_timestamp = DATA['vip_users'][user_id]
    if time.time() > expiration_timestamp:
        LOGGER.info(f"VIP expired for user {user_id}. Removing automatically.")
        await remove_vip(user_id)
        return False, None
        
    expiration_date = datetime.fromtimestamp(expiration_timestamp, tz=TIMEZONE)
    return True, expiration_date.strftime("%Y-%m-%d %H:%M:%S")

async def get_vip_users():
    if 'vip_users' not in DATA or not DATA['vip_users']:
        return "Tidak ada user VIP."

    all_vips = list(DATA['vip_users'].keys())
    cleaned = False
    for user_id in all_vips:
        expiration_timestamp = DATA['vip_users'].get(user_id)
        if expiration_timestamp and time.time() > expiration_timestamp:
            LOGGER.info(f"Cleaning up expired VIP: {user_id}")
            del DATA['vip_users'][user_id]
            cleaned = True
            
    if cleaned and Config.SAVE_TO_DATABASE:
        await db.save_data(str(DATA))

    if not DATA['vip_users']:
        return "Tidak ada user VIP yang aktif."

    vip_list = "👤 **Daftar User VIP Aktif:**\n\n"
    for user_id, timestamp in DATA['vip_users'].items():
        status = datetime.fromtimestamp(timestamp, tz=TIMEZONE).strftime("%Y-%m-%d %H:%M")
        vip_list += f"- ID: `{user_id}` | Exp: `{status}`\n"
    return vip_list
