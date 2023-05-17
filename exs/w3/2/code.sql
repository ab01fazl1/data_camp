-- Section1
    select p.title as 'p_title', c.title as 'c_title' from submissions s
    join problems p on s.problem_id = p.id
    join contests c on c.id = p.contest_id
    group by s.problem_id, p.contest_id
    order by count(problem_id) DESC, p.title, c.title;

-- Section2
    SELECT c.title as 'title', COUNT(DISTINCT s.user_id) AS 'amount'
    FROM submissions s
    JOIN problems p ON s.problem_id = p.id
    JOIN contests c ON p.contest_id = c.id
    GROUP BY c.id
    ORDER BY COUNT(DISTINCT s.user_id) DESC, c.title ASC;

-- Section3
   SELECT u.name as 'name', SUM(s.max_score) as 'score'
    FROM users u
    JOIN (
      SELECT user_id, problem_id, MAX(score) as max_score
      FROM submissions
      WHERE problem_id IN (
        SELECT id
        FROM problems
        WHERE contest_id = (
          SELECT id
          FROM contests
          WHERE title = 'mahale'
        )
      )
      GROUP BY user_id, problem_id
    ) s ON u.id = s.user_id
    GROUP BY u.id
    ORDER BY SUM(s.max_score) DESC, u.name ASC;
-- Section4
   SELECT u.name as 'name', SUM(sp.max_score) AS 'score'
    FROM (
        SELECT problem_id, user_id, MAX(score) AS max_score
        FROM submissions
        GROUP BY problem_id, user_id
    ) AS sp
    JOIN users u ON sp.user_id = u.id
    JOIN problems p ON sp.problem_id = p.id
    JOIN contests c ON p.contest_id = c.id
    GROUP BY u.name
    ORDER BY SUM(sp.max_score) DESC, u.name ASC;

-- Section5
   update contests
    set title = 'Mosabeghe Mahale'
    where title = 'mahale';
-- Section6
   DELETE FROM contests c
    WHERE c.id NOT IN (
      SELECT DISTINCT c.id
      FROM problems
      inner join problems p on c.id = p.contest_id
      INNER JOIN submissions ON problems.id = submissions.problem_id
    )