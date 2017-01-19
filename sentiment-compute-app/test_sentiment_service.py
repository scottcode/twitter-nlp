import sys
import json

from sentiment_service import cl


def sentiment_score(payload):
    X = payload['data']
    prediction = cl.predict_proba(X)[:][:,1]
    return prediction

if __name__ == '__main__':
    json_data = """{"data": [{"created_at":"Mon Jan 16 15:57:34 +0000 2017","id":821023597573476352,"id_str":"821023597573476352","text":"Def Leppard, Poison, and Tesla are touring together and the closest they are coming is Fresno. Who goes to Fresno??? \ud83d\ude2d","source":"\u003ca href=\"http:\/\/twitter.com\/download\/iphone\" rel=\"nofollow\"\u003eTwitter for iPhone\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":28614063,"id_str":"28614063","name":"Betsy Langowski","screen_name":"superbetsy","location":"Campbell, CA","url":null,"description":"\uf8ff. Star Wars\/Zelda\/Math. Proud wearer of dog hair. Minnesota transplant. Video games. Books. Generalized epic geek.","protected":false,"verified":false,"followers_count":1580,"friends_count":433,"listed_count":77,"favourites_count":1381,"statuses_count":22106,"created_at":"Fri Apr 03 17:46:53 +0000 2009","utc_offset":-21600,"time_zone":"Central Time (US & Canada)","geo_enabled":true,"lang":"en","contributors_enabled":false,"is_translator":false,"profile_background_color":"FF6699","profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme11\/bg.gif","profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme11\/bg.gif","profile_background_tile":true,"profile_link_color":"D11957","profile_sidebar_border_color":"CC3366","profile_sidebar_fill_color":"E5507E","profile_text_color":"362720","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/814142404206817280\/xCbZIvRx_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/814142404206817280\/xCbZIvRx_normal.jpg","profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/28614063\/1400806485","default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":{"id":"0354c827bfda68de","url":"https:\/\/api.twitter.com\/1.1\/geo\/id\/0354c827bfda68de.json","place_type":"city","name":"Campbell","full_name":"Campbell, CA","country_code":"US","country":"United States","bounding_box":{"type":"Polygon","coordinates":[[[-121.991728,37.254665],[-121.991728,37.307009],[-121.918729,37.307009],[-121.918729,37.254665]]]},"attributes":{}},"contributors":null,"is_quote_status":false,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"filter_level":"low","lang":"en","timestamp_ms":"1484582254199"}]}"""
    full = json.loads(json_data)
    sys.stdout.write(sentiment_score(full))
