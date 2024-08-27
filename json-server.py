import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import create_user

class JSONServer(HandleRequests):
    def do_POST(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "register":
            new_user_id = successfully_created = create_user(request_body)
        
            return self.response(json.dumps({"id": new_user_id}), status.HTTP_201_SUCCESS_CREATED.value)
        
        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()