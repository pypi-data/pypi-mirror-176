from pathlib import Path

path = Path().absolute()

print(Path(__file__).parent.resolve())

TMDB_URL = "https://api.themoviedb.org"
TMDB_VERSION = "3"

guest_session = "guest_session"
user_session = "user_session"

url_header_encoded = {'content-type': 'application/x-www-form-urlencoded'}

#route = f"{str(Path().absolute())}\\tmdb_wrapper\\utils\\session_id.pkl"

route = "tmdb_wrapper/tmdb_wrapper/utils/session_id.pkl"