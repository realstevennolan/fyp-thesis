import requests
from bs4 import BeautifulSoup

def scrape_squad_sitemap():
    sitemap_url = "https://www.munsterrugby.ie/squad-sitemap.xml"
    
    # Fetch the sitemap
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        print(f"Failed to fetch sitemap: {response.status_code}")
        return

    # Parse the XML sitemap
    soup = BeautifulSoup(response.content, 'xml')
    urls = [loc.text for loc in soup.find_all("loc")]

    print(f"Found {len(urls)} player URLs.")  # Debugging: Show the number of URLs found

    # Scrape data from each URL
    for url in urls:
        scrape_player_page(url)

def scrape_player_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Example of extracting player data
    try:
        player_name = soup.find("h1", class_="player-name").text.strip()
        position = soup.find("div", class_="player-position").text.strip()
        dob = soup.find("div", class_="player-dob").text.strip()
        height = soup.find("div", class_="player-height").text.strip()
        weight = soup.find("div", class_="player-weight").text.strip()

        print(f"Scraped: {player_name}, {position}, {dob}, {height}, {weight}")
        
        # Optionally save the data to your database
        save_player_to_database(player_name, position, dob, height, weight)

    except AttributeError as e:
        print(f"Failed to extract data from {url}: {e}")

# def save_player_to_database(name, position, dob, height, weight):
#     from rugbyanalyticsproject.models import player  # adjust model import as needed
#     player.objects.create(
#         name=name,
#         position=position,
#         dob=dob,
#         height=height,
#         weight=weight
#     )
#     print(f"saved player: {name}")
