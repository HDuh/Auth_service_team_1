from flask_restful import Resource, reqparse


class Profile(Resource):
    def get(self):
        """
        Get own profile method for users
        ---
        tags:
          - profile
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
                      id:
                        type: string
                      username:
                        type: string
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

    def patch(self):
        """
        Update profile method for users
        ---
        tags:
          - profile
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - username
              properties:
                username:
                  type: string
                  description: The user's username.
                  default: "Beast"
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
                      id:
                        type: string
                      username:
                        type: string
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

    def delete(self):
        """
        Delete profile method for users
        ---
        tags:
          - profile
        responses:
          200:
            description: Successfully deletion user
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: True
                message:
                  type: string
                  description: Response message
          400:
            description: Unsuccessfully deletion user
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                message:
                  type: string
                  description: Response message
        """
        pass


class GetHistory(Resource):
    def get(self):
        """
        Return list of user's login history
        ---
        tags:
          - profile
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
                    type: string
        """
        pass
