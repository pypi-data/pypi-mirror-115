import requests
import time


class tweeter:
    '''This class holds the authenticaiton for the academic access, 
       as well as methods for query search (ex hashtags or text), as well as mentions and users.
       It supports the Twitter api 2 endpoints of academic full archive search'''
    
    def __init__(self, key = "", params = dict()):
        '''Define the key for academic access (not the two you would need for the old access)'''
        
        self.key = key
        self.params = params
        
    #set the parameters
    
    
    def create_url(self, q, call = "search"):
        '''Function returns the main body of the url, inputting q into the string.'''

        if call == "search":
            return "https://api.twitter.com/2/tweets/search/all?query={}".format(q)

        elif call == "user_tweets":
            return "https://api.twitter.com/2/users/{}/tweets".format(q)

        elif call == "user_mentions":
            return "https://api.twitter.com/2/users/{}/mentions".format(q)
        
        elif call == "user_id":
            return "https://api.twitter.com/2/users?ids={}".format(q)
        
        elif call == "user_name":
            return "https://api.twitter.com/2/users/by?usernames={}".format(q)
        
        elif call == "following":
            return "https://api.twitter.com/2/users/{}/following".format(q)
        
        elif call == "followers":
            return "https://api.twitter.com/2/users/{}/followers".format(q)
        
    
    def get_next_token(self, params, next_token = 0, call = "search"):
        '''The function adds the pagnation token to the parameters when there are mutiple pages. 
           Only used during the api call, does not need to be set manually. 
           If you want to set parameters set them directly in the object'''
        
        if call == "user_mentions" or call == "user_tweets" or call == "following" or call == "followers":
            token = "pagination_token"
            
        else:
            token = "next_token"

        if next_token != 0:
            params[token] = next_token
        
        self.params = params
        #return params
    
    def create_headers(self, bearer_token):
        '''This funciton simply creates the authetication in the header for the query
           Returns the header as a dictionary '''
        
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        
        return headers


    def connect_to_endpoint(self, url, headers, params):
        '''Function send the actuall get request to the url, with the specified headers as parameters
           Returns a json response object '''
        
        response = requests.request("GET", url, headers=headers, params=params)
        
        return response.json()

    def rate_limits(self,respect_limits = True, call = 'search'):
        '''This function determines if the call to twitter api should respect the rate limits. 
           Only set this to false if you know that you are retreiving less data, than the limits allows,
           as repeated breaking of the rate limits can get you banned. '''
        
        if respect_limits == True:
            
            #search
            if call == 'search': 
                time.sleep(3.00001)
                
            #user_tweets
            if call == 'user_tweets':
                time.sleep(0.60001)
            
            #user_mentions
            if call == 'user_mentions':
                time.sleep(2.00001)
            
            #user_id
            if call == "user_id":
                time.sleep(3.00001)
                
            #user_name
            if call == "user_name":
                time.sleep(3.00001)
            
            #following
            if call == "following":
                time.sleep(60.00001)
            
            #followers
            if call == "followers":
                time.sleep(60.00001)
        
    def twitter_search(self, q,call = "search", pages = 10000, respect_limits = True):
        '''The main method of the class for retrieving data. This method takes a query (q) and a type of query
           it then gets all the data for that query, using the authentication and parameters set before. 
           the results is returned as a list of the desired objects 
           
           The fucntion will only run for 10.000 pages before stopping. 
           If more is needed update the parameter in your call
        
        
         
           Call argument determines the type of call, the call names are consistently named after the 
           the name of the api endpoint in the v2 api, though they are sometimes odd. 
        

            ----implemented
            search: - Full archive tweet search using query (can search for hashtags or text) 
                    - https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
                    - 300 requests per 15-minute (also a 1 per sec limit)
                    
            user_tweets: - Tweets of a specific user id (Similar to the old user timeline from v1)
                         - https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
                         - 1500 requests per 15-minute
                         
            user_mentions: - Mentions of a specific user id 
                           - https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-mentions
                           - 450 requests per 15-minute

            user_id: - Information about the user(s) by id(s). A list of ids can be provided with comma (no space)
                     - https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
                     - 300 requests per 15-minute
                   
            user_name: - Information about the user(s) by username(s). A list of names can be provided with comma (no space)
                       - https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by
                       - 300 requests per 15-minute
                        
            following: - A list of accounts that the given user id follows
                       - https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-following
                       - 15 request per 15-minute
            
            followers: - A list of accounts that the given user id is followed by
                       - https://developer.twitter.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers
                       - 15 request per 15-minute
                    
            ----not implemented yet
            https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets
            https://developer.twitter.com/en/docs/twitter-api/tweets/retweets/api-reference/get-tweets-id-retweeted_by
            https://developer.twitter.com/en/docs/twitter-api/tweets/counts/api-reference/get-tweets-counts-all
            https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-tweets-id-liking_users
            https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-users-id-liked_tweets    

        '''
        
        
        dicts = []
        i = 0

        while i < pages - 1 :
            

            if i == 0:
                
                url = self.create_url(q, call)
                headers = self.create_headers(self.key)
                data = self.connect_to_endpoint(url, headers, self.params)
                
                try:
                    dicts.append(data['data'])
                except:
                    dicts.append(data)
                

            else:
                try:       
                    next_token = data['meta']['next_token']
                    
                    self.get_next_token(self.params, next_token = next_token, call = call)
                    
                    url = self.create_url(q, call)
                    headers = self.create_headers(self.key)
                    data = self.connect_to_endpoint(url, headers, self.params)

                    
                    dicts.append(data['data'])
                    
                    #check if there is another next token for next round
                    try: 
                        data['meta']['next_token']
                    
                    except KeyError:
                    
                    #remove the next_token from the params, in case we want to run it again from start
                        try:
                            self.params.popitem()
                        except:
                            pass
                    
                    #no more things to scrape
                        break
                        
                        
                except:
                    
                    #remove the next_token from the params, in case we want to run it again from start
                    try:
                        self.params.popitem()
                    except:
                        pass
                    
                    #no more things to scrape
                        break

            #print information
            print("Working on page {}".format(str(i+1)), end='\r')
            
            #respect the rate limit - if so wait an appropriate amount of time 
            self.rate_limits(respect_limits, call = call)
            
            #update counter
            i += 1

        print("All done!")

        #make to list
        final_list = []
        for i in dicts:
            for j in i:
                final_list.append(j)

        return final_list
    
 