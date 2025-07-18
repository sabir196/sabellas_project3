from bs4 import BeautifulSoup
import sqlite3

# Load the saved HTML
with open("/Users/sababa/Downloads/players_selenium.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Connect to SQLite database
conn = sqlite3.connect('/Users/sababa/Downloads/players.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    profile_link TEXT
)
''')

# Parse players from lookup page
players = soup.select("div.col-sm-12.col-md-6.col-lg-4.col-xl-3.col-user.col-player")
print(f"Found {len(players)} players.")

for card in players:
    try:
        name = card.select_one("div.profile a").text.strip()
        profile_link = card.select_one("div.profile a")["href"].strip()
        print(f"✔️ {name} — {profile_link}")

        cursor.execute('''
            INSERT INTO players (name, profile_link)
            VALUES (?, ?)
        ''', (name, profile_link))
    except Exception as e:
        print("❌ Skipped a player due to error:", e)

conn.commit()
conn.close()
print("✅ All players saved to players.db")
