# eduContents/utils.py
import feedparser
import requests
from eduContents.models import EduContent 
from fireHazards.models import FireHazard
from scholarly import scholarly

#settings.py에서 불러오기
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
        self.api_key = get_env_variable('YOUTUBE_API_KEY') # 보안!!!!
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
        # EduContent.objects.create(youtube_video_links=video_links) # Moved EduContent creation/update outside of this method



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
    
class FireSafetyInstructionsHandler:
    def __init__(self, fire_hazard_object):
        self.fire_hazard_object = fire_hazard_object
    
    def get_instructions(self):

        instructions_dict = {
            "Gas Stove" : """
                Check for Gas Leaks Regularly: Inspect the gas stove and its connections for leaks. If you smell gas (a rotten egg smell) or hear a hissing noise near your stove, do not attempt to light the stove or any matches. Ventilate the area and contact a professional immediately to fix the leak.

                Clean Regularly: Ensure your gas stove, burners, and oven are clean and free of grease build-up. Grease can ignite and cause a fire. Regular cleaning prevents the accumulation of flammable materials.

                Use the Right Size Pots and Pans: Always use pots and pans that fit the burner size. Using too small a pot on a large burner can cause the handle to heat up or even catch fire from the flames.

                Never Leave Cooking Unattended: Unattended cooking is a leading cause of kitchen fires. Always stay in the kitchen when you're cooking on your gas stove. If you must leave, even for a short period, turn off the stove.

                Install a Carbon Monoxide Detector: Gas stoves can produce carbon monoxide. Installing a carbon monoxide detector near your kitchen can help alert you to dangerous levels of this odorless, colorless gas.

                Keep Flammable Items Away: Keep flammable materials such as paper towels, curtains, and plastic utensils away from your gas stove. These items can easily catch fire if left too close to the burner.

                Know How to Extinguish a Fire: In the event of a small grease fire, never use water to extinguish it as it can cause the fire to spread. Instead, turn off the burner, and use a metal lid or baking soda to smother the flames. For larger fires, use a class B fire extinguisher or call the fire department immediately.

                Child and Pet Safety: Keep children and pets away from the stove when it's in use. Teach children kitchen safety and consider installing safety devices to prevent them from turning on the stove.

                Proper Installation and Maintenance: Ensure your gas stove is installed by a qualified professional and follow the manufacturer's instructions for maintenance. Regular inspections by a professional can identify and rectify potential hazards.

                Be Prepared: Have a fire extinguisher readily available in the kitchen and ensure everyone in the household knows how to use it. Familiarize yourself with the emergency shut-off valve for your gas supply.
            """,

            "Outlet" : """
                Avoid Overloading Outlets: Plugging too many devices into an outlet can overload it, leading to overheating and potentially a fire. Use power strips sparingly and ensure they're rated for the devices you're using.

                Inspect Outlets Regularly: Look for signs of damage, such as cracks, loose parts, or burn marks. Damaged outlets should be replaced immediately by a qualified electrician.

                Use Outlet Covers: In homes with small children, use safety covers on unused outlets to prevent them from inserting objects into the sockets.

                Keep Outlets Dry: Ensure that outlets in areas prone to moisture, like kitchens and bathrooms, are equipped with Ground Fault Circuit Interrupters (GFCIs). These devices can prevent electric shock and fires by shutting off the power when they detect a short circuit or a ground fault.

                Don’t Use Damaged Cords: Inspect cords for damage before use. Frayed, cracked, or worn electrical cords can expose wires, increasing the risk of a fire. Replace damaged cords immediately.

                Maintain a Safe Distance: Keep furniture, curtains, and other potentially combustible materials at least a few inches away from outlets to prevent overheating.

                Unplug Appliances When Not in Use: Unplugging devices not only saves energy but also reduces the risk of fire from overheating or power surges.

                Avoid Running Cords Under Carpets: Running cords under rugs or carpets can damage the cords due to foot traffic and hide potential damage. This can lead to overheating and possibly a fire.

                Professional Installation and Repairs: Always have new outlets installed and existing ones repaired by a qualified electrician to ensure they meet safety standards.

                Educate Everyone in the Home: Make sure all household members understand the importance of electrical safety and know how to use outlets properly.
            """,

            "Refrigerator" : """
                Keep Coils Clean: The coils at the back or beneath your refrigerator can accumulate dust and dirt, which can cause the motor to overheat. Clean these coils regularly (at least twice a year) to ensure efficient operation and reduce the risk of overheating.

                Ensure Adequate Ventilation: Refrigerators need space for air to circulate around the coils. Make sure there's enough space between your refrigerator and the wall to prevent overheating. Check the manufacturer's recommendations for the required clearance.

                Check Electrical Connections: Ensure the plug and cord are in good condition. If the cord is frayed or damaged, it should be replaced immediately to avoid electrical fires.

                Use a Dedicated Power Outlet: Refrigerators should be plugged into their own power outlet and not share a multi-outlet adapter or extension cord with other appliances. This reduces the risk of overloading the circuit.

                Do Not Overload: Avoid placing too many items on top of or around the refrigerator. This can block air vents and lead to overheating.

                Regular Maintenance and Inspections: Have your refrigerator inspected and serviced regularly by a professional. This can help identify potential issues before they become serious problems.

                Be Mindful of Placement: Keep your refrigerator away from heat sources like ovens, dishwashers, and direct sunlight. Excessive heat can make the compressor work harder, increasing the risk of overheating.

                Turn Off If You Smell Burning: If you notice a burning smell coming from your refrigerator, unplug it immediately and contact a professional for inspection and repair. Do not attempt to fix electrical problems yourself.

                Monitor Temperature Settings: Setting your refrigerator or freezer to extremely low temperatures can cause the unit to work too hard, potentially leading to overheating. Use the manufacturer's recommended settings for optimal performance and safety.

                Dispose of Old Refrigerators Properly: Older refrigerators may not meet current safety standards and can pose a fire risk. If replacing an old unit, ensure it is properly disposed of or recycled according to local regulations.
            """,

            "Air Conditioner" : """
                Regular Maintenance: Have your air conditioning system serviced by a professional at least once a year. This includes cleaning filters, checking refrigerant levels, and ensuring electrical components are in good condition.

                Clean or Replace Filters Regularly: Dirty filters can restrict airflow and cause the unit to overheat. Check filters monthly during peak usage and clean or replace them as recommended by the manufacturer.

                Inspect Electrical Cords and Connections: Before the cooling season begins, inspect the air conditioner's electrical cords for any signs of wear or damage. If cords are frayed or damaged, have them replaced before using the unit.

                Use a Dedicated Electrical Circuit: Air conditioners should be plugged into a dedicated electrical circuit to prevent overloading. Do not use extension cords or plug other high-power appliances into the same outlet.

                Ensure Proper Installation: If installing a window unit, make sure it is securely mounted and that the electrical components are protected from the elements. Improper installation can lead to electrical hazards.

                Keep the Area Around the Unit Clear: Ensure that there's no buildup of leaves, debris, or other materials around outdoor units. For indoor units, keep furniture and other items away to ensure adequate airflow and reduce the risk of overheating.

                Don't Overwork Your AC: Setting your air conditioner to a very low temperature won't cool your home faster and can overwork the unit. Use programmable thermostats to maintain a comfortable and safe temperature.

                Turn Off When Not Needed: Turn off the air conditioner when you leave the house or use timers or smart home systems to control it efficiently. This reduces the risk of overheating and saves energy.

                Check for Recalls: Keep an eye on manufacturer recalls for air conditioning units. Defective products can pose a fire risk. Register your unit with the manufacturer to receive updates.

                Practice Electrical Safety: Ensure your home's electrical system can handle the load from your air conditioning unit. Older homes may need an electrical system upgrade to safely operate modern AC units.

                Install Smoke Detectors: While not specific to air conditioners, having working smoke detectors in your home can provide an early warning in the event of a fire.
            """,

            "LED lamp" : """
                Use Quality Products: Purchase LED lamps from reputable manufacturers. High-quality LEDs are designed to meet safety standards and are less likely to overheat or cause electrical issues.

                Check Compatibility: Ensure the LED lamp is compatible with your fixtures and dimmers. Using incompatible bulbs can lead to overheating and potentially cause a fire.

                Avoid Overloading: Do not overload lighting circuits or extension cords with too many lamps or other electrical devices, as this can cause overheating and increase the risk of fire.

                Proper Installation: Ensure LED lamps are correctly installed in fixtures that are designed for their specific type and wattage. Incorrect installation can lead to electrical shorts and overheating.

                Ventilation: Even though LED lamps produce less heat than traditional bulbs, they still need proper ventilation to dissipate the heat they do generate. Avoid using them in enclosed fixtures unless they're rated for such use.

                Keep Away from Flammable Materials: Keep LED lamps away from flammable materials such as fabrics, paper, or curtains. Even though LEDs are cooler, their electrical components can malfunction and cause a fire.

                Regular Inspection: Periodically check LED lamps and fixtures for signs of damage, such as cracked bulbs or loose connections. Replace any damaged items immediately.

                Follow Manufacturer Instructions: Always read and follow the manufacturer's instructions regarding the use and installation of LED lamps. This includes adhering to recommended wattages and using the lamps within their intended environments (e.g., not using indoor-rated lamps outdoors).

                Use Surge Protectors: Protect LED lamps from power surges with surge protectors. Power surges can damage the electrical components of LED lamps, potentially leading to fire hazards.

                Turn Off When Not Needed: Reduce the risk of overheating and save energy by turning off LED lamps when they're not in use, especially when leaving home.

                Dispose of Properly: When an LED lamp reaches the end of its life, dispose of it according to local regulations. Some components may be recyclable or require special disposal methods to prevent environmental harm and safety risks.
            """,

            "Wood Boiler" : """
                Installation by Professionals: Ensure your wood boiler is installed by a certified professional who follows the local codes and manufacturer's instructions. Proper installation is crucial for safety and efficiency.

                Use Seasoned Wood: Burn only dry, seasoned wood. Wet or unseasoned wood can lead to incomplete combustion, increasing the risk of chimney fires due to the buildup of creosote, a flammable substance.

                Regular Maintenance and Inspection: Have your wood boiler and chimney inspected and cleaned at least once a year by a qualified professional. This helps prevent chimney fires and ensures the system is operating safely.

                Keep the Area Around the Boiler Clear: Maintain a clear area around the wood boiler. Keep combustible materials, such as paper, wood, and fabric, at a safe distance to prevent accidental fires.

                Install Smoke and Carbon Monoxide Detectors: Install and maintain smoke and carbon monoxide detectors in your home, particularly near the area where the wood boiler is installed. These detectors can provide early warning in case of a fire or dangerous CO levels.

                Follow Manufacturer's Operating Instructions: Always operate your wood boiler according to the manufacturer's instructions. This includes guidelines on loading the wood, adjusting the airflow, and other operational procedures.

                Ensure Proper Ventilation: Make sure your wood boiler has adequate ventilation to support complete combustion and to vent harmful gases, such as carbon monoxide, outside.

                Use a Spark Arrestor: Install a spark arrestor on your chimney if one is not already in place. This device can catch flying sparks and prevent them from starting a fire outside your home.

                Check for Leaks: Regularly inspect the boiler for leaks in the water system, the firebox, and around the seals. Leaks can lead to inefficient operation and potential safety hazards.

                Emergency Plan: Have an emergency plan in place and make sure all household members know what to do in case of a fire. This includes knowing how to shut down the boiler quickly and safely.

                Proper Ash Disposal: Dispose of ashes in a metal container with a tight-fitting lid, and place it on a non-combustible surface away from the building. Ashes can retain heat for several days and potentially ignite combustibles if not handled properly.
            """,
        }

        if self.fire_hazard_object in instructions_dict:
            return instructions_dict[self.fire_hazard_object]
        else:
            return "no tips available for this fire hazard"

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
                'fire_safety_instructions': safety_instructions  # Adding fire safety instructions from the handler
            }
        )
    except FireHazard.DoesNotExist:
        print(f"FireHazard with id {fire_hazard_id} does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")