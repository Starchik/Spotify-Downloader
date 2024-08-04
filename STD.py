import os
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed

SAVE_FOLDER = 'spotify_tracks'
os.makedirs(SAVE_FOLDER, exist_ok=True)

def get_spotify_client(client_id, client_secret, redirect_uri, scope):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                     client_secret=client_secret,
                                                     redirect_uri=redirect_uri,
                                                     scope=scope))

def get_all_saved_tracks(sp, limit=50):
    offset = 0
    all_tracks = []
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        tracks = results['items']
        if not tracks:
            break
        all_tracks.extend(tracks)
        offset += limit
    return all_tracks

def save_track_metadata(tracks, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in tracks:
            track = item['track']
            track_name = track['name']
            track_artists = ", ".join([artist['name'] for artist in track['artists']])
            f.write(f"{track_name} - {track_artists}\n")

def search_youtube(query):
    yt_dlp_path = os.path.join(os.path.dirname(__file__), 'yt-dlp.exe')
    command = [yt_dlp_path, 'ytsearch1:{}'.format(query), '--get-id']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        video_id = result.stdout.strip()
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

def download_video(url, output_path):
    yt_dlp_path = os.path.join(os.path.dirname(__file__), 'yt-dlp.exe')
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
    command = [yt_dlp_path, '-x', '--audio-format', 'mp3', '--ffmpeg-location', ffmpeg_path, '-o', output_path, url]
    subprocess.run(command)

def update_log(message):
    log_text.insert(tk.END, message + "\n")
    log_text.yview(tk.END)

def process_track(track_info):
    youtube_url = search_youtube(track_info)
    if youtube_url:
        update_log(f"Found URL: {youtube_url}")
        safe_track_name = track_info.replace('/', '_').replace('\\', '_')
        output_filename = os.path.join(SAVE_FOLDER, f"{safe_track_name}.mp3")
        try:
            download_video(youtube_url, output_filename)
            update_log(f"Downloaded: {output_filename}")
        except Exception as e:
            update_log(f"Error downloading {track_info}: {e}")
    else:
        update_log(f"Could not find: {track_info}")

def process_tracks(client_id, client_secret, redirect_response):
    try:
        redirect_uri = 'https://sites.google.com/view/spredirect/'
        scope = 'user-library-read'
        sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

        # Get the code from the redirect
        code = sp_oauth.parse_response_code(redirect_response)

        # Get and check the access token
        token_info = sp_oauth.get_access_token(code)
        if token_info:
            sp = spotipy.Spotify(auth=token_info['access_token'])

            update_log("Fetching all saved tracks...")
            all_tracks = get_all_saved_tracks(sp)
            update_log(f"Found {len(all_tracks)} tracks.")

            # Save track metadata
            metadata_file = os.path.join(SAVE_FOLDER, 'track_metadata.txt')
            save_track_metadata(all_tracks, metadata_file)
            update_log(f"Track metadata saved to {metadata_file}")

            # Read tracks from file and download
            with open(metadata_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            total_tracks = len(lines)
            update_log("Starting multi-threaded track download...")
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(process_track, line.strip()): line for line in lines}
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        update_log(f"An error occurred: {e}")

            update_log("All tracks processed.")
        else:
            messagebox.showerror('Error', 'Failed to get access token.')
    except spotipy.exceptions.SpotifyException as e:
        messagebox.showerror('Error', f'Spotify API Error: {e}')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def start_download():
    client_id = client_id_entry.get().strip()
    client_secret = client_secret_entry.get().strip()
    redirect_response = redirect_response_entry.get().strip()
    if not client_id or not client_secret or not redirect_response:
        messagebox.showwarning('Error', 'Please enter Client ID, Client Secret, and Redirect Response.')
        return
    thread = threading.Thread(target=process_tracks, args=(client_id, client_secret, redirect_response))
    thread.start()

def open_auth_url():
    client_id = client_id_entry.get().strip()
    client_secret = client_secret_entry.get().strip()
    redirect_uri = 'https://sites.google.com/view/spredirect/'
    scope = 'user-library-read'
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    webbrowser.open(auth_url)

def paste_to_entry(entry):
    try:
        entry.delete(0, tk.END)  # Clear current text
        entry.insert(0, root.clipboard_get())  # Paste text from clipboard
    except tk.TclError:
        messagebox.showwarning('Error', 'Clipboard is empty or not accessible.')

def open_url(url):
    webbrowser.open(url)

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Update clipboard
    messagebox.showinfo('Success', f'Address {text} copied to clipboard.')

root = tk.Tk()
root.title("Spotify Tracks Downloader by Starchik")

def on_link_click(url):
    copy_to_clipboard(url)
    webbrowser.open(url)

instruction_label = tk.Label(root, text="Instructions:\n"
                                        "1. Create an app in the Spotify Developer Dashboard. (Use this link for redirect https://sites.google.com/view/spredirect/)\n"
                                        "2. Write down your Client ID and Client Secret.\n"
                                        "3. Enter Client ID and Client Secret in the fields below.\n"
                                        "4. Click 'Open Auth URL', visit the link, and authorize.\n"
                                        "5. Enter the obtained Redirect Response and click 'Start Download'.\n\n"
                                        "Spotify Developer Dashboard link:",
                             justify=tk.LEFT, padx=10, pady=10)
instruction_label.pack(pady=10)

def copy_text_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Update clipboard
    messagebox.showinfo('Success', f'Address {text} copied to clipboard.')

instruction_label.bind("<Button-1>", lambda e: copy_text_to_clipboard("https://sites.google.com/view/spredirect/"))

link_label = tk.Label(root, text="https://developer.spotify.com/dashboard",
                      fg="blue", cursor="hand2")
link_label.pack()
link_label.bind("<Button-1>", lambda e: open_url("https://developer.spotify.com/dashboard"))

instruction_label = tk.Label(root, text="Support the project:\n",
                             justify=tk.LEFT)
instruction_label.pack()

donate_label = tk.Label(root, text=" https://destream.net/live/IgorStorcheus/donate",
                        fg="blue", cursor="hand2")
donate_label.pack(pady=5)
donate_label.bind("<Button-1>", lambda e: open_url("https://destream.net/live/IgorStorcheus/donate"))

crypto_frame = tk.Frame(root)
crypto_frame.pack(pady=10)

buttons_info = [
    ("USDT TRC20", "TY2uCasX4mjsyPu8Wkv9zHAFNBBBFQ2KMm"),
    ("BTC", "143KQQ7G7biWEuxcvfZHM6eastyxNQduYP"),
    ("ETH", "0xd6506c16e4484fd013f6d16bb0e8f135e517f08a"),
    ("BNB (BEP20)", "0x752a91f70bdda26f4b5656a69fdfc54411f4d6cf")
]

for label, address in buttons_info:
    button = tk.Button(crypto_frame, text=label, command=lambda addr=address: copy_to_clipboard(addr))
    button.pack(side=tk.LEFT, padx=5)

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

client_id_label = tk.Label(entry_frame, text="Client ID:")
client_id_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
client_id_entry = tk.Entry(entry_frame, width=50)
client_id_entry.grid(row=0, column=1, padx=5, pady=5)
client_id_paste_button = tk.Button(entry_frame, text="Paste", command=lambda: paste_to_entry(client_id_entry))
client_id_paste_button.grid(row=0, column=2, padx=5, pady=5)

client_secret_label = tk.Label(entry_frame, text="Client Secret:")
client_secret_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
client_secret_entry = tk.Entry(entry_frame, width=50)
client_secret_entry.grid(row=1, column=1, padx=5, pady=5)
client_secret_paste_button = tk.Button(entry_frame, text="Paste", command=lambda: paste_to_entry(client_secret_entry))
client_secret_paste_button.grid(row=1, column=2, padx=5, pady=5)

redirect_response_label = tk.Label(entry_frame, text="Redirect Response:")
redirect_response_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
redirect_response_entry = tk.Entry(entry_frame, width=50)
redirect_response_entry.grid(row=2, column=1, padx=5, pady=5)
redirect_response_paste_button = tk.Button(entry_frame, text="Paste", command=lambda: paste_to_entry(redirect_response_entry))
redirect_response_paste_button.grid(row=2, column=2, padx=5, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

open_auth_url_button = tk.Button(button_frame, text="Open Auth URL", command=open_auth_url)
open_auth_url_button.pack(side=tk.LEFT, padx=10)

start_download_button = tk.Button(button_frame, text="Start Download", command=start_download)
start_download_button.pack(side=tk.LEFT, padx=10)

log_text = scrolledtext.ScrolledText(root, width=100, height=20)
log_text.pack(pady=10)

root.mainloop()
