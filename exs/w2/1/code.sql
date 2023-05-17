-- Section1

   ALTER TABLE users
   DROP COLUMN date_joined;

-- Section2

   UPDATE users
   SET email = 'new3@example.com'
   WHERE user_id = 3;

-- Section3

   UPDATE users
   SET username = CONCAT('@', username)
   WHERE username NOT LIKE '@%';

-- Section4

   INSERT INTO users (username, password, email) VALUES
   ('@user4', 'password4', 'user4@example.com');

-- Section5

   select * from users
   WHERE username = '@user4';

-- Section6

   UPDATE comments
   SET content = REPLACE(content, 'hate', '****')
   WHERE content LIKE '%hate%';