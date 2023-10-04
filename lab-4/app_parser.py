import socket
import re
import os


server_address = ('localhost', 8081)
simple_pages_folder = 'simple_pages'
os.makedirs(simple_pages_folder, exist_ok=True)


def make_request(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)
        request = f"GET {path} HTTP/1.1\r\nHost: {server_address[0]}\r\n\r\n"
        client_socket.sendall(request.encode())
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data
    return response.decode("utf-8")


def extract_html_content(response):
    header_end = response.find('\r\n\r\n') + 4
    html_content = response[header_end:]
    return html_content


def extract_product_details(html):
    product_details = {}
    match = re.search(r"<h1>(.*?)</h1>", html)
    if match:
        product_details["name"] = match.group(1)
    match = re.search(r"Author: (.*?)</p>", html)
    if match:
        product_details["author"] = match.group(1)
    match = re.search(r"Price: \$(.*?)</p>", html)
    if match:
        product_details["price"] = float(match.group(1))
    match = re.search(r"Description: (.*?)</p>", html)
    if match:
        product_details["description"] = match.group(1)
    return product_details


product_listing_response = make_request("/product")
product_routes = re.findall(r'href=\'(/product/\d+)\'', product_listing_response)
product_details_dict = {}

for product_route in product_routes:
    product_response = make_request(product_route)
    product_details = extract_product_details(product_response)
    product_details_dict[product_route] = product_details

for route, details in product_details_dict.items():
    print(f"Product Route: {route}")
    print(details)
    print("\n")

for path in ('/', '/about', '/contacts'):
    page_content = make_request(path)
    if path == '/':
        filename = os.path.join(simple_pages_folder, 'main.html')
    else:
        filename = os.path.join(simple_pages_folder, path.lstrip('/').replace('/', '_') + '.html')
    
    with open(filename, 'w', encoding='utf-8') as file:
        html_content = extract_html_content(page_content)
        file.write(html_content)
        print(f"Saved {path} content to {filename}")
