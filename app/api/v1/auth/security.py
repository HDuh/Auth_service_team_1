from flask_restful import Resource, reqparse


class ChangePassword(Resource):
    def post(self):
        """
        Change password method for users
        ---
        tags:
          - user
        parameters:
          - in: body
            name: body
            schema:
              id: ChangePassword
              required:
                - password
                - password_confirm
              properties:
                password:
                  type: string
                  description: The user's password.
                  default: "Qwerty123"
                password_confirm:
                  type: string
                  description: Password confirmation
                  default: "Qwerty123"
        responses:
          200:
            description: Message that user was created
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
                    default: ...
                  default: []
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
                errors:
                  type: array
                  description: Data with error validation messages
                  items:
                    type: object
                    default: ...
                  default: []
                message:
                  type: string
                  description: Response message
        """
        pass
