Test Case 1 - Brute Force
Test Methodology:
1.	Create testing account
2.	Configure Burp Suite Intruder with login POST request
3.	Set payload position on password field
4.	Execute attack
5.	Monitor Responses to confirm working lockout after 5th and 6th attempts

Test Case 2 - SQL Injection
1.	Scan web application using preferred scanner such as Snyk or Bandit
2.	GIVEN registration form, enter the malicious query test'); SELECT * FROM users; -- into username section, which in turn should throw a SQLite3 error.
3.	Record Results


