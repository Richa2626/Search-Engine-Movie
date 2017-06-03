import requests
from bs4 import BeautifulSoup

baseUrl = "http://www.imdb.com"


#get movie name and make a url to fetch movie details from imdb

def create_url(query):
	url ="http://www.imdb.com/find?ref_=nv_sr_fn&q="
	query = query.replace(" ","+")
	url = url+query+'&s=all'
	return url


#extract all the links for a particular movie

def extract_all_items(url):
	global baseUrl
	res = requests.get(url)
	con = res.text
	soup = BeautifulSoup(con,  "html.parser")
	main_div = soup.find("div", {"id":"main"})
	divs = main_div.findAll("div", {"class": "findSection"})

	# getting table with Title
	mydiv = ""
	for div in divs:
		if div.find("h3").text == "Titles":
			mydiv = div
			break
	if mydiv == "":
		return {}
	else:
		table = mydiv.find("table", {"class": "findList"})
		rows = table.findAll("tr")
		results = {}
		for row in rows:
			columns = row.findAll("td")
			movie_url = columns[1].find("a").get("href")
			movie_name = columns[1].text
			results.update({baseUrl+movie_url : movie_name})
		return results


#return all the movie details

def get_movie_details(url):
	movie_name, movie_director,certificate, duration,movie_image_url,movie_video_url, genre, release_date,movie_credit_summary = ['']*9
	ratings = 0
	res = requests.get(url)
	con = res.text
	soup = BeautifulSoup(con,  "html.parser")

	div = soup.find("div", {"id":"title-overview-widget"})

	movie_name_div = div.find("div", {"class" : "title_wrapper"})
	if movie_name_div is not None:
		movie_name = movie_name_div.h1.text

	ratings_div = div.find("div", {"class" : "ratingValue"})
	if ratings_div is not None:
		ratings = ratings_div.span.text

	movie_image_url_div = div.find("div" , {"class" : "poster"})
	if movie_image_url_div is not None:
		movie_image_url = movie_image_url_div.img['src']

	movie_video_url_div = div.find("div" , {"class" : "slate"})
	if movie_video_url_div is not None:
		movie_video_url = baseUrl + movie_video_url_div.a['href']

	movie_details_div = div.find("div", {"class" : "subtext"})
	if movie_details_div is not None:
		movie_details = movie_details_div.text
		if '|' in movie_details:
			movie_details_info = movie_details.split('|')
		if movie_details_info[0] is not None:
			certificate = movie_details_info[0].strip()
		if movie_details_info[1] is not None:
			duration = movie_details_info[1].strip()

	movie_credit_summary_div = div.find("div", {"class" : "summary_text"})
	if movie_credit_summary_div is not None:
		movie_credit_summary = movie_credit_summary_div.text.strip()

	movie_details = [movie_name, movie_director, ratings, certificate, duration,
						movie_image_url, movie_video_url,genre, release_date,
						movie_credit_summary]

	return movie_details
