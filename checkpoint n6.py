import requests
from bs4 import BeautifulSoup
url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
def get_wikipedia_html_content(url):
    # Send a GET request to the Wikipedia page
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_article_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.find('h1', {'class': 'firstHeading'}).text
    return title

def extract_article_text_with_headings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    article_content = {}
    paragraphs = soup.find_all('p')
    current_heading = "Introduction"  # Default heading for the introduction section

    for paragraph in paragraphs:
        if paragraph.find('span', {'class': 'mw-headline'}):
            # If a heading is found, update the current_heading
            current_heading = paragraph.find('span', {'class': 'mw-headline'}).text
        if current_heading not in article_content:
            article_content[current_heading] = []
        article_content[current_heading].append(paragraph.text)

    return article_content

def collect_redirect_links(url):
    redirect_links = []
    html_content = get_wikipedia_html_content(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a', {'class': 'mw-redirect'})
        for link in links:
            redirect_links.append(link.get('href'))
    return redirect_links

def parse_wikipedia_page(url):
    html_content = get_wikipedia_html_content(url)
    if html_content:
        title = extract_article_title(html_content)
        article_content = extract_article_text_with_headings(html_content)
        redirect_links = collect_redirect_links(url)
        
        result = {
            "title": title,
            "content": article_content,
            "redirect_links": redirect_links
        }
        return result
    else:
        return None

# Example usage:
wikipedia_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
parsed_data = parse_wikipedia_page(wikipedia_url)

# To print the title, article content, and redirect links:
print("Title:", parsed_data["title"])
print("Content:", parsed_data["content"])
print("Redirect Links:", parsed_data["redirect_links"])
