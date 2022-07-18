from flask_restful import Resource, reqparse


class UserLogin(Resource):
    def post(self):
        """
        Login
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - username
                - password
              properties:
                username:
                  type: string
                  description: The user's username.
                  default: "Beast"
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
        responses:
          200:
            description: Success user's login
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: True
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                    properties:
                      access_token:
                        type: string
                      refresh_token:
                        type: string
                message:
                  type: string
                  description: Response message
          400:
            description: Bad request response
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
        """
        pass


class UserLogout(Resource):
    def post(self):
        """
        Logout
        ---
        tags:
          - user
        responses:
          200:
            description: Success user's logout
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: True
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                message:
                  type: string
                  description: Response message
          401:
            description: Authorization error response
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                errors:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                description:
                  type: string
                  description: Response description
                message:
                  type: string
                  description: Response message
        """
        pass


class UserLogoutRefresh(Resource):
    def post(self):
        """
        Logout refresh token method for users
        ---
        tags:
          - user
        responses:
          200:
            description: Success user's logout refresh token
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: True
                data:
                  type: array
                  description: Response data
                  items:
                    type: object
                message:
                  type: string
                  description: Response message
          401:
            description: Authorization error response
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                errors:
                  type: array
                  description: Response data
                  items:
                    type: object
                    default: ...
                  default: []
                description:
                  type: string
                  description: Response description
                message:
                  type: string
                  description: Response message
        """
        pass
