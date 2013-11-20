import twitter
import csv
import datetime

def main():
	# consumer keys are fixed; get the access tokens by running get_access_token.py
	api = twitter.Api(consumer_key='v6gTWjtVMytN9KHeU3ZHA',
                      consumer_secret='sc2zbFaqqCLR5IDyzB6NyFZqte2X8SqC4WljSas',
                      access_token_key='2792071-0sRZQSKrLlwSwFs6zzIoTgV2wh9Lud5f9y42aqU530',
                      access_token_secret='KBoLWRe5nMH6AXlawZUspsl1TBKT81CyNvunEGFrcqTzD')
	# print api.VerifyCredentials()

	data_file = open('tweet_data.csv','wb')
	csv_writer = csv.writer(f)

	user_limits = [
		{ 'screen_name': 'BarackObama', 'since_id': 383978603974643712, 'max_id': 395696484827402240 }
	]

	cum_statuses = 0
	requests = 0
	for user in user_limits:
		statuses = api.GetUserTimeline(screen_name=user['screen_name'], 
										since_id=user['since_id'], 
										max_id=user['max_id'], 
										count=200)
		requests += 1

		for (i, status) in enumerate(statuses):
			csv_writer.writerow([status.created_at, user['screen_name'], status.text.encode('utf-8'), status.retweet_count, status.favorite_count])
		cum_statuses += 200
		
		if requests % 175 == 0:
			print "Warning: Reached 175 request threshold"
			print "Dumping data to file"
			data_file.flush()
			data_file.close()
			print "Going to sleep for 15 minutes; will awake at: {0}".format(str(datetime.datetime.now() + datetime.timedelta(minutes=15)))
			sleep(15 * 60)
			data_file = open('tweet_data.csv','wb')

	print "Job completed"
	print "Closing files"
	data_file.flush()
	data_file.close()
	print "Closed files"
	print "Cumulative tweets captured: {0}".format(cum_statuses)
	print "API requests: {0}".format(requests)

if __name__ == '__main__':
	main()