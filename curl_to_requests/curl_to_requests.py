import json
import re
import subprocess
import urllib.parse as parse

def curl_to_requests(curl_request: str) -> str:
    curl_list = re.split(r"[\b\s]\-H[\b\s]", curl_request)

    # Handle curl 'url'
    url_re = re.compile(r"curl \".+\"")
    url = curl_list.pop(0)
    url = url_re.search(url).group(0)
    url = url.replace("curl", "url =")
    url = url.strip()

    # Handle headers
    headers = []
    for header in curl_list:
        header = header.replace("^", "")
        header = header.replace(": ", "\": \"")
        header = "    " + header.strip()
        headers.append(header)

    # Parse the data
    if re.search('--data-raw', headers[-1]):
        headers[-1], data = headers[-1].split('--data-raw')
        headers[-1] = "    " + headers[-1].strip()

        data = parse.parse_qs(data)
        data = json.dumps(data)
        data = re.sub(r"^{", "{\n    ", data)
        data = re.sub(r"}$", "\n}", data)
        data = re.sub(r",\s(?=\")", ",\n    ", data)
        data = "data = " + data

    headers = ',\n'.join(headers)
    headers = "headers = {\n" + headers + "\n}"
    
    if not data:
        requests_string = headers + "\n" + url
    else:
        requests_string = headers + "\n" + data + "\n" + url
    subprocess.run(["clip"], input=requests_string.encode('utf-8'), shell=True)


