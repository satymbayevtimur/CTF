# logon
- Tags: Web Exploitation
- Description: The factory is hiding things from all of its users. Can you login as Joe and find what they've been looking at? (link)

# Solution
- Let's open the link and register a user.
- In cookies we can see flag "admin", which is equals "False".
- We can change it to "True", refresh the page and retrieve the flag.

```
picoCTF{th3_c0nsp1r4cy_l1v3s_6edb3f5f}
```
