login_request_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "username": {
      "type": "string"
    },
    "password": {
      "type": "string"
    }
  },
  "required": [
    "username",
    "password"
  ]
}

login_response_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "message": {
            "type": "string"
        },
        "token": {
            "type": "string"
        }
    },
    "required": [
        "message",
        "token"
    ]
}
