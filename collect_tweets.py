import twitter
from twitter import TwitterError
import csv, json, calendar, datetime
from time import sleep

requests = 0
cum_statuses = 0 
earliest_tweet_id = None
data_file = None
api = None

def fetch_tweets(sn, sid, mid):
	global requests
	global api

	rate_limits = api.GetRateLimitStatus()
	if rate_limits['resources']['statuses']["/statuses/user_timeline"]['remaining'] == 0:
		print "Warning: Rate limit reached"
		time_now_epoch = calendar.timegm(time.gmtime())
		print "Going to sleep for {0} seconds".format(time_now_epoch - rate_limits['reset_time_in_seconds'])
		sleep(time_now_epoch - rate_limits['reset_time_in_seconds'])
	requests += 1
	return api.GetUserTimeline(screen_name=sn, since_id=sid, max_id=mid, count=100)


def write_statuses(sn, statuses):
	global data_file
	global cum_statuses

	data_file = open('tweet_data.csv','ab')
	csv_writer = csv.writer(data_file)
	for (i, status) in enumerate(statuses):
		csv_writer.writerow([status.created_at, sn, status.text.encode('utf-8'), status.retweet_count, status.favorite_count])
	cum_statuses += len(statuses)
	data_file.flush()
	data_file.close()

def main():
	# consumer keys are fixed; get the access tokens by running get_access_token.py
	# storing them in a JSON file for now
	global api
	global cum_statuses
	global requests

	credentials = json.loads(open('credentials.json').read())
	api = twitter.Api(consumer_key=credentials['consumer_key'],
                      consumer_secret=credentials['consumer_secret'],
                      access_token_key=credentials['access_token_key'],
                      access_token_secret=credentials['access_token_secret'])
	# print api.VerifyCredentials()

	user_limits = [
		{'screen_name':'whitehouse', 'since_id':379624790585135107,'max_id':390248610731806720}
	]

	for user in user_limits:
		print "Collecting tweets for {0}; requests={1}".format(user['screen_name'], requests)
		statuses = fetch_tweets(user['screen_name'], user['since_id'], user['max_id'])
		write_statuses(user['screen_name'], statuses)
		earliest_tweet_id = reduce(lambda s1, s2: min(s1, s2), map(lambda s: s.id, statuses))
		while earliest_tweet_id > user['since_id']:
			print "\tIterating; requests={0}, earliest={1}, since_id={2}".format(requests, earliest_tweet_id, user['since_id'])
			statuses = fetch_tweets(user['screen_name'], user['since_id'], earliest_tweet_id)
			write_statuses(user['screen_name'], statuses)
			earliest_tweet_id = reduce(lambda s1, s2: min(s1, s2), map(lambda s: s.id, statuses))
		print "Done with tweets for {0}".format(user['screen_name'])

	print "Job completed"
	# print "Closing files"
	# data_file.flush()
	# data_file.close()
	# print "Closed files"
	print "Cumulative tweets captured: {0}".format(cum_statuses)
	print "API requests: {0}".format(requests)

if __name__ == '__main__':
	main()