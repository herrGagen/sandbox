CREATE TABLE players
				(playerID Integer Primary Key
                ,FirstName text
                ,LastName text
				{% for i in range(n) %}
					,Week{{i}} boolean
				{% endfor %}
				);