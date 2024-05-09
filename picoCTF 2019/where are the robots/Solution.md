# where are the robots
- Tags: Web Exploitation
- Description: Can you find the robots? (link)

# Solution
- Follow the link, there you will see a simple web page. If we try access ./robots.txt, we will find some fields.
- What is "robots.txt"?
- A robots.txt file tells search engine crawlers which URLs the crawler can access on your site. This is used mainly to avoid overloading your site with requests; it is not a mechanism for keeping a web page out of Google. To keep a web page out of Google, block indexing with noindex or password-protect the page.
- Also, we can see in task's title the hint: "robots".

```
User-agent: *
Disallow: /8028f.html
```

- If we follow this link, there will be our flag.

```
picoCTF{ca1cu1at1ng_Mach1n3s_8028f}
```
