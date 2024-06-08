import requests

where_value = 'nexearch' 
sm_value = 'top_hty'
fbm_value = 1
ie_value = 'utf8'
query_value = 'python'

base_url = "https://search.naver.com/search.naver"
parameter = "?where={0}&sm={1}&fbm={2}&ie={3}&query={4}".format(where_value, sm_value, 
                                                                fbm_value, ie_value, 
                                                                query_value)
url_para = base_url + parameter
r = requests.get(url_para)

print(r.url)
