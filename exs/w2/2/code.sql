-- Section1

  SELECT family_name , given_name as 'name'
  FROM players
  WHERE given_name LIKE '%pir%' OR family_name LIKE '%pir%';

-- Section2

  SELECT shirt_number, COUNT(*) as count_shirt_number
  FROM player_appearances
  GROUP BY shirt_number
  HAVING count_shirt_number > 1000
  ORDER BY count_shirt_number DESC;

-- Section3

  SELECT distinct p.family_name as 'family_name', p.given_name as 'name'
  FROM players p
  INNER JOIN (
    SELECT player_id
    FROM award_winners
    WHERE award_id = 'A-8'
  ) aw1 ON p.player_id = aw1.player_id
  INNER JOIN (
    SELECT player_id
    FROM award_winners
    WHERE award_id <> 'A-8'
  ) aw2 ON aw1.player_id = aw2.player_id
  order by 'family_name';
