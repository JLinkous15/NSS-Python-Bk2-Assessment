import json
from views import *
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of HTTP requests to the server
    """

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != '':
            query_params = url_components.query.split("&")

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id, query_params)

    def do_GET(self):
        """Handles GET requests to the server
        """
        parsed = self.parse_url(self.path)
        ( resource, id, query_params ) = parsed

        
        if '?' not in self.path:
            if resource == 'species':
                if id is not None:
                    response =get_single_species(id)
                else:
                    response=get_all_species()
            elif resource == 'snakes':
                if id is not None:
                    response =get_single_snake(id)
                else:
                    response=get_all_snakes(query_params)
            elif resource == 'owners':
                if id is not None:
                    response =get_single_owner(id)
                else:
                    response=get_all_owners()
            else:
                response = {"Message":"Not Supported"}
        else:
            if resource == 'snakes':
                if id is not None:
                    response =get_single_snake(id)
                else:
                    response=get_all_snakes(query_params)

        #Setting the appropriate header
        if "message" in response:
            if response["message"] == "Bad Request":
                self._set_headers(400)
            elif response["message"] == "Not Supported":
                self._set_headers(404)
            elif response["message"] == "Not Allowed":
                self._set_headers(405)
        else:
            self._set_headers(200)

        # Send a JSON formatted string as a response
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Posts snakes to server, but only with all necessary information"""

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)
        
        # Parse the URL
        parsed = self.parse_url(self.path)
        ( resource, id, query_params ) = parsed

        # Initialize new snake
        new_post = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "snakes":
            
            if "gender" not in post_body:
                print("needs gender")
                new_post = {"message":"Bad request. Please provide a gender."}
            elif "name" not in post_body:
                print("needs name")
                new_post = {"message":"Bad request. Please provide a name."}
            elif "color" not in post_body:
                print("needs color")
                new_post = {"message":"Bad request. Please provide a color."}
            elif "owner_id" not in post_body:
                print("needs owner_id")
                new_post = {"message":"Bad request. Please provide a owner_id."}
            elif "species" not in post_body:
                print("needs species_id")
                new_post = {"message":"Bad request. Please provide a species_id."}
            else:
                post_body["species_id"] = post_body.pop("species")
                new_post = create_snake(post_body)

        if "message" in post_body:
            self._set_headers(400)
        else:
            self._set_headers(201)

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_post).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handles PUT requests to the server"""
        self.do_PUT()

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
