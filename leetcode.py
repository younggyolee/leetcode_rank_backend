import requests
import json

def get_data_from_leetcode(username):
    query = '''
        query userContestRankingInfo($username: String!) {
            userContestRanking(username: $username) {
                rating
                topPercentage
            }
        }
    '''
    variables = {'username': username}
    url = 'https://leetcode.com/graphql/'

    try:
        r = requests.post(url, json={'query': query , 'variables': variables})
        data = json.loads(r.text)['data']
        return {
            'rating': data['userContestRanking']['rating'],
            'topPercentage': data['userContestRanking']['topPercentage']
        }
    except Exception as e:
        print(str(e))
        raise Exception('error while fetching!')