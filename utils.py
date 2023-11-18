import os
import googlemaps
import json
from langchain.chat_models import ChatOpenAI
from langchain.tools import StructuredTool
from langchain.agents import initialize_agent, AgentType
from pydantic import BaseModel, Field
from typing import Optional, Union, List 
from dotenv import load_dotenv

load_dotenv()

google_maps_key = os.getenv("google_maps_key")
gmaps = googlemaps.Client(key=google_maps_key)

def retrieve_location(): 
  "Returns latitude and longitude of current location"
  latitude = 37.423304896346345
  longitude = -122.16023584591919
   
  return latitude, longitude

def reverse_geocode(latitude: float, longitude: float): 
  "Converts latitude and longitude into a readable address"
  result = gmaps.reverse_geocode((latitude, longitude))
  if result:
        address = result[0].get('formatted_address', 'No address found')
  else:
    address = 'No address found'
  
  return address

def find_places(query: Optional[str] = None,
                       location: Optional[Union[tuple, list, str]] = None,
                       radius: Optional[int] = None,
                       language: Optional[str] = None,
                       min_price: Optional[int] = None,
                       max_price: Optional[int] = None,
                       open_now: Optional[bool] = False,
                       place_type: Optional[str] = None,
                       region: Optional[str] = None): 
  "Finds places based on location and other optional parameters. For each place, returns place ID, name, coordinates as a tuple, formatted address, and rating."
  
  params = {
        'query': query,
        'location': location,
        'radius': radius,
        'language': language,
        'min_price': min_price,
        'max_price': max_price,
        'open_now': open_now,
        'type': place_type,
        'region': region
    } 
  
  params = {k: v for k, v in params.items() if v is not None}
  response = gmaps.places(**params)
  
  results = response['results'][:5] # limit to top 5 results 
  
  simplified_results = []
  for place in results: 
    place_info = {
      'place_id': place.get('place_id'), 
      'name': place.get('name'), 
      'location': (place['geometry']['location']['lat'], place['geometry']['location']['lng']), 
      'formatted_address': place.get('formatted_address'), 
      'rating': place.get('rating')
    }
    simplified_results.append(place_info)
    
  return simplified_results

class FindPlaces(BaseModel): 
  query: Optional[str] = Field(None, description = "Text string to search for, e.g., 'restaurant'")
  location: Optional[Union[tuple, list, str]] = Field(None, description = "Latitude and longitude as a tuple or string")
  radius: Optional[int] = Field(None, description = "Search radius in meters")
  language: Optional[str] = Field(None, description = "The language in which to return results")
  min_price: Optional[int] = Field(None, description = "Minimum price level of places to include, from 0 (most affordable) to 4 (most expensive)")
  max_price: Optional[int] = Field(None, description = "Maximum price level of places to include, from 0 (most affordable) to 4 (most expensive)")
  open_now: Optional[bool] = Field(False, description = "Return only those places that are open for business at the time the query is sent")
  place_type: Optional[str] = Field(None, description = "Type of place to restrict results to")
  region: Optional[str] = Field(None, description = "Region code to bias results towards")
  
find_places_tool = StructuredTool(
  func = find_places, 
  name = "Find Places", 
  description = "Finds places based on location and other optional parameters. For each place, returns place ID, name, coordinates as a tuple, formatted address, and rating.", 
  args_schema = FindPlaces
)

def main(): 
  tools = []
  tools.append(StructuredTool.from_function(retrieve_location))
  tools.append(StructuredTool.from_function(reverse_geocode))
  tools.append(find_places_tool)
  
  # TODO: 
  # Missing: place
  # Missing: find_place 
  # Missing: directions 
  # Missing: distance_matrix
  
  llm = ChatOpenAI(model="gpt-4")
  agent_chain = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
  agent_chain.invoke(
    {
      "input": "Is there a cafe near me?"
    }
  )
  
  # TODO: 
  # places()
    # Only certain 'type' can be accepted. Prompt agent. 
    # Only certain 'regions' can be accepted. 
  

   
if __name__ == "__main__": 
  main()
  # Important GMaps documentation: https://googlemaps.github.io/google-maps-services-python/docs/index.html#googlemaps.Client.places

  
 
  

