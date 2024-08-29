import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import create_user, login_user
from views import create_category
from views import create_post, retrieve_post, update_post


class JSONServer(HandleRequests):
    def do_POST(self):
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "register":
            # Capture the entire dictionary returned by create_user
            user_response = create_user(request_body)

            if user_response:
                # Return the response with the valid key and token
                return self.response(
                    json.dumps(user_response), status.HTTP_201_SUCCESS_CREATED.value
                )
            # else:
            #     # Handle case where user creation fails
            #     return self.response(
            #         json.dumps({"valid": False}),
            #         status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
            #     )

        elif url["requested_resource"] == "login":
            user_response = login_user(request_body)

            if user_response:
                return self.response(user_response, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "posts":
            post_response = create_post(request_body)

            if post_response:
                return self.response(
                    json.dumps(post_response), status.HTTP_201_SUCCESS_CREATED.value
                )
        
        elif url["requested_resource"] == "categories":
            category_response = create_category(request_body)

            if category_response:
                return self.response(json.dumps(category_response), status.HTTP_201_SUCCESS_CREATED.value)

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_GET(self):

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = retrieve_post(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )
    def do_PUT(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "posts":
            if pk != 0:
                successfully_updated = update_post(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
