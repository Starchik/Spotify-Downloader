# Spotify Tracks Downloader by Starchik

This is a Python application that allows you to download your saved Spotify tracks as MP3 files using YouTube as the source. The application uses the Spotipy library to interact with the Spotify API and yt-dlp to download and convert YouTube videos to MP3.

## Features

- Fetch all saved tracks from your Spotify library.
- Search for each track on YouTube.
- Download and convert YouTube videos to MP3 format.
- Multi-threaded downloading for faster performance.
- GUI interface using Tkinter.

## Executable

- [Download Spotify Tracks Downloader](https://mega.nz/file/HvBxUDIQ#yaOziUeV7gvF_WkMvVx8X3IVGuUJfVRUajVPQ4fj5cU) (completely ready to use, includes yt-dlp and ffmpeg)

## Requirements

- Python 3.6+
- Spotify Developer account
- yt-dlp executable
- ffmpeg executable

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Starchik/Spotify-Downloader.git
    cd spotify-downloader
    ```

2. **Install the required Python packages:**
    ```bash
    pip install spotipy tkinter
    ```

3. **Download yt-dlp and ffmpeg executables:**

   - [Download yt-dlp](https://github.com/yt-dlp/yt-dlp#installation)
   - [Download ffmpeg](https://ffmpeg.org/download.html)

   Place the `yt-dlp.exe` and `ffmpeg.exe` files in the same directory as the script.

## Usage

1. **Create a Spotify app:**

   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and create a new app.
   - Set the Redirect URI to `https://sites.google.com/view/spredirect/`.
   - Note down your Client ID and Client Secret.
   

3. **Run the script:**
    ```bash
    python spotify_downloader.py
    ```

4. **Follow the instructions in the GUI:**

    - Enter your Client ID and Client Secret.
    - Click 'Open Auth URL' to open the authorization URL in your browser.
    - Authorize the app and get the Redirect Response URL.
    - Enter the Redirect Response in the GUI.
    - Click 'Start Download' to begin downloading your saved Spotify tracks.

## Donations

If you would like to support the project, you can donate via the following methods:

- **USDT ERC20:** 0xC8c30E6355A592a4ef8AD2179741Af6AF722F5B1
- **BTC:** 18kxRMjRuuZd4ScK5PDktrJCTaa5QjS1AX
- **ETH:** 0xC8c30E6355A592a4ef8AD2179741Af6AF722F5B1

You can also donate via [destream.net](https://destream.net/live/IgorStorcheus/donate).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Spotipy](https://github.com/plamere/spotipy) - Python client for the Spotify Web API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl fork with additional features and fixes
- [ffmpeg](https://ffmpeg.org/) - A complete, cross-platform solution to record, convert and stream audio and video

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
