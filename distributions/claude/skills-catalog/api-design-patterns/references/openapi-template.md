# Full OpenAPI Template

A complete OpenAPI 3.0 specification template with common patterns. Copy and adapt for new APIs.

## Complete Template

```yaml
openapi: 3.0.3
info:
  title: My Service API
  description: |
    RESTful API for managing resources.

    ## Authentication
    All endpoints require a Bearer token unless marked as public.

    ## Rate Limiting
    - Standard: 1000 requests/minute
    - Burst: 50 requests/second
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Local development

tags:
  - name: Users
    description: User management
  - name: Posts
    description: Blog post operations

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/PerPageParam'
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive, pending]
        - name: sort
          in: query
          schema:
            type: string
            default: -createdAt
      responses:
        '200':
          description: Paginated list of users
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResponse'
                  - type: object
                    properties:
                      data:
                        type: array
                        items:
                          $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create user
      operationId: createUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/ValidationError'
        '409':
          $ref: '#/components/responses/Conflict'

  /users/{userId}:
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid

    get:
      summary: Get user by ID
      operationId: getUser
      tags: [Users]
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      summary: Update user
      operationId: updateUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      summary: Delete user
      operationId: deleteUser
      tags: [Users]
      responses:
        '204':
          description: User deleted
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required: [id, email, name, createdAt]
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        status:
          type: string
          enum: [active, inactive, pending]
          default: pending
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true

    CreateUserRequest:
      type: object
      required: [email, name]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100

    UpdateUserRequest:
      type: object
      minProperties: 1
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        status:
          type: string
          enum: [active, inactive]

    UserResponse:
      type: object
      properties:
        data:
          $ref: '#/components/schemas/User'

    PaginatedResponse:
      type: object
      properties:
        meta:
          type: object
          properties:
            total:
              type: integer
            page:
              type: integer
            perPage:
              type: integer
        links:
          type: object
          properties:
            self:
              type: string
            next:
              type: string
              nullable: true
            prev:
              type: string
              nullable: true

    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              code:
                type: string
              message:
                type: string
        requestId:
          type: string

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1
    PerPageParam:
      name: perPage
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  responses:
    ValidationError:
      description: Request validation failed
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                $ref: '#/components/schemas/Error'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                $ref: '#/components/schemas/Error'
    Conflict:
      description: Resource conflict
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                $ref: '#/components/schemas/Error'

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

## Tips

- Use `$ref` extensively to avoid duplication
- Put shared parameters in `components/parameters`
- Define reusable error responses in `components/responses`
- Use `readOnly` for server-generated fields (id, timestamps)
- Use `required` arrays to enforce mandatory fields
- Validate your spec with `npx @redocly/cli lint openapi.yaml`
