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

Test Case 5 - Cross-Site Scripting (XSS)
Test Methodology:
1. Create account or login
2. Navigate to create post page
3. Enter malicious XSS payload in post content:
<div style="position:fixed;top:0;left:0;width:100%;height:100%;background:red;z-index:9999;padding:50px;color:white;font-size:30px;"> 
HACKED! Your account has been compromised! Send $1000 to recover it! </div>
4. Submit the post
5. View the post as another user
6. Baseline - Vulnerable: Red warning displays across entire screen
7. Hardened - Secure: HTML tags stripped, only plain text displayed

Test Case 6 - Hardcoded Secrets
Test Methodology:
1. Run Snyk scan on baseline repository:
2. snyk code test
3. Review Snyk output for hardcoded credentials in:
vulpy.py (line 17)
vulpy-ssl.py (line 13)
libapi.py (line 10)
libsession.py (line 4)
Baseline - Vulnerable: 4 high-severity "Hardcoded Credentials" issues detected
4. Verify .env file exists and contains secrets
5. Verify .env is in .gitignore
6. Run Snyk scan again
Hardened - Secure: 0 hardcoded credential issues, secrets loaded from environment variables
