# Inventory Service

A Flask-based GraphQL service for managing inventory items.

## Features

- GraphQL API for inventory management
- PostgreSQL database for data persistence
- Docker containerization
- CRUD operations for inventory items

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository
2. Navigate to the Inventory-service directory
3. Run the following command to start the services:

```bash
docker-compose up --build
```

The service will be available at:
- GraphQL endpoint: http://localhost:5000/graphql
- GraphiQL interface: http://localhost:5000/graphql

## GraphQL Operations

### Query Examples

1. Get all inventory items:
```graphql
query {
  inventoryItems {
    id
    name
    description
    quantity
    unitPrice
    sku
    createdAt
    updatedAt
  }
}
```

2. Get a specific inventory item:
```graphql
query {
  inventoryItem(id: 1) {
    name
    quantity
    unitPrice
  }
}
```

### Mutation Examples

1. Create a new inventory item:
```graphql
mutation {
  createInventoryItem(
    name: "Example Item"
    description: "This is an example item"
    quantity: 100
    unitPrice: 29.99
    sku: "EX-001"
  ) {
    inventoryItem {
      id
      name
      quantity
    }
  }
}
```

2. Update an inventory item:
```graphql
mutation {
  updateInventoryItem(
    id: 1
    quantity: 150
    unitPrice: 34.99
  ) {
    inventoryItem {
      id
      name
      quantity
      unitPrice
    }
  }
}
```

## Project Structure

```
Inventory-service/
├── app.py              # Main application file
├── database.py         # Database configuration
├── models.py           # SQLAlchemy models
├── schema.py           # GraphQL schema
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
└── docker-compose.yml # Docker Compose configuration
``` 