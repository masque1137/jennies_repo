from bs4 import BeautifulSoup
import requests
import pandas as pd

page_url = "https://www.airbnb.com/s/Richmond--Virginia--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-09-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Richmond%2C%20VA&place_id=ChIJ7cmZVwkRsYkRxTxC4m0-2L8&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"


RULES_SEARCH_PAGE = {
    'name': {'tag': 'div', 'class': 'g1qv1ctd c1v0rf5q dir dir-ltr', 'get': 'aria-label'},
}

def build_urls(page_url, listings_per_page=20, pages_per_location=15):
    """Builds links for all search pages for a given location"""
    
    url_list = []
    for i in range(pages_per_location):
        offset = listings_per_page * i
        url_pagination = page_url + f'&items_offset={offset}'
        url_list.append(url_pagination)
       
    return url_list

def extract_element_data(soup, params):
    """Extracts data from a specified HTML element"""
    
    # 1. Find the right tag
    if 'class' in params:
        elements_found = soup.find_all(params['tag'], params['class'])
    else:
        elements_found = soup.find_all(params['tag'])

    elements_text = elements_found[0].text
    output= [elements_text]

    for element in elements_found[0]:
        this_text = element.text
        if "Â" in this_text:
            breakpoint()
        this_text = this_text.replace("\xa0"," ")
        this_text = this_text.replace(" – ",'-')
        output.append(this_text)
    
    # # 2. Extract text from these tags
    # if 'get' in params:
    #     element_texts = [el.get(params['get']) for el in elements_found]
    # else:
    #     element_texts = [el.get_text() for el in elements_found]
        
    # # 3. Select a particular text or concatenate all of them
    # tag_order = params.get('order', 0)
    # if tag_order == -1:
    #     output = '**__**'.join(element_texts)
    # else:
    #     output = element_texts[tag_order]
    
    return output


def scrape_page(page_url):
    """Extracts HTML from a webpage"""
    
    answer = requests.get(page_url)
    content = answer.content
    soup = BeautifulSoup(content, features='html.parser')
    
    return soup

def extract_listing(page_url):
    """Extracts listings from an Airbnb search page"""
    
    page_soup = scrape_page(page_url)
    listings = page_soup.findAll("div", {"class": "c1l1h97y dir dir-ltr"})

    return listings

# listing_soups = extract_listing(page_url)

# features_list = []
# for listing in listing_soups:
#     # features_dict = {}
#     for feature in RULES_SEARCH_PAGE:
#         # features_dict[feature] = extract_element_data(listing, RULES_SEARCH_PAGE[feature])
#         output = extract_element_data(listing, RULES_SEARCH_PAGE[feature])
#         features_list.append(output)




url_list = build_urls(page_url)

features_list = []
for this_url in url_list:
    listing_soups = extract_listing(this_url)
    for listing in listing_soups:
        # features_dict = {}
        for feature in RULES_SEARCH_PAGE:
            # features_dict[feature] = extract_element_data(listing, RULES_SEARCH_PAGE[feature])
            output = extract_element_data(listing, RULES_SEARCH_PAGE[feature])
            features_list.append(output)

features_frame = pd.DataFrame(features_list, columns =["Full","Type","Name","Sub_Name","Dates","Price","Rating"])

features_frame.to_csv("airbnb_features.csv")

these_listings = extract_listing(page_url)


# for this_listing in these_listings:
#     this_text = this_listing.text
#     if "\/" in this_text:
#         this_text = this_text.split('x')[0] 

x = 5
# g1qv1ctd c1v0rf5q dir dir-ltr