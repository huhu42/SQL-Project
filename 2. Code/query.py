import sqlite3
import pprint


db = sqlite3.connect("database.db") # connect to the database file

c = db.cursor()



# 1. number of nodes
nodes_num = '''
SELECT COUNT(*)
FROM nodes
'''

# 2. number of ways
ways_num = '''
SELECT COUNT(*)
FROM ways;
'''

# 3. number of highways nodes
num_highways = '''
SELECT COUNT(DISTINCT(id))
FROM nodes_tags
WHERE key = "highway";
'''

#4. Top 10 types of way tag:
ways_types = '''
SELECT type, COUNT(*)
FROM ways_tags
GROUP by type
ORDER by COUNT(*) DESC
LIMIT 10;
'''


#5. Top 10 keys for address:
addr_keys = '''
SELECT key, count(*)
FROM ways_tags
WHERE type = 'addr'
GROUP by key
ORDER by COUNT(*) DESC
LIMIT 10;
'''

#6. Top 10 users:
big_users = '''
SELECT e.user, COUNT(*)
FROM (SELECT user FROM nodes
	  UNION ALL
      SELECT user FROM ways) e
GROUP by e.user
ORDER by COUNT(*) DESC
LIMIT 10;

'''

#7. Number of restaurants by tag key:
tor_rest = '''
SELECT KEY, COUNT(DISTINCT(ID))
from nodes_tags
WHERE value = 'restaurant'
GROUP by key;
'''


#8. All restaurant tag keys
rest_attrib = '''
SELECT key, COUNT(*)
FROM nodes_tags JOIN
(SELECT DISTINCT(id) from nodes_tags where value = 'restaurant') as u
WHERE u.id = nodes_tags.id
GROUP by key
ORDER by COUNT(*) DESC;
'''


c.execute(rest_attrib)
rows = c.fetchall()

pprint.pprint (rows)
