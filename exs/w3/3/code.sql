
-- Section1

   SELECT DISTINCT p.family_name as 'family_name', p.given_name as 'name', p.birth_date as 'birth_date',
        CASE t.team_name
            WHEN 'Serbia and Montenegro' THEN 'Serbia'
            WHEN 'Yugoslavia' THEN 'Serbia'
            ELSE t.team_name
        END AS 'team_name'
    FROM players p
    JOIN player_appearances s ON p.player_id = s.player_id
    JOIN teams t ON s.team_id = t.team_id
    WHERE p.family_name LIKE '%ić' AND t.team_name <> 'Croatia'
    ORDER BY t.team_name, p.birth_date, p.family_name, p.given_name;

-- Section2

   SELECT
       t.team_name AS team_name,
        SUM(
            CASE ts.position
                WHEN 1 THEN 4
                WHEN 2 THEN 3
                WHEN 3 THEN 2
                WHEN 4 THEN 1
            END
        ) AS total_score
    FROM
        tournament_standings ts
        JOIN teams t ON ts.team_id = t.team_id
    GROUP BY
      CASE WHEN t.team_name = 'West Germany' THEN 'Germany'
           ELSE t.team_name
      END
    ORDER BY
        total_score DESC, team_name
    LIMIT 10;


-- Section3

   your third query here

-- Section4

   your fourth query here