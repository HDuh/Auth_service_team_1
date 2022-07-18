from flask_restful import Resource


class CreateRole(Resource):
    def post(self):
        """
        Create new role
        ---
        tags:
          - role
        parameters:
          - in: body
            name: body
            schema:
              id: Roles
              required:
                - name
                - permissions
              properties:
                name:
                  type: string
                  description: The role's name.
                  default: "super_admin"
                permissions:
                  type: array
                  description: Roles permissions.
                  default: []
        responses:
          200:
            description: The Role data
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
                          default: a1c0eaa1-6255-40cc-83fc-1e33ed14f4c3
                        name:
                          type: string
                          default: user
                        permissions:
                          type: array
                          default: []
                  default: []
          400:
            description: Bad request, already existed role name
            schema:
              properties:
                success:
                  type: boolean
                  description: Response status
                  default: False
                errors:
                  type: array
                  description: Data with error validation messages
                  items:
                    type: object
                    default: ...
                  default: []
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


class Role(Resource):
    def get(self, role_id):
        """
        Return detail of specific role by role_id
        ---
        tags:
          - role
        parameters:
          - in: path
            name: role_id
            required: true
            description: The ID of user's role
            type: string
        responses:
          200:
            description: The Role data
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
                          default: a1c0eaa1-6255-40cc-83fc-1e33ed14f4c3
                        name:
                          type: string
                          default: user
                  default: []
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
                  description: Data with error validation messages
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

    def patch(self, role_id):
        """
        Update data of specific role by role_id
        ---
        tags:
          - role
        parameters:
          - in: path
            name: role_id
            required: true
            description: The ID of user's role
            type: string
        parameters:
          - in: body
            name: body
            schema:
              id: Role
              required:
                - name
              properties:
                name:
                  type: string
                  description: The role's name.
                  default: "super_admin"
        responses:
          200:
            description: The Role data
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
                          default: a1c0eaa1-6255-40cc-83fc-1e33ed14f4c3
                        name:
                          type: string
                          default: user
                  default: []
          400:
            description: Bad request, already existed role name
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

    def delete(self, role_id: str):
        """
        Delete specific role by role_id
        ---
        tags:
          - role
        parameters:
          - in: path
            name: role_id
            required: true
            description: The ID of user's role
            type: string
        responses:
          202:
            description: The Role deleted
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
                  default: []
                message:
                  type: string
                  description: Response message
        """
        pass


class RoleList(Resource):
    def get(self) -> dict:
        """
        Return list of user's roles
        ---
        tags:
          - role
        responses:
          200:
            description: The Role data
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
                      roles:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: string
                              default: a1c0eaa1-6255-40cc-83fc-1e33ed14f4c3
                            name:
                              type: string
                              default: user
                            permissions:
                              type: array
                              default: []
                        default: []
                  default: []
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


class UserRole(Resource):
    def post(self):
        """
        Create user's role for specific user
        ---
        tags:
          - user_role
        parameters:
          - in: body
            name: body
            schema:
              id: UserRoles
              required:
                - user_id
                - role_id
              properties:
                user_id:
                  type: string
                  description: The user's id.
                  default: 28b28c98-926b-45aa-826c-5ea495ecbfa5
                role_id:
                  type: string
                  description: The role's id.
                  default: 6e14280c-48fe-4bf9-94c0-94083e9eec55
        responses:
          200:
            description: The User's role created
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
                  default: []
        """
        pass

    def delete(self):
        """
        Delete user's role for specific user
        ---
        tags:
          - user_role
        parameters:
          - in: body
            name: body
            schema:
              id: UserRoles
              required:
                - user_id
                - role_id
              properties:
                user_id:
                  type: string
                  description: The user's id.
                  default: 28b28c98-926b-45aa-826c-5ea495ecbfa5
                role_id:
                  type: string
                  description: The role's id.
                  default: 6e14280c-48fe-4bf9-94c0-94083e9eec55
        responses:
          200:
            description: The User's role deleted
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
                  default: []
          400:
            description: The User's role deleted
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
                  default: []
                message:
                  type: string
                  description: Response message
        """
        pass
