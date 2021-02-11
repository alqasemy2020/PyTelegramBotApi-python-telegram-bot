# `f.data()` returns bytes not str so just use `f.data().decode('utf-8')` like:
# ```
# import urllib3
# import networkx as nx

# url = 'https://raw.githubusercontent.com/leanhdung1994/WebMining/main/airports.net'
# http = urllib3.PoolManager()
# f = http.request('GET', url)
# G = nx.read_pajek(f.data.decode('utf-8'), encoding = 'UTF-8')
# print(G)
# ```

me = 'رفع منشئ اساسي'

rank_to_promotion = me
print([rank_to_promotion])