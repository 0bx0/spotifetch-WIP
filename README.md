# 🎧 Spotifetch-WIP
A terminal-based Spotify profile viewer with neofetch-style ASCII art and colorful output. Built using Python and Spotipy.

# 📦 About

Spotifetch mimics the iconic style of neofetch, but for Spotify users. It shows your user stats, currently playing track, top and recent artists — all styled with colors and a cool ASCII logo.

> ⚠️ This is a Work in Progress — I'm still adding stuff and polishing it


# 📥 Download & Run

I'm still working on it, so I only released the source code:

```
git clone https://github.com/0bx0/spotifetch-WIP/
cd spotifetch-WIP
python3 ./spotifetch.py
```


> If you want it to kinda feel like a command use this:
```
alias spotifetch='python3 /full/path/to/spotifetch.py'
```

# 🚀 Usage
▶️ View Your Spotify Profile
```
python3 ./spotifetch.py
```

Displays:

    Username, ID, followers

    Total playlists & liked songs

    Currently playing track

    Top & recently played artists

# 🔍 Search for a Song

python3 ./spotifetch.py Taylor Swift Paper Rings

Returns:

    Song name, artist(s)

    Album, release date, duration

    Whether you've liked the song

# 📌 Requirements

    Python 3.7+

    Spotify Developer credentials

    Spotipy library:
```
pip install spotipy
```

# 🛠 TODO

    Turn into a proper CLI tool

    Better error handling & formatting

# 🧠 Tip



📄 License

MIT License
Made with 💚 by @0bx0

Let me know if you'd like a version with emoji removed, more dev-focused, or more aesthetic/minimal!
