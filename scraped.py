from bs4 import BeautifulSoup
import sqlite3



with open("/Users/sababa/Downloads/players_selenium.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
# --- TEMP DEBUG: See if we can extract player names ---
names = soup.select("h2.player-name")
print("Found", len(names), "names")

for n in names:
    print("➡️", n.text.strip())



conn = sqlite3.connect('players.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               age TEXT,
               birthday TEXT,
               primary_position TEXT,
               secondary_position TEXT,
               bats TEXT,
               throws TEXT,
               available TEXT,
               available_dates TEXT,
               distance_travel TEXT,
               current_team TEXT
               )''')


def extract(label, card):
    try:
        return card.find('span', string=label).find_next('span').text.strip()
    except:
        return ''
        
player_cards = soup.select('div.player-details-single')
print("found", len(player_cards), "player_cards")
for card in player_cards:
        sport = extract(card, 'Sport Type:')
        if sport.lower() != 'baseball':
             continue

        name = extract('NAME:', card)
        age = extract('AGE:', card)
        birthday = extract('BIRTHDAY:', card)
        primary_position = extract('PRIMARY POSITION:', card)
        secondary_position = extract('SECONDARY POSITION:', card)
        bats = extract('BATS:', card)
        throws = extract('THROWS:', card)
        available = extract('AVAILABLE:', card)
        available_dates = extract('AVAILABLE DATES:', card)
        distance_travel = extract('DISTANCE TRAVEL:', card)
        current_team = extract('CURRENT TEAM:', card)

        cursor.execute('''
                    INSERT INTO players (name, age, birthday, primary_position, secondary_position, bats, throws, available, available_dates, distance_travel, current_team)

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (name, age, birthday, primary_position, 
                            secondary_position, bats, throws, available,
                            available_dates, distance_travel,
                            current_team))
conn.commit()
conn.close()
print("data scraped")

                         