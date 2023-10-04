import http.server
import socketserver
import json
import re


with open("products.json", "r") as products_file:
    products = json.load(products_file)


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path

        if path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Home Page</h1> <h2>This is our home pageeee!!!</h2></body></html>")
            
        elif path == '/about':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>About Us Info</h1><p>Lorem ipsum lol</p></body></html>")
            
        elif path == '/contacts':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Contact Us</h1><p>here's our info </p></body></html>")
        
        elif path == '/product' or path == '/product/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = "<html><body><h1>Products</h1><ul>"

            for i in range(len(products)):
                response += f"<li><a href='/product/{i+1}'>{products[i]['name']}</a></li>"

            response += "</ul></body></html>"
            self.wfile.write(response.encode())
        
        elif re.match(r'^/product/\d+$', path):
            product_id = int(path.split("/")[-1])
            if 1 <= product_id <= len(products):
                product = products[product_id - 1]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                product_html = f"""
                    <html>
                    <body>
                        <h1>{product['name']}</h1>
                        <p>Author: {product['author']}</p>
                        <p>Price: ${product['price']}</p>
                        <p>Description: {product['description']}</p>
                    </body>
                    </html>
                """
                self.wfile.write(product_html.encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")
        
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 not found</h1></body></html>")


PORT = 8081
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
