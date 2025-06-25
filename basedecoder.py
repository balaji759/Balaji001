import base64
import re
import zlib
import os
import io
import zipfile
import requests
import shutil
import pyfiglet
import time
from threading import Thread
from uuid import uuid4

# Color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

# Telegram Bot Token
BOT_TOKEN = "7891872689:AAFSFOCbsAKlEeZK_xrA13wmjnUAMjyrGXo"  # Replace with your actual bot token

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    ascii_art = pyfiglet.figlet_format("Divyaman AI", font="small")
    print(f"{CYAN}{ascii_art}{RESET}")
    print(f"{GREEN}🔍 Base Decoding Bot | Unlimited Users{RESET}\n")

def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    if parse_mode:
        data["parse_mode"] = parse_mode
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"{RED}Error sending message: {e}{RESET}")
        return None

def delete_message(chat_id, message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
    data = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    try:
        requests.post(url, json=data)
    except Exception:
        pass

def send_typing_action(chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendChatAction"
    data = {
        "chat_id": chat_id,
        "action": "typing"
    }
    try:
        requests.post(url, json=data)
    except Exception:
        pass

def send_document(chat_id, file_path, caption=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        try:
            response = requests.post(url, files=files, data=data)
            return response.json()
        except Exception as e:
            print(f"{RED}Error sending document: {e}{RESET}")
            return None

def download_file(file_id, file_name):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = response.json()['result']['file_path']
            download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            
            response = requests.get(download_url)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                return file_name
    except Exception as e:
        print(f"{RED}Error downloading file: {e}{RESET}")
    return None

def show_loading_animation(chat_id, loading_message):
    dots = 0
    while not loading_message['stop']:
        dots = (dots + 1) % 4
        edit_message_text(chat_id, loading_message['message_id'], 
                         f"Decoding your file{'.' * dots} Please wait")
        time.sleep(0.5)

def edit_message_text(chat_id, message_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    }
    try:
        requests.post(url, json=data)
    except Exception:
        pass

def extract_encoded_strings(file_content):
    patterns = [
        r"'(.*?)'",
        r"(.*?)",
        r'"(.*?)"',
        r'"""(.*?)"""',
        r"'''(.*?)'''",
        r"b'''(.*?)'''",
        r'b"""(.*?)"""',
        r"b'(.*?)'",
        r'b"(.*?)"',
        r'base64\.b64decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
        r'base64\.b64decode\(\s*b[\'"]([^\'"]+)[\'"]\s*\)',
        r'base64\.b85decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
        r'base64\.b85decode\(\s*b[\'"]([^\'"]+)[\'"]\s*\)',
        r'(exec|eval|compile)\(\s*base64\.b64decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
        r'(exec|eval|compile)\(\s*base64\.b85decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
        r'base64\.b64decode\(\s*base64\.b64decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
        r'base64\.b85decode\(\s*base64\.b85decode\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\)',
        r'base64\.(b16decode|b32decode|b64decode|b85decode|urlsafe_b64decode)\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
        r'base64\.(b16decode|b32decode|b64decode|b85decode|urlsafe_b64decode)\(\s*b[\'"]([^\'"]+)[\'"]\s*\)',
    ]
    
    matches = []
    for pattern in patterns:
        for match in re.findall(pattern, file_content, re.DOTALL):
            if isinstance(match, tuple):
                matches.append(match[-1])
            else:
                matches.append(match)
    return matches

def is_mostly_printable(s, threshold=0.9):
    text = s.strip()
    if not text:
        return False
    printable_count = sum(c.isprintable() for c in text)
    return (printable_count / len(text)) >= threshold

def try_all_decodes(encoded_str, output_prefix="decoded_output"):
    candidates = []
    decoding_methods = [
        ('base64', base64.b64decode),
        ('base85', base64.b85decode),
        ('base32', base64.b32decode),
        ('base16', lambda s: base64.b16decode(s, casefold=True)),
    ]

    for method_name, decoder in decoding_methods:
        for direction in ['normal', 'reversed']:
            try:
                data = encoded_str[::-1] if direction == 'reversed' else encoded_str
                decoded_bytes = decoder(data.encode())

                # Check for ZIP files
                if decoded_bytes[:4] == b'PK\x03\x04':
                    zip_output_dir = f"{output_prefix}_zip_{method_name}_{direction}"
                    os.makedirs(zip_output_dir, exist_ok=True)

                    try:
                        with zipfile.ZipFile(io.BytesIO(decoded_bytes), 'r') as zf:
                            zf.extractall(zip_output_dir)
                        return {
                            'text': f'ZIP archive extracted to {zip_output_dir}',
                            'method': method_name,
                            'direction': direction,
                            'source': 'zip',
                            'zip_output_dir': zip_output_dir
                        }
                    except zipfile.BadZipFile:
                        continue

                # Try zlib decompression
                try:
                    decompressed = zlib.decompress(decoded_bytes)
                    decoded_str = decompressed.decode('utf-8', errors='ignore')
                    source = 'zlib-compressed'
                except Exception:
                    decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
                    source = 'plain'

                if is_mostly_printable(decoded_str):
                    candidates.append({
                        'text': decoded_str,
                        'method': method_name,
                        'direction': direction,
                        'source': source
                    })
            except Exception:
                continue

    if candidates:
        return sorted(candidates, key=lambda c: (c['source'] == 'plain', len(c['text'])), reverse=True)[0]
    return None

def process_file(file_path, chat_id):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            contents = f.read()

        encoded_strings = extract_encoded_strings(contents)
        if not encoded_strings:
            return False, "No encoded strings found in the file."

        # Create unique output directory for each request
        output_dir = f"temp_{str(uuid4())[:8]}"
        os.makedirs(output_dir, exist_ok=True)
        success_count = 0

        for i, encoded in enumerate(encoded_strings):
            result = try_all_decodes(encoded, output_prefix=os.path.join(output_dir, f'chunk{i+1}'))
            if result:
                success_count += 1
                if result['source'] == 'zip':
                    zip_path = shutil.make_archive(result['zip_output_dir'], 'zip', result['zip_output_dir'])
                    send_document(chat_id, zip_path, f"ZIP archive decoded (Method: {result['method'].upper()})")
                    os.remove(zip_path)
                    shutil.rmtree(result['zip_output_dir'])
                else:
                    out_name = os.path.join(output_dir, f'decoded_{i+1}.py')
                    with open(out_name, 'w', encoding='utf-8') as out_f:
                        out_f.write(result['text'])
                    send_document(chat_id, out_name, 
                                f"Decoded content (Method: {result['method'].upper()}, Direction: {result['direction']})")
                    os.remove(out_name)

        # Clean up
        shutil.rmtree(output_dir)
        return True, f"Successfully decoded {success_count} chunks. Check your files above."

    except Exception as e:
        # Clean up if any error occurs
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False, f"Error during processing: {str(e)}"

def handle_updates():
    offset = None
    show_banner()
    print(f"{GREEN}✅ Bot is running and ready to receive files from unlimited users!{RESET}")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?timeout=30"
            if offset:
                url += f"&offset={offset}"
            
            response = requests.get(url)
            if response.status_code == 200:
                updates = response.json().get('result', [])
                if updates:
                    offset = updates[-1]['update_id'] + 1
                    
                    for update in updates:
                        if 'message' in update:
                            message = update['message']
                            chat_id = message['chat']['id']
                            user_name = message['chat'].get('first_name', 'User')
                            
                            if 'text' in message:
                                text = message['text'].lower()
                                
                                if text == '/start':
                                    welcome_msg = (
                                        f"👋 Hello {user_name}! Welcome to Divyaman AI\n\n"
                                        "🔍 I can decode various base-encoded files including:\n"
                                        "- Base16\n- Base32\n- Base64\n- Base85\n\n"
                                        "📤 Just send me your encoded file and I'll decode it for you!"
                                    )
                                    send_message(chat_id, welcome_msg)
                                    
                                elif text == '/help':
                                    help_msg = (
                                        "ℹ️ How to use this bot:\n\n"
                                        "1. Simply upload your base-encoded file\n"
                                        "2. Wait while I decode it\n"
                                        "3. Receive your decoded files!\n\n"
                                        "Supported formats: Base16, Base32, Base64, Base85"
                                    )
                                    send_message(chat_id, help_msg)
                            
                            elif 'document' in message:
                                file_id = message['document']['file_id']
                                file_name = message['document'].get('file_name', f'encoded_{str(uuid4())[:4]}.py')
                                
                                # Send initial response
                                loading_msg = send_message(chat_id, "🔍 Starting to decode your file...")
                                if loading_msg and 'result' in loading_msg:
                                    loading_message_id = loading_msg['result']['message_id']
                                else:
                                    continue
                                
                                # Show typing action
                                send_typing_action(chat_id)
                                
                                # Start loading animation in a separate thread
                                loading = {'stop': False}
                                loading_thread = Thread(target=show_loading_animation, 
                                                      args=(chat_id, loading))
                                loading_thread.start()
                                
                                # Download the file
                                downloaded_file = download_file(file_id, file_name)
                                if downloaded_file:
                                    # Process the file
                                    success, result_msg = process_file(downloaded_file, chat_id)
                                    
                                    # Stop loading animation
                                    loading['stop'] = True
                                    loading_thread.join()
                                    
                                    # Delete loading message
                                    delete_message(chat_id, loading_message_id)
                                    
                                    # Send result
                                    if success:
                                        send_message(chat_id, "✅ " + result_msg)
                                    else:
                                        send_message(chat_id, "❌ " + result_msg)
                                    
                                    # Clean up downloaded file
                                    if os.path.exists(downloaded_file):
                                        os.remove(downloaded_file)
                                else:
                                    loading['stop'] = True
                                    loading_thread.join()
                                    delete_message(chat_id, loading_message_id)
                                    send_message(chat_id, "❌ Failed to download the file. Please try again.")
            
        except KeyboardInterrupt:
            print(f"\n{RED}🚫 Bot stopped by user{RESET}")
            break
        except Exception as e:
            print(f"{RED}Error in update handling: {e}{RESET}")
            time.sleep(5)

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print(f"{RED}Please set your Telegram bot token in the script{RESET}")
    else:
        # Create temp directory if not exists
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        # Change working directory to temp to avoid clutter
        os.chdir('temp')
        
        handle_updates()