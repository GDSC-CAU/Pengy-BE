# eduContents/utils.py
import feedparser
import requests
from eduContents.models import EduContent 
from fireHazards.models import FireHazard
from scholarly import scholarly #open source library for scholarly content

from config.settings import get_env_variable
from urllib.parse import quote_plus


class GoogleNewsHandler:
    def __init__(self, query):
        self.query = query
        self.year = 3  # Search news from the past n years
        self.num = 3  # Get top n results

    def fetch_news_data(self):
        # Encode the query to ensure it's URL-safe
        encoded_query = quote_plus(f"{self.query} fire when:{self.year}y")
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:self.num]:
            articles.append({
                'title': entry.title,
                'link': entry.link
            })
        return articles

class YouTubeVideoHandler:
    def __init__(self, query):
        self.query = query
        self.api_key = get_env_variable('YOUTUBE_API_KEY')
        self.max_results = 1

    def fetch_video_links(self):
        video_links = []
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={self.max_results}&q={self.query}&type=video&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('items', [])
            for result in results:
                video_id = result['id']['videoId']
                # video_links.append(f"https://www.youtube.com/watch?v={video_id}")
        # return video_links
        return video_id

class ScholarlyContentHandler:
    def __init__(self, query):
        self.query = f"{query} fire causes"  # Add 'causes' to the query
        self.num_articles = 1  # Number of papers to retrieve
        self.language = "en"  # Note: 'scholarly' may not support language filtering directly

    def fetch_articles(self):
        search_result = scholarly.search_pubs(self.query)
        articles_data = []
        try:
            for _ in range(self.num_articles):
                articles_data.append(next(search_result))
        except StopIteration:
            print("Less than the requested number of articles were found.")
        return articles_data
    
    def get_scholarly_content(self):
        fetched_articles = self.fetch_articles()
        scholarly_content = []
        max_abstract_length = 150  # 최대 길이 설정

        for article in fetched_articles:
            try:
                bib = article.get('bib', {})
                title = bib.get('title', 'No title available')
                authors_list = bib.get('author', [])
                authors = ', '.join(authors_list) if isinstance(authors_list, list) else 'No author available'
                pub_year = bib.get('pub_year', 'Publication year not available')
                venue = bib.get('venue', 'Venue not available')
                abstract = bib.get('abstract', 'Abstract not available')
                if len(abstract) > max_abstract_length:
                    abstract = abstract[:max_abstract_length] + '...'  # 초록 길이 제한

                pub_url = article.get('pub_url', 'URL not available')
                
                scholarly_content.append({
                    'title': title,
                    'authors': authors,
                    'pub_year': pub_year,
                    'venue': venue,
                    'abstract': abstract,
                    'pub_url': pub_url
                })
            except AttributeError as e:
                print(f"Error processing article: {e}")

        return scholarly_content
    
# Example usage in a Django view or another function
def update_edu_content(fire_hazard_id):
    try:
        fire_hazard = FireHazard.objects.get(id=fire_hazard_id)
        news_handler = GoogleNewsHandler(fire_hazard.object)
        google_news_data = news_handler.fetch_news_data()
        
        video_handler = YouTubeVideoHandler(fire_hazard.object + 'fire prevention tips')
        youtube_video_links = video_handler.fetch_video_links()

        scholarly_handler = ScholarlyContentHandler(fire_hazard.object)
        scholarly_data = scholarly_handler.get_scholarly_content()

        # Initialize the FireSafetyInstructionsHandler with the fire_hazard.object
        safety_instructions_handler = FireSafetyInstructionsHandler(fire_hazard.object)
        safety_instructions = safety_instructions_handler.get_instructions()

        # Update or create EduContent for the fire_hazard
        edu_content, created = EduContent.objects.update_or_create(
            fire_hazard=fire_hazard,
            defaults={
                'google_news_data': google_news_data,
                'youtube_video_links': youtube_video_links,
                'scholarly_data': scholarly_data,  # Adding scholarly data to EduContent
            }
        )
    except FireHazard.DoesNotExist:
        print(f"FireHazard with id {fire_hazard_id} does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_edu_content_with_str(fire_hazard_str):
    try:
        # Check if the FireHazard already has educational content in the database
        fire_hazard = FireHazard.objects.filter(object=fire_hazard_str).first()
        if fire_hazard:
            # Check if there is already educational content linked to this FireHazard
            if EduContent.objects.filter(fire_hazard=fire_hazard).exists():
                print(f"Educational content already exists for {fire_hazard_str}. Skipping data fetching.")
                return None

        # If FireHazard does not exist, create a new instance
        else:
            fire_hazard = FireHazard.objects.create(object=fire_hazard_str)

        # Proceed to fetch data as the educational content does not exist
        news_handler = GoogleNewsHandler(fire_hazard.object)
        google_news_data = news_handler.fetch_news_data()
        
        video_handler = YouTubeVideoHandler(fire_hazard.object + ' fire prevention tips')
        youtube_video_links = video_handler.fetch_video_links()
        
        scholarly_handler = ScholarlyContentHandler(fire_hazard.object)
        scholarly_data = scholarly_handler.get_scholarly_content()
        
        
        # Save the new educational content to the database
        edu_content = EduContent(
            fire_hazard=fire_hazard,
            google_news_data=google_news_data,
            youtube_video_links=youtube_video_links,
            scholarly_data=scholarly_data,
        )
        edu_content.save()
        
        print(f"New educational content created for {fire_hazard_str}")
        return edu_content
    
    except Exception as e:
        print(f"An error occurred while retrieving educational content: {e}")
        return None
