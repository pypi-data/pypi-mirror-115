# academic_tweet
API wrapper for academic track Twitter


The package contains a wrapper for the new v2 twitter API, developed especially for use with academic track acces to the API.

The package functions in threee eaasy steps:
- - Create a tweeter object with your' twitter API bearer token
- - Set the parameters of you query by setting the .params of the object
- - Make the appropriate call to the API using the .twitter_search() method, with the correct call = specified 

See the test notebook for an example of the use case

Implemented calls: 

The call names are consistently named after the the name of the api endpoint in the v2 api, though they are sometimes odd. 

search: 
- Full archive tweet search using query (can search for hashtags or text) 
- https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
- 300 requests per 15-minute (also a 1 per sec limit)

 user_tweets: 
 - Tweets of a specific user id (Similar to the old user timeline from v1)
 - https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
 - 1500 requests per 15-minute

 user_mentions: 
 - Mentions of a specific user id 
 - https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-mentions
 - 450 requests per 15-minute

 user_id: 
 - Information about the user(s) by id(s). A list of ids can be provided with comma (no space)
 - https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
 - 300 requests per 15-minute

 user_name: 
 - Information about the user(s) by username(s). A list of names can be provided with comma (no space)
 - https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by
 - 300 requests per 15-minute

 following: 
 - A list of accounts that the given user id follows
 - https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-following
 - 15 request per 15-minute

 followers: 
 - A list of accounts that the given user id is followed by
 - https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers
 - 15 request per 15-minute

To see what paramters you want to set see: https://developer.twitter.com/en/docs/twitter-api/early-access


The package is deceloped by August Lohse, for my work as a Ph.D student at SODAS at UCPH. It is freely availbe for use for everyone, just give credit where it is due. 
