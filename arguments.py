#!/usr/bin/python

#global imports
import optparse

#local imports
import payloads as payload_module

def get_arguments():
    targets = []
    fuzzing = False
    type = None
    payload_codes = None
    usage = "python3 xss_scanner.py [-parameters] [arguments]\n" \
            "TYPES OF PAYLOADS:\n" \
            "    basic       Basic payload\n" \
            "    div         DIV Payload\n" \
            "    img         IMG Payload\n" \
            "    body        BODY Payload\n" \
            "    svg         SVG Payload\n\n" \
            "Payload Codes:\n" \
            "    1           UPPER CASE\n" \
            "    2           UPPER AND LOWER CASE\n" \
            "    3           URL ENCODE\n" \
            "    4           HTML ENTITY ENCODE\n" \
            "    5           SPLIT PAYLOAD\n" \
            "    6           HEX ENCODE\n" \
            "    7           UTF-16 ENCODE\n" \
            "    8           UTF-32 ENCODE\n" \
            "    9           DELETE TAG\n" \
            "    10          UNICODE ENCODE\n" \
            "    11          US-ASCII ENCODE\n" \
            "    12          BASE64 ENCODE\n" \
            "    13          UTF-7 ENCODE\n" \
            "    14          PARENTHESIS BYPASS\n" \
            "    15          UTF-8 ENCODE\n" \
            "    16          TAG BLOCK BREAKOUT\n" \
            "    17          SCRIPT BREAKOUT\n" \
            "    18          FILE UPLOAD PAYLOAD\n" \
            "    19          INSIDE COMMENTS BYPASS\n" \
            "    20          MUTATION PAYLOAD\n" \
            "    21          MALFORMED IMG\n" \
            "    22          SPACE BYPASS\n" \
            "    23          DOWNLEVEL-HIDDEN BLOCK\n" \
            "    24          TRY ALL"

    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-u", dest="url", 
                      help="  Target site to scan. Usage: -u <url>")
    parser.add_option("-l", dest="list",
                      help="  List of target sites. Usage: -l <list>")    
    parser.add_option("-t", dest="type", 
                      help="  Type of payload. Usage: -t <type>")
    parser.add_option("-p", dest="payload",
                      help="  Choose payload. Usage: -p <payload_code>[,<payload_code>]",)
    parser.add_option("-f", dest="fuzz",
                      help="  For basic fuzzing use argument 'basic'. For custom fuzzing specify wordlist.")

    (options, arguments) = parser.parse_args()

    if options.list and options.url:
        parser.error("[+] Specify either target website(1) or list of websites, not both of them")
    if not options.list and not options.url:
        parser.error("[+] Please specify a target website")
    if options.url:
        targets.append(options.url)
    if options.list:
        file = open(options.list, "r")
        for i in file.readlines():
            targets.append(i[:-1])
    
    if not options.type and not options.payload:
        fuzzing = "basic"
    else:
        if options.type in payload_module.types.keys():
            type = options.type
        else:
            parser.error("Specify a type of payload")


        #payload
        payloads = options.payload.split(",")
        if "24" in payloads:
            payload_codes = [i for i in range(24)]
        else:    
            payload_codes = [int(payload) for payload in payloads if -1<int(payload)<25]



    #fuzzing
    if options.fuzz:
        fuzzing = options.fuzz


    return [type, payload_codes, fuzzing, targets]


