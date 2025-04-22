import spotipy
import sys

# Define colors and formatting
GRAY = "\033[90m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RED = "\033[31m"
WHITE = "\033[37m"
BOLD = "\033[1m"
RESET = "\033[0m"
logo = """⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀
⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄
⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇
⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃
⠀⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀
⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⡿⠁⠀
⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀ """

# Do Not Touch
# Initialize spotipy API and create an object called sp with provided credentials
client_id = '58fe916446be4e289c9978b2c934567f'
client_secret = '1817c61934804f65ac893c35ff3f1760'
redirect_uri = 'http://127.0.0.1:8888/callback'


# Updated scope to include all necessary permissions
scope = 'user-library-read user-top-read user-read-recently-played user-read-currently-playing'

auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=client_id, 
                                          client_secret=client_secret, 
                                          redirect_uri=redirect_uri, 
                                          scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Args handler
args = sys.argv[1:]  # Get command line arguments excluding script name

def display_neofetch_style(left_content, right_content_lines):
    # Split logo into lines
    left_lines = left_content.split('\n')
    
    # Determine the width of the logo for padding
    left_width = max(len(line) for line in left_lines)
    
    # Print logo and content side by side (neofetch style)
    for i in range(max(len(left_lines), len(right_content_lines))):
        if i < len(left_lines):
            left_line = f"{GREEN}{left_lines[i]}{RESET}"
        else:
            left_line = " " * left_width
        
        if i < len(right_content_lines):
            right_line = right_content_lines[i]
        else:
            right_line = ""
        
        # Add padding between logo and user info
        print(f"{left_line}    {right_line}")

def fetch_user_details():
    try:
        # Get basic user info
        user_info = sp.current_user()
        username = user_info['display_name']
        user_id = user_info['id']
        user_followers = user_info['followers']['total']
        
        # Get user playlists
        user_playlists = sp.user_playlists(user_id)
        playlist_count = user_playlists['total']
        playlists = [playlist['name'] for playlist in user_playlists['items']]
        
        # Get currently playing track
        current_song = sp.current_user_playing_track()
        current_track_name = "None"
        if current_song and current_song.get('item'):
            current_track_name = current_song['item']['name']
        
        # Get number of liked songs using current_user_saved_tracks()[2][5]
        liked_songs = sp.current_user_saved_tracks(limit=1)
        liked_songs_count = liked_songs['total']
        
        # Get recently played tracks and extract artist names[1]
        recently_played = sp.current_user_recently_played(limit=5)
        recent_artists = []
        for item in recently_played['items']:
            artist_names = [artist['name'] for artist in item['track']['artists']]
            for artist in artist_names:
                if artist not in recent_artists:
                    recent_artists.append(artist)
                if len(recent_artists) >= 5:  # Limit to 5 artists
                    break
            if len(recent_artists) >= 5:
                break
        
        # Get top artists based on user's listening[3]
        top_artists = sp.current_user_top_artists(time_range='medium_term', limit=5)
        top_artist_names = [artist['name'] for artist in top_artists['items']]
        
        # Prepare user info lines (neofetch style) with color formatting
        info_lines = []
        info_lines.append(f"{BOLD}{BLUE}{username}@Spotify{RESET}")
        info_lines.append(f"{BLUE}--------------------{RESET}")
        info_lines.append(f"{BOLD}{BLUE}User:{RESET} {WHITE}{username} (ID: {user_id}){RESET}")
        info_lines.append(f"{BOLD}{BLUE}Followers:{RESET} {WHITE}{user_followers}{RESET}")
        info_lines.append(f"{BOLD}{BLUE}Playlists:{RESET} {WHITE}{playlist_count}{RESET}")
        info_lines.append(f"{BOLD}{BLUE}Liked Songs:{RESET} {WHITE}{liked_songs_count}{RESET}")
        info_lines.append(f"{BOLD}{BLUE}Listening To:{RESET} {WHITE}{current_track_name}{RESET}")
        
        # Display recent artists
        recent_artists_str = ", ".join(recent_artists[:5])
        info_lines.append(f"{BOLD}{BLUE}Recently Played Artists:{RESET} {WHITE}{recent_artists_str}{RESET}")
        
        # Display top artists
        top_artists_str = ", ".join(top_artist_names)
        info_lines.append(f"{BOLD}{BLUE}Top Artists:{RESET} {WHITE}{top_artists_str}{RESET}")
        
        # Display the info next to the logo
        display_neofetch_style(logo, info_lines)
        
        # Handle playlist display separately after the neofetch style display
        if playlist_count >= 4:
            print(f"\n{WHITE}Print all {len(playlists)} playlists?{RESET}")
            user_input = input(f"{BOLD}{BLUE}y/N:{RESET} ")
            if user_input.lower() == 'y':
                print(f"\n{BOLD}{BLUE}Playlists:{RESET}")
                for playlist in playlists:
                    print(f"{WHITE}- {playlist}{RESET}")
            else:
                print(f"{WHITE}Exiting...{RESET}")
                return
        else:
            # If fewer than 4 playlists, just show them all
            print(f"\n{BOLD}{BLUE}Playlists:{RESET}")
            for playlist in playlists:
                print(f"{WHITE}- {playlist}{RESET}")
    
    except spotipy.SpotifyException as e:
        print(f"{BOLD}{RED}Error:{RESET} {WHITE}Failed to fetch Spotify data: {str(e)}{RESET}")
    except Exception as e:
        print(f"{BOLD}{RED}Error:{RESET} {WHITE}An unexpected error occurred: {str(e)}{RESET}")
def fetch_song_details(song_str):
    try:
        # Search for and display information about a song
        results = sp.search(q=song_str, type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            track_artist = ', '.join([artist['name'] for artist in track['artists']])
            duration_ms = track['duration_ms']
            duration_min = duration_ms // 60000
            duration_sec = (duration_ms % 60000) // 1000
            duration = f"{duration_min}:{duration_sec:02d}"
            is_liked = sp.current_user_saved_tracks_contains([track['id']])
            track_album = track['album']['name']
            
            # Prepare song info lines with color formatting
            info_lines = []
            info_lines.append(f"{BOLD}{BLUE}Song Search:{RESET} {song_str} {RESET}- {track['id'] if track['id'] else ''}")
            info_lines.append(f"{BLUE}--------------------{RESET}")
            
            info_lines.append(f"{BOLD}{BLUE}Track:{RESET} {WHITE}{track_name}{RESET}")
            info_lines.append(f"{BOLD}{BLUE}Artist(s):{RESET} {WHITE}{track_artist}{RESET}")
            info_lines.append(f"{BOLD}{BLUE}Album:{RESET} {WHITE}{track_album}{RESET}")
            info_lines.append(f"{BOLD}{BLUE}Liked:{RESET} {WHITE}{'Yes' if is_liked[0] else 'No'}{RESET}")  
            info_lines.append(f"{BOLD}{BLUE}Duration:{RESET} {WHITE}{duration}{RESET}")
            info_lines.append(f"{BOLD}{BLUE}Release Date:{RESET} {WHITE}{track['album']['release_date']}{RESET}")   
            
            # Display the info next to the logo 
            display_neofetch_style(logo, info_lines)
            
        else:
            # Prepare error message with color formatting
            info_lines = []
            info_lines.append(f"{BOLD}{BLUE}Song Search: {song_str}{RESET}")
            info_lines.append(f"{BLUE}--------------------{RESET}")
            info_lines.append(f"{WHITE}No results found for the given song.{RESET}")
            
            # Display the info next to the logo
            display_neofetch_style(logo, info_lines)
    
    except spotipy.SpotifyException as e:
        print(f"{BOLD}{BLUE}Error:{RESET} {WHITE}Failed to search for song: {str(e)}{RESET}")
    except Exception as e:
        print(f"{BOLD}{BLUE}Error:{RESET} {WHITE}An unexpected error occurred: {str(e)}{RESET}")

# Logic to handle command line arguments
if not args:
    # If no arguments provided, fetch user details
    fetch_user_details()
else:
    # If arguments provided, join them with spaces and pass to fetch_song_details
    fetch_song_details(' '.join(args))