if __name__ == "__main__":
    # curl_to_requests(
    #     'curl "https://flask.palletsprojects.com/en/3.0.x/tutorial/views/" --compressed -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8" -H "Accept-Language: en-US,en;q=0.5" -H "Accept-Encoding: gzip, deflate, br, zstd" -H "Referer: https://flask.palletsprojects.com/en/3.0.x/tutorial/database/" -H "Alt-Used: flask.palletsprojects.com" -H "Connection: keep-alive" -H "Cookie: _cfuvid=aBIhpjq2yekzT095BorbA2W74Mx4jcd0iCDBOk0nU4I-1729043066861-0.0.1.1-604800000" -H "Upgrade-Insecure-Requests: 1" -H "Sec-Fetch-Dest: document" -H "Sec-Fetch-Mode: navigate" -H "Sec-Fetch-Site: same-origin" -H "Sec-Fetch-User: ?1" -H "Priority: u=0, i"'
    # )
    curl_to_requests(
        'curl "https://access-web.dcf.state.fl.us/CPSLookup/search.aspx" -X POST -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8" -H "Accept-Language: en-US,en;q=0.5" -H "Accept-Encoding: gzip, deflate, br, zstd" -H "Content-Type: application/x-www-form-urlencoded" -H "Origin: https://access-web.dcf.state.fl.us" -H "Connection: keep-alive" -H "Referer: https://access-web.dcf.state.fl.us/CPSLookup/search.aspx" -H "Upgrade-Insecure-Requests: 1" -H "Sec-Fetch-Dest: document" -H "Sec-Fetch-Mode: navigate" -H "Sec-Fetch-Site: same-origin" -H "Sec-Fetch-User: ?1" -H "Priority: u=0, i" --data-raw "__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=ESM90pR^%^2Fv3LcX7m^%^2BAfInBDhPEXwRwRhtafUgms0iVVlkVaLhEsiives7kYcalaOIqCHTzrrqLF35vHHD4EsuriCbUNEOFRakpqbkKVdq4vLF^%^2BYGVDoi3zcUQhcPzAPavQCJx^%^2BJH^%^2FupNJJB6^%^2FolEsupU3cewDPUlZEYfvkH7U53uqeqMwVlYuTyjaE1Je7qJs04DG2ydJtdT15bxDLM3ChES2S1n^%^2FiYxV^%^2Bec^%^2FJpSrWaw0aPv8cZ0hmM9Jlg^%^2BgTpoA6OTgyEsBtP4EB88mpKP7y7eOe8jQyKI^%^2BmVUbuY14Va^%^2BATxEySDhwZGMLADt8qiGWTMGntMMqxxPpNMWXFC^%^2BcN3DydhM5A5X73DBMvSfqQ^%^2BB4AvcmHxsFP5894aXnheekl4fwG64^%^2BMjmkjsYdMKLcLzXqZDLzQ3cLZBVJwI4cIrG5cceM12CojuRBKvQkevdSMjr9iXe9oTOT2RHWIlVHUONNha5zZ7rEH3KX3IOTwfBSZZH73Q1uemFYlnACJaDFYTul0mOp6zZRBBi^%^2BEnonyecq3hJ^%^2BEDeD20fJVf7li^%^2BkvUFpihAC9BFuugqoN1Fc0slfWrVYhu34A2JlsAzHi14W9s9UowgUWJ79p1JI7fudjWfS24wRVv^%^2FIFEESFs^%^2BjimsyaHQIzk5gwmBGVFlBqFQmoVqL0FLrYip58^%^2BAOztYmpHXdLDw7a^%^2BwqZN4B7cKSGZKrWkWNgb7QyVbO^%^2Bi76lOhzx6Ew42e4uxSYvk2IA2mkXLjbEZr7OpDBe2DiYFy3U1wKXQDN9^%^2B2bfFeip5YkKFOLidCKQNKka8Pf^%^2F81rSCrHdfLF1Ya2X8NGx4zlJH8Dk7vRSFTdKpkcAXrnAWhkhLlPZc3aOtYvRaPZD0Pk9t8bdxVBWOlQEh^%^2B4YG7Rmt1FWVcyga1hknDihl67WmUngkdsV2T3XBrVsFbkg^%^2FWW^%^2FL0BkIEcIWjEAFMLlCcjDCgHbuwV2XKgCP0LBi^%^2F9ov9L4eWObqcp1DPuNTMULWhw0mmE^%^2BvZRCkUSbZhmQEaraQGr7qjmALN1NPtCtYxqOOJ4GARSesNmZx0OmXWkFWmc562EDJPnBdRkF^%^2FPIYv079Qs1Zxyz5GGJiTfIybENOuil9QVtk4^%^2Bg9w1hO1P^%^2Faaq9ms^%^2FMSemuuroTbtaAb1hgWJdp0BC5y^%^2Fjq3ldcWXVmFTFXCr4aTK4mVxx9^%^2FM7lSBMTgiGMSHp4cv4RRp3wNkJwVXwlIrEL1X1Q^%^2FkLg^%^2FQl76iy4vPOpyyVX^%^2FgMEFWjOezgBl4JxbvU4tQ3cYxp139Efqmh11f0LlX7Loavazd1eYwwQj8CFeARzRlaD4FEygRg3KTuMD2GH8qOUgvytPjqiMc3^%^2F1TJRXUzmhrAMqe7FxklU2TJmM4YwCYmjhPaDsE^%^2FJPKY9cIOvAtfRu^%^2FWnK^%^2BhNMgkEHQe^%^2FSvc3kyM11A7gjFuZNaRgKJvTIpWTxxq5Wc^%^2FT5Fe01mWjZvkqzhGdDJd29KSKdSBuP^%^2FhipGTe7y^%^2BJeCV8KS299p1LaElTPn7UKFI0JL7X5o^%^2FR6N00Z3JHizkQzLlracWKSJDOwm6Hiek9H3CTW^%^2FQpWRfqHS^%^2F5CMsgSiCMS^%^2BeEazzgd3^%^2B^%^2BYs9pRbQbC2nBbHn^%^2Bt2mtwHErOrllkychzUeN1x5KpcNeM6KzN8cAzi4QAsU2G^%^2FwcIVTk^%^2FC3AmFOdoRp8GlF12UHeDOoV^%^2FTrfQ9eEQ^%^2FCNHH1ICWjEzgPsKbv0u5^%^2FZitCQM1hg6wbXV4MKuce^%^2FSWUjuep^%^2BF^%^2BU^%^2B2sqOGpXfdwAyIcQZh403L0186Kx2VgWV6Fnnk7nKvEbazbifnA4PL1oahdXrfRKm92YkakdvDoS705oeamhw0vXs^%^2FCwROljYttrLGaqo1mZkex0G4vtLtnE91ht1gv^%^2B^%^2BnTKvU5eNHxSX8y8hot49he5EX9MYdxj1hXjIpWG5W^%^2FsBBy5FlJbkt5PNbJGC5q5CSpeH32gANJZneNCOLrDqdMdSXPqX2q0Rke2Qx8wsDfhL7Z53bhzqY7JHW85BHf70^%^2BWqksDbI1fKp74LQ8cu^%^2B^%^2FgXLUM5qYYDvnfDlAv^%^2FcnR3BdXWFhlD2BWMAkAAer6wVQQViPC8bCjFCnqBvdp7sNa2KgxRm7Q3hoH2lXY07RGmACBK50grXGGD4qq6IUXgpJluAKSPP1A^%^2FY9LByJCmU4bcYOOZvPbGDbQ^%^2Bx1KfYZFBR1DlNjmm^%^2FlYfGtLuHI^%^2FbTiAGjcbYW2HQKBDge8^%^2BH96K^%^2ByTbwz9JnWWJQNejMgEk8CRS0hkv^%^2BT5bhEnhtTKojD8aD7^%^2F2KXjkK3e5I1RcvXd0LSWaNYDevYBPpw6LDNJFAtaVG0OOHQgHz7DCqEsZf3kQZuQ695Fz7PueGCPtBg3AfoYQFzH^%^2Bi^%^2FpDgdrOC73ua5iYrJH9N3tdSaasJxEcP5mSblYDMgK^%^2BSqys6mQZdahtVgok6^%^2BAOqyuXpqO4LWDDYZK7p2E1uSbUeW5PLaQAZIPxk4SZg^%^3D^%^3D&__VIEWSTATEGENERATOR=B3291024&__VIEWSTATEENCRYPTED=&__PREVIOUSPAGE=mQ8fPkaebOIQ6s24OTKdwjIoEvfx3Z4XAoKil2TI5YXIVxHMn1d3JFSroI4kDxLuts2liiY3O5VKDKyv4aj8Xx1WMeSTGT1Vb0WbaNZWcE41&__EVENTVALIDATION=6lYlwbeEUdUePGu07iVHYGAseC8FsRG7gnt6KLaVMkPYHz61cAtvBsl^%^2FZUyi2V8OL3pB3DXHOa3b1OHdZXGCeO^%^2BwiPSL99oB04^%^2BVMjClA7JXX5tu^%^2BMhIRLSeROVL4qiftpXkVU^%^2B1wHCq1bn^%^2FlpsDQ2kTLiJdnjRIEi8SZkJQDnmzjOqcifgNRHW3w25h9z47CB6^%^2FzOUwtM61Cx0wI4L2XRR8sLtN7kr9Zh2Mz0wui^%^2FbaCgNULXEh7K60rX0vqSegrU8VDKl^%^2BX0RPbH0^%^2B^%^2BwnFnEsxnfLAjhRWjN^%^2FfcT^%^2BGqnQ45BOnyk^%^2FUzHns2CNG8wMdtYbpop8LzkhhN4lBMi8c5J1kniSG9GaJl4FaRGhBTxWfUxemRI81POUVWl3nM0l8F2EJX6yfEFaAlrwFyp5TxoWk3PASy2YXn7N2e5JBapn6cEWApXG4uXjjky1cHhWqMpoqWa0Lro^%^2BDwf5EYwk9avmOJkWhL49SqGn0bVbMqdW8gfT^%^2Bhmk^%^2FBWNXPfPfYOy7gQHkFspQh2uvrzSxYO^%^2Fm494xRxMl8srHR^%^2FGftZdbkxON7Tzw2d9r78k36HETx7xCSAfhe63E8TQfEDkMM0SoeES6oauD4^%^2B6VoAeqCgAcmoUtsZo8pWcZ8UfhqpQsmCS4WpVLItbtHE^%^2F3VYVoPYMFusbQUxd4lXHAPUMOGYXVac1bw7iELZeIOOEmCPisqygCjBLWfTDLdHNQsSzVn9mgJU4h6YMmPw1VSPYSuiTpqMDL3oK5tw3eK8gqRS^%^2B46BQZnxzKv^%^2FgRzDkPv5UG9g0frSjpkPzWwDNn9vbM7W^%^2FO1zP7j6RePzqVwFy4BHiRjUNMe6GRr4ZizVO6V4OZsF85tAmMIbvLLu^%^2Boot3O86aHuErjBqFCWuni6qwyTa7MQJ^%^2F96HBpKPvA9JXkb94FqsqchLjKBB3dqdMXwBzBEwQAPQxQzXhVwZZf2k^%^2BXPp3BHEGpBpnIpRuxezRbEYEc4^%^2B^%^2B2eGPfAhycMHr4Y4PR4ual^%^2FBQeZ0YTTXZeQCivBTWm3znC5ZwxX1jRhc8uJO5Fw^%^2Fbg9JFdesrmim0cnEHUwyu4xZWj4ZOZC^%^2F666T2kwJ4ssvSxSEoXrwJjBM^%^2BWXGXUF1MgdxbYkmU^%^2F7d4jjv9TWmMcP73uNipu88sCnGONPP9Wsr^%^2FUFhTyKioXPGwsRHSfLuWj18i4uREK59qjmQ814j6l2jL1GKHxAAIJFCjbUj1nXbTQPCvvu2vvS8HvBCM8yUaMwcwdAvopwahFOG0EmoV^%^2FsEMO^%^2BMKlYa2ggmwaBDZpTkmzL1zONfbr6C^%^2B6JOIvgeJWrrVwZqUqZf^%^2FQgCwePDHLHVTSVXLZG4btkM5g^%^2FMB10dt^%^2FdwopQMXWkadAZsoAn9XSI65zO1D^%^2FxK8VVQ9N6KKfDn5IWIiob3zNMifccyoyVTMzE2DvY4ty^%^2BHzzETYFjghCsafSirZ3ogdZ51w1oCWrpk^%^2BTmD8^%^2Fy7ogtStP7WF5ci15tzs9kT0j8J10KYBvr^%^2FROKr0T5SvEtNT9P2UQIGG^%^2BDOLpfyzXXlhkZdYot7Pw9lkNBcuh3c29ERwX^%^2FBioXVbUM1Bv0k0YtVNsvTX^%^2BNJhxLbXUmAJGm3kBeF2Gu4aWbuiBOLThMjvqFzo7UIxZmTbDklEJqs9XSv1lUDNff7hI1O^%^2FtsT6UzR0FtdvgIkOTO4fFdbVqPl5OrWZmZsjKX10Y0d9^%^2F7UFC7gx4CF4iwsR9tXU4lj0xsGY6Ps^%^2FFSCIkQ9UePTI7bgHG6JuS17jNOXmm2SvxG5U79O0e5fYSh6f5juTkqT7KEMB678xE2ceHH0p9I^%^2FFxYicyDfKkPXDO^%^2B629Fw^%^3D^%^3D&ctl00^%^24ContentPlaceHolder^%^24radSearch=1&ctl00^%^24ContentPlaceHolder^%^24drpCounty=01&ctl00^%^24ContentPlaceHolder^%^24btnSearch.x=47&ctl00^%^24ContentPlaceHolder^%^24btnSearch.y=15"'
    )