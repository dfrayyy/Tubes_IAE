import requests
from config import Config

class InventoryService:
    @staticmethod
    def get_products():
        try:
            response = requests.post(
                f"{Config.INVENTORY_SERVICE_URL}/graphql",
                json={
                    "query": """
                    query {
                        products {
                            id
                            name
                            description
                            quantity
                            unitPrice
                            category {
                                name
                                id
                            }
                            supplier {
                                name
                                id
                            }
                        }
                    }
                    """
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching products: {e}")
            return None

    @staticmethod
    def create_product(name, description, category_id, supplier_id, quantity=0, unit_price=None):
        try:
            response = requests.post(
                f"{Config.INVENTORY_SERVICE_URL}/graphql",
                json={
                    "query": """
                    mutation ($name: String!, $description: String, $categoryId: Int!, $supplierId: Int!, $quantity: Int, $unitPrice: Float) {
                        createProduct(
                            name: $name
                            description: $description
                            categoryId: $categoryId
                            supplierId: $supplierId
                            quantity: $quantity
                            unitPrice: $unitPrice
                        ) {
                            product {
                                id
                                name
                                description
                                quantity
                                unitPrice
                                category {
                                    name
                                }
                                supplier {
                                    name
                                }
                            }
                        }
                    }
                    """,
                    "variables": {
                        "name": name,
                        "description": description,
                        "categoryId": category_id,
                        "supplierId": supplier_id,
                        "quantity": quantity,
                        "unitPrice": unit_price
                    }
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating product: {e}")
            return None

    @staticmethod
    def update_product(id, name=None, description=None, category_id=None, supplier_id=None, quantity=None, unit_price=None):
        variables = {
            "id": id,
            "name": name,
            "description": description,
            "categoryId": category_id,
            "supplierId": supplier_id,
            "quantity": quantity,
            "unitPrice": unit_price
        }
        # Remove None values
        variables = {k: v for k, v in variables.items() if v is not None}
        
        try:
            response = requests.post(
                f"{Config.INVENTORY_SERVICE_URL}/graphql",
                json={
                    "query": """
                    mutation ($id: Int!, $name: String, $description: String, $categoryId: Int, $supplierId: Int, $quantity: Int, $unitPrice: Float) {
                        updateProduct(
                            id: $id
                            name: $name
                            description: $description
                            categoryId: $categoryId
                            supplierId: $supplierId
                            quantity: $quantity
                            unitPrice: $unitPrice
                        ) {
                            product {
                                id
                                name
                                description
                                quantity
                                unitPrice
                                category {
                                    name
                                }
                                supplier {
                                    name
                                }
                            }
                        }
                    }
                    """,
                    "variables": variables
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error updating product: {e}")
            return None

    @staticmethod
    def delete_product(id):
        try:
            response = requests.post(
                f"{Config.INVENTORY_SERVICE_URL}/graphql",
                json={
                    "query": """
                    mutation ($id: Int!) {
                        deleteProduct(id: $id) {
                            success
                            message
                        }
                    }
                    """,
                    "variables": {
                        "id": id
                    }
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error deleting product: {e}")
            return None

    @staticmethod
    def get_categories():
        try:
            response = requests.post(
                f"{Config.INVENTORY_SERVICE_URL}/graphql",
                json={
                    "query": """
                    query {
                        categories {
                            id
                            name
                            description
                        }
                    }
                    """
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching categories: {e}")
            return None

    @staticmethod
    def get_suppliers():
        try:
            response = requests.post(
                f"{Config.INVENTORY_SERVICE_URL}/graphql",
                json={
                    "query": """
                    query {
                        suppliers {
                            id
                            name
                            contactInfo
                            address
                        }
                    }
                    """
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching suppliers: {e}")
            return None

class StockInService:
    @staticmethod
    def get_stock_ins():
        try:
            response = requests.post(
                f"{Config.STOCK_IN_SERVICE_URL}/graphql",
                json={
                    "query": """
                    query {
                        stockIns {
                            id
                            product {
                                name
                            }
                            quantity
                            date
                            unitPrice
                        }
                    }
                    """
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching stock ins: {e}")
            return None

    @staticmethod
    def create_stock_in(product_id, quantity, date, unit_price=None):
        try:
            response = requests.post(
                f"{Config.STOCK_IN_SERVICE_URL}/graphql",
                json={
                    "query": """
                    mutation ($productId: Int!, $quantity: Int!, $date: Date!, $unitPrice: Float) {
                        createStockIn(
                            productId: $productId
                            quantity: $quantity
                            date: $date
                            unitPrice: $unitPrice
                        ) {
                            stockIn {
                                id
                                product {
                                    name
                                }
                                quantity
                                date
                                unitPrice
                            }
                        }
                    }
                    """,
                    "variables": {
                        "productId": product_id,
                        "quantity": quantity,
                        "date": date,
                        "unitPrice": unit_price
                    }
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating stock in: {e}")
            return None

class StockOutService:
    @staticmethod
    def get_stock_outs():
        try:
            response = requests.post(
                f"{Config.STOCK_OUT_SERVICE_URL}/graphql",
                json={
                    "query": """
                    query {
                        stockOuts {
                            id
                            product {
                                name
                            }
                            quantityUsed
                            usageDate
                            issuedToService
                            relatedId
                        }
                    }
                    """
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching stock outs: {e}")
            return None

    @staticmethod
    def create_stock_out(product_id, quantity_used, usage_date, issued_to_service=None, related_id=None):
        try:
            response = requests.post(
                f"{Config.STOCK_OUT_SERVICE_URL}/graphql",
                json={
                    "query": """
                    mutation ($productId: Int!, $quantityUsed: Int!, $usageDate: Date!, $issuedToService: String, $relatedId: String) {
                        createStockOut(
                            productId: $productId
                            quantityUsed: $quantityUsed
                            usageDate: $usageDate
                            issuedToService: $issuedToService
                            relatedId: $relatedId
                        ) {
                            stockOut {
                                id
                                product {
                                    name
                                }
                                quantityUsed
                                usageDate
                                issuedToService
                                relatedId
                            }
                        }
                    }
                    """,
                    "variables": {
                        "productId": product_id,
                        "quantityUsed": quantity_used,
                        "usageDate": usage_date,
                        "issuedToService": issued_to_service,
                        "relatedId": related_id
                    }
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating stock out: {e}")
            return None 