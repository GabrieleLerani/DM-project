-- Insert new user with random id
DO $$
DECLARE test_uid int := CAST(FLOOR(RANDOM()*(290000-300000  + 1)) + 300000 AS int8);
BEGIN 
	INSERT INTO user_data VALUES (test_uid, 'test','test','30');
    INSERT INTO rating VALUES (test_uid, '0522848966','8.0');	
END $$; 


-- Remove test user and ratings
DO $$
BEGIN 
	DELETE FROM rating WHERE isbn = '0522848966' and rating = '8.0';
	DELETE FROM user_data WHERE country = 'test' and province = 'test' and age = '30';
END $$;


-- Test inserction of new element
select * from user_data where country = 'test'
select * from rating where isbn = '0522848966' and rating = '8.0'