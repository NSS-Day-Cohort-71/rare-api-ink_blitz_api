import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import create_user, login_user, get_all_users, retrieve_user
from views import create_category, list_categories
from views import create_post, retrieve_post, update_post, list_posts, delete_post
from views import create_tag, list_tags, retrieve_tag, update_tag, delete_tags
from views import create_comment, list_comments


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
                return self.response(
                    json.dumps(category_response), status.HTTP_201_SUCCESS_CREATED.value
                )

        elif url["requested_resource"] == "tags":
            tag_response = create_tag(request_body)

            if tag_response:
                return self.response(
                    json.dumps(tag_response), status.HTTP_201_SUCCESS_CREATED.value
                )
        elif url["requested_resource"] == "comments":
            comment_response = create_comment(request_body)

            if comment_response:
                return self.response(
                    json.dumps(comment_response), status.HTTP_201_SUCCESS_CREATED.value
                )

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            # Handle single post retrieval by primary key
            if url["pk"] != 0:
                response_body = retrieve_post(url["pk"])

                if response_body:  # Check if the post exists
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response(
                        "Post not found",
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )

            # Handle listing all posts
            response_body = list_posts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "users":
            if url["pk"] != 0:
                response_body = retrieve_user(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                response_body = get_all_users()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "tags":
            if url["pk"] != 0:
                response_body = retrieve_tag(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            else:
                response_body = list_tags()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "categories":
            response_body = list_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "comments":
            response_body = list_comments()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_PUT(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "posts":
            if pk != 0:
                successfully_updated = update_post(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
        elif url["requested_resource"] == "tags":
            if pk != 0:
                successfully_updated = update_tag(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_DELETE(self):
        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "posts":
            if pk != 0:
                successfully_deleted = delete_post(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
        elif url["requested_resource"] == "tags":
            if pk != 0:
                successfully_deleted = delete_tags(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )
        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
