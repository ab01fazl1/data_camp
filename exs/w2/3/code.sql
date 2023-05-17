-- Section1

    SELECT m.title as 'title'
    FROM movie m
    LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
    WHERE mg.genre_id IS NULL;

-- Section2

    SELECT m.title as 'Title', p.person_name as 'Director/Leading actor'
    FROM movie m
    JOIN (
      SELECT mc.movie_id, mc.person_id
      FROM movie_cast mc
      WHERE mc.cast_order = 0
    ) c ON m.movie_id = c.movie_id
    JOIN (
      SELECT mc.movie_id, mc.person_id
      FROM movie_crew mc
      WHERE mc.job = 'Director'
    ) d ON m.movie_id = d.movie_id AND c.person_id = d.person_id
    JOIN person p ON c.person_id = p.person_id
    order by m.title;

-- Section3

    SELECT person.person_name as 'Name', COUNT(movie_cast.movie_id) AS count_of_movies
    FROM movie_cast
    INNER JOIN person ON movie_cast.person_id = person.person_id
    WHERE movie_cast.cast_order = 0
    GROUP BY person.person_id
    ORDER BY count_of_movies DESC, person.person_name;

-- Section4

    SELECT g.genre_name as genre, AVG(m.vote_average) AS avg_rating, MAX(m.vote_average) AS max_rating, MIN(m.vote_average) AS min_rating
    FROM genre g
    INNER JOIN movie_genres mg ON g.genre_id = mg.genre_id
    INNER JOIN movie m ON mg.movie_id = m.movie_id
    GROUP BY g.genre_id
    ORDER BY avg_rating desc;

-- Section5

    SELECT p1.person_name AS `person #1`, p2.person_name AS `person #2`, COUNT(DISTINCT mc1.movie_id) AS movies_played_together
    FROM movie_cast mc1
    INNER JOIN movie_cast mc2 ON mc1.movie_id = mc2.movie_id AND mc1.person_id < mc2.person_id
    INNER JOIN person p1 ON mc1.person_id = p1.person_id
    INNER JOIN person p2 ON mc2.person_id = p2.person_id
    GROUP BY p1.person_id, p2.person_id
    ORDER BY movies_played_together DESC, p1.person_name, p2.person_name
    LIMIT 10;