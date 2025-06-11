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
                            productId
                            quantityUsed
                            usageDate
                            issuedToService
                            relatedId
                            notes
                            createdAt
                            updatedAt
                            status
                            approvedBy
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
    def create_stock_out(product_id, quantity_used, usage_date, issued_to_service, approved_by, related_id=None, notes=None):
        try:
            response = requests.post(
                f"{Config.STOCK_OUT_SERVICE_URL}/graphql",
                json={
                    "query": """
                    mutation ($productId: Int!, $quantityUsed: Int!, $usageDate: String!, $issuedToService: String!, $approvedBy: String!, $relatedId: String, $notes: String) {
                        createStockOut(
                            productId: $productId
                            quantityUsed: $quantityUsed
                            usageDate: $usageDate
                            issuedToService: $issuedToService
                            approvedBy: $approvedBy
                            relatedId: $relatedId
                            notes: $notes
                        ) {
                            stockOut {
                                id
                                productId
                                quantityUsed
                                usageDate
                                issuedToService
                                relatedId
                                notes
                                createdAt
                                status
                                approvedBy
                            }
                            message
                        }
                    }
                    """,
                    "variables": {
                        "productId": product_id,
                        "quantityUsed": quantity_used,
                        "usageDate": usage_date,
                        "issuedToService": issued_to_service,
                        "approvedBy": approved_by,
                        "relatedId": related_id,
                        "notes": notes
                    }
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating stock out: {e}")
            return None

    @staticmethod
    def get_stock_out_by_id(id):
        try:
            response = requests.post(
                f"{Config.STOCK_OUT_SERVICE_URL}/graphql",
                json={
                    "query": """
                    query ($id: Int!) {
                        stockOut(id: $id) {
                            id
                            productId
                            quantityUsed
                            usageDate
                            issuedToService
                            relatedId
                            notes
                            createdAt
                            updatedAt
                            status
                            approvedBy
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
            print(f"Error fetching stock out: {e}")
            return None

    @staticmethod
    def get_stock_outs_by_filter(product_id=None, issued_to_service=None, start_date=None, end_date=None, status=None):
        try:
            variables = {
                "productId": product_id,
                "issuedToService": issued_to_service,
                "startDate": start_date,
                "endDate": end_date,
                "status": status
            }
            # Remove None values
            variables = {k: v for k, v in variables.items() if v is not None}

            response = requests.post(
                f"{Config.STOCK_OUT_SERVICE_URL}/graphql",
                json={
                    "query": """
                    query ($productId: Int, $issuedToService: String, $startDate: String, $endDate: String, $status: String) {
                        stockOuts(
                            productId: $productId
                            issuedToService: $issuedToService
                            startDate: $startDate
                            endDate: $endDate
                            status: $status
                        ) {
                            id
                            productId
                            quantityUsed
                            usageDate
                            issuedToService
                            relatedId
                            notes
                            createdAt
                            updatedAt
                            status
                            approvedBy
                        }
                    }
                    """,
                    "variables": variables
                }
            )
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching filtered stock outs: {e}")
            return None 