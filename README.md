

# Secure Python Coding

---

#### Agenda

- Introduction
- Top Security Vulnerabilities
- SQL Injection
- Cross Site Scripting
- Server-Side Request Forgery 
- Command Injection
- Supply chain attacks (pypy)
- Python Security Tips
- Appendix
- Module Highlights
- Questions
- Wrap up
 

 

>When you learn a language, a module or a framework, you learn how it is supposed to be used. When thinking about security, you need to think about how it can be misused.​

 
#### Top Python Security Vulnerabilities​

- SQL Injections (SQLi)
- XSS (Cross Site Scripting)
- Server-Side Request Forgery
- Command Injections
- Xpath Injections
- nsecure Deserialization (Pickeling)
- Directory Traversal
 
---


# SQLI
 Define what a sqli is

Detection methods

 

Attackers will hunt for SQL injection in a variety of ways. Submitting the single quote character ' and -- looking for errors or other anomalies.      
   
Ex 1: https://www.exampleurl.com/index?allUsers=1'-- AND active=1
>
       Ex 2: A user logins with user securityCoach' -- and a blank password​
                `SQL Interpretation SELECT * FROM users WHERE username = securityCoach' --' AND password = ''
   

2.  Submitting Boolean conditions such as `OR 1=1 and OR 1=2`, and looking for differences in the application's responses. `1=1` will always evaluate as a true result.

3. Submitting payloads designed to trigger time delays when executed within a SQL query, and  looking for differences in the time taken to respond.



High Risk Security Vulnerabilities
SQL Injection – Passing Safe Query Parameters



### BAD Vulnerable Example.  DON'T Do This!
cursor.execute("SELECT securitycoaches FROM users WHERE username = '" + username + '");
cursor.execute("SELECT securitycoaches min FROM users WHERE username = '{}'".format(username));

cursor.execute("SELECT securitycoaches FROM users WHERE username = '%s' % username);
cursor.execute(f"SELECT securitycoaches FROM users WHERE username = '{username}'");

 

### GOOD CODE

#### SAFE EXAMPLES. DO THIS!
cursor.execute("SELECT securitycoaches FROM users WHERE username = %s'", (username, ));
cursor.execute("SELECT securitycoaches FROM users WHERE username = %(username)s", {'username': username});


#### Preventing  SQLI

Use prepared statements and parametrized quries

Bind variables to SQL query parameters with dedicated methods
Validate parameters used to build queries. 
Sanitize Input 
Filter use very strict Regular Expression patterns (RegEx)


---

# XSS
 
 
Define/explain XSS

 - Vuln xss code vs safe code

 #### BAD CODE


templates/xss_shared.html
>
``<!doctype html>
`<title>Hello from Flask</title>`
``{% if name %}
  <h1>Hello {{ name }}!</h1>
``{% else %}
  <h1>Hello, World!</h1>
``{% endif %}



## XSS.py

>`@xss.route('/insecure/no_template_engine_replace', methods =['GET'])
>`def no_template_engine_replace():
   ` param = request.args.get('param', 'not set')
>
    `html = open('templates/xss_shared.html').read()
    `response = make_response(html.replace('{{ name }}', param)) # Noncompliant: ``param is not sanitized`
    `return response

 