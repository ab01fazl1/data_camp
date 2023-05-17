
-- Section1

   select p.platform_name as 'platform_name', AVG(rs.num_sales) as 'Average'
   from platform p
   join game_platform on game_platform.platform_id = p.id
   join region_sales rs on game_platform.id = rs.game_platform_id
   group by p.platform_name
   order by AVG(rs.num_sales) DESC;

-- Section2

   select g.game_name as 'game_name', gpub.publisher_name as 'publisher_name', gp.platform_name as 'platform_name', gp.release_year as 'release_year', sum(rs.num_sales) as 'global_sales'
   from game g
   join (select gp.id, gp.game_id, p.publisher_name
         from game_publisher gp
         join publisher p
         on gp.publisher_id = p.id) gpub on gpub.game_id = g.id
   join (select gp.id, gp.game_publisher_id, p.platform_name, gp.release_year
         from platform p
         join game_platform gp
         on gp.platform_id = p.id) gp on gp.game_publisher_id = gpub.id
   join region_sales rs on rs.game_platform_id = gp.id
   group by g.game_name, gp.platform_name
   order by sum(rs.num_sales) DESC
   limit 20;

-- Section3

   select game.game_name as 'game_name', count(distinct game_platform.platform_id) as 'platform_count' from game_platform
   join game_publisher on game_platform.game_publisher_id = game_publisher.id
   join game on game_publisher.game_id = game.id
   group by game_name
   order by count(distinct game_platform.platform_id) DESC;

-- Section4

   SELECT
       pl.platform_name AS platform,
       g.genre_name AS genre,
       dense_rank() OVER (PARTITION BY pl.id ORDER BY SUM(s.num_sales) DESC) AS genre_in_platform_rank,
       SUM(s.num_sales) AS genre_sale,
       dense_rank() OVER (ORDER BY SUM(s.num_sales) DESC) AS total_rank
   FROM
       genre g
       JOIN game ga ON g.id = ga.genre_id
       JOIN game_publisher gp ON ga.id = gp.game_id
       JOIN game_platform p ON gp.id = p.game_publisher_id
       JOIN platform pl ON p.platform_id = pl.id
       JOIN region_sales s ON p.id = s.game_platform_id
   WHERE
       pl.id IS NOT NULL
   GROUP BY
       pl.platform_name,
       g.genre_name
   ORDER BY
       genre_sale DESC, platform, genre;


