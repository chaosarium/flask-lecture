## HTTP

- Stands for **Hypertext Transfer Protocol**
- A standard for how computers should talk to each other through internet connection, basically
- HTTP requests — whenever you want to get information, send message, etc.

An example http request (from Wikipedia):

```text
GET / HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

Here, we see that this is a `GET` request to `www.example.com` to request data at `/` sent via `Mozilla/5.0` etc...

And here's the response

```text
HTTP/1.1 200 OK
Date: Mon, 23 May 2005 22:38:34 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 155
Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT
Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)
ETag: "3f80f-1b6-3e1cb03b"
Accept-Ranges: bytes
Connection: close

<html>
  <head>
    <title>An Example Page</title>
  </head>
  <body>
    <p>Hello World, this is a very simple HTML document.</p>
  </body>
</html>
```

We see a status code `200`, date, time, content type, ..., and the data we got back, which is some `html` code. 

If you open the inspect panel on your browser and go to the `Network` tab, chances are you will see http requests flying around.

(You may also see `https` somewhere. That's `http` with encryption)

In the example, we saw a `GET` request, but there are more. We'll briefly go over the two most common ones:

- `GET` is usually when you want to... duh get something
- `POST` is when you have data you want to send to the server

These requests can have some "payload". There are many places where you can include data in the request and in many different formats.

- `headers` is usually for metadata-ish key-value pairs
- `body` is where most of the data is
- `url params` is literally data embedded in the url. 
  - For example, when you do a google search, you see the url looks something like this: `https://www.google.com/search?q=http&newwindow=1`. The params are:
    - `q` which has value `http`
    - `newwindow` which has value `1`
