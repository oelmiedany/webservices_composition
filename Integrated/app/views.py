from app import app
from flask import Flask, request, render_template, redirect
from .forms import *
import json
import requests
import logging

logging.basicConfig(filename='log.txt', 
                    level=logging.DEBUG, 
					format='%(levelname)s:%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S'
                    )

class Film():
	def __init__(self, d):
		self.title = d["title"]
		self.year = d["year"]
		self.genre = d["genre"]
		self.duration = d["duration"]
		self.actors = d["actors"]

class NYTimesInfo():
	def __init__(self, d):
		if d:
			self.headline = d["headline"]
			self.url = d["link"]["url"]
			if d["critics_pick"] == 1:
				self.critics_pick = 'Yes'
			else:
				self.critics_pick = 'No'
		else:
			self.headline = "no review"

#logs information about the request
def log_request_info():
	#convert access_route list into string format
	access_route = ""
	for ip in request.access_route:
		access_route += ip + " "

	#log the IP address, user agent and access route of requester
	logging.info("Request from: %s  User agent: %s  Access route: %s",
				request.remote_addr, request.user_agent.string, access_route)

	return

#home route
@app.route('/', methods=['GET', 'POST'])
def homeScreen():
	#initialise variables
	dateForm = DateForm()
	date = ""
	films = []
	directors = []

	#get cinema film data for a specific input date
	if dateForm.validate_on_submit():
		date = dateForm.date.data
		#set up webservice 1 url and response data
		s1_url = "http://localhost:9988/whatsonrest/whatson/query/" + date
		s1_response = requests.get(s1_url)
		s1_data = s1_response.json()

		#add data to arrays that are fed into template
		for f in s1_data:
			films.append(f["title"])
			directors.append(f["director"])

	return render_template('home.html', dateForm=dateForm, films=films, directors=directors, date=date)

#method for testing 3rd web service
@app.route('/test', methods=['GET'])
def test():
	apiKey = '7JRQGpEB0FUBKCmQ12pyirmAhmJYYNaF'
	s3_url = "https://api.nytimes.com/svc/movies/v2/reviews/search.json"
	s3_params = {'query': 'Baby driver', 'api-key': apiKey}
	s3_response = requests.get(s3_url, params=s3_params)

	s3_data = s3_response.json()

	return s3_data

#display all films by specific director along with NYTimes review
@app.route('/director-films/<director>', methods=['GET'])
def directorFilms(director):
	#initialise arrays
	films = []
	nytimes_info = []

	#set up service 2 and service 3 requests and response for s2
	s2_url = "http://127.0.0.1:4500/by-director/" + director
	s2_response = requests.get(s2_url)

	apiKey = '7JRQGpEB0FUBKCmQ12pyirmAhmJYYNaF'
	s3_url = "https://api.nytimes.com/svc/movies/v2/reviews/search.json"

	#add films from s2 data
	if s2_response.status_code == 200:
		data = s2_response.json()
		for f in data['films']:
			films.append(Film(f))

	#initialise pick and review count used to calculate critic pick ratio
	pick_count = 0
	review_count = 0
	#step through each film and generate the response from service 3
	for f in films:
		s3_params = {'query': f.title, 'api-key': apiKey}
		s3_response = requests.get(s3_url, params=s3_params)
		s3_data = s3_response.json()

		#check if there is a review in the response
		if s3_response.status_code == 200 and s3_data['num_results'] != 0:
			#add the review data
			info = NYTimesInfo(s3_data["results"][0])
			nytimes_info.append(info)
			#update review and pick count
			review_count += 1
			if info.critics_pick == "Yes":
				pick_count += 1
		else:
			nytimes_info.append(NYTimesInfo(None))

	#calculate critic pick ratio
	if review_count > 0:
		critic_ratio = pick_count / review_count

	return render_template('director_films.html', director=director, films=films, nytimes_info=nytimes_info, critic_ratio=critic_ratio)
