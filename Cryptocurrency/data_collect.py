# https://www.analyticsvidhya.com/blog/2018/09/multivariate-time-series-guide-forecasting-modeling-python-codes/
# https://www.coingecko.com/api/documentations/v3#/
#

import requests
import json
import pandas as pd

class CoinGeckoApi:

    def __init__(self, crypto='bitcoin', ccy='usd'):
        self.crypto = crypto
        self.ccy = ccy
        self.api_url_base = 'https://api.coingecko.com/api/v3/'
        self.headers = {'Content-Type': 'application/json'}
        print("CRYPTO: {0} || CCY: {1}".format(crypto, ccy))

    def get_data(self, date):
        ## RegEx check
        # dd-mm-yyyy
        print("DATE: {0}".format(date))
        api_url = "{0}coins/bitcoin/history?date={1}".format(self.api_url_base, date)
        response = requests.get(api_url, headers=self.headers)
        if response.status_code == 200:
            api_data = json.loads(response.content.decode('utf-8'))
            api_data_selected = [[
                                date,
                                self.ccy,
                                self.crypto,
                                api_data['market_data']['current_price'][self.ccy] ,
                                  api_data['market_data']['market_cap'][self.ccy] ,
                                  api_data['market_data']['total_volume'][self.ccy] ,

                                  api_data['community_data']['facebook_likes'] ,
                                  api_data['community_data']['twitter_followers'] ,
                                  api_data['community_data']['reddit_average_posts_48h'] ,
                                  api_data['community_data']['reddit_average_comments_48h'] ,
                                  api_data['community_data']['reddit_subscribers'],
                                  api_data['community_data']['reddit_accounts_active_48h'] ,

                                  api_data['developer_data']['forks'] ,
                                  api_data['developer_data']['stars'] ,
                                  api_data['developer_data']['subscribers'] ,
                                  api_data['developer_data']['total_issues'] ,
                                  api_data['developer_data']['closed_issues'] ,
                                  api_data['developer_data']['pull_requests_merged'] ,
                                  api_data['developer_data']['pull_request_contributors'] ,
                                  api_data['developer_data']['commit_count_4_weeks'] ,

                                  api_data['public_interest_stats']['alexa_rank'],
                                  api_data['public_interest_stats']['bing_matches']
                                  ]]

            #print(api_data_selected)
            api_data_df = pd.DataFrame(data=api_data_selected,
                                       columns= ['date', 'ccy', 'crypto',
                                            'current_price', 'market_cap', 'total_volume',

                                               'facebook_likes', 'twitter_followers',
                                               'reddit_average_posts_48h', 'reddit_average_comments_48h',
                                               'reddit_subscribers', 'reddit_accounts_active_48h',

                                               'forks', 'stars', 'subscribers', 'total_issues',
                                               'closed_issues', 'pull_requests_merged',
                                               'pull_request_contributors', 'commit_count_4_weeks',

                                               'alexa_rank', 'bing_matches'])

            print(api_data_df.columns)
            print(api_data_df.shape)
            print(api_data_df.get_values())
            print("RETURNING POPULATED DF")
            return api_data_df
        else:
            print("RETURNING NONE")
            return None

if __name__ == '__main__':
    cga = CoinGeckoApi()
    df = cga.get_data('30-12-2018')




