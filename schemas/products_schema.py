products_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "product_id": {
                "type": "number"
            },
            "name": {
                "type": "string"
            },
            "description": {
                "type": "string"
            },
            "price": {
                "type": "string"
            },
            "category": {
                "type": "string"
            },
            "manufacturer": {
                "type": "string"
            },
            "imageUrl": {
                "type": "string"
            },
            "freeShipping": {
                "type": "number"
            }
        },
        "required": [
            "product_id",
            "name",
            "description",
            "price",
            "category",
            "manufacturer",
            "imageUrl",
            "freeShipping"
        ]
    }
}
