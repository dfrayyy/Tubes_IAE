# Stock In Service

A Flask-based GraphQL service for managing stock incoming transactions.

## Features

- GraphQL API for managing stock incoming transactions
- Integration with main inventory database
- Stock quantity tracking
- Transaction history

## API Endpoints

The service is available at:
- GraphQL endpoint: http://localhost:5001/graphql
- GraphiQL interface: http://localhost:5001/graphql

## GraphQL Operations

### Query Examples

1. Get all stock in transactions:
```graphql
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
```

2. Get specific stock in transaction:
```graphql
query {
  stockIn(id: 1) {
    product {
      name
      quantity
    }
    quantity
    date
    unitPrice
  }
}
```

### Mutation Examples

1. Create stock in transaction:
```graphql
mutation {
  createStockIn(
    productId: 1
    quantity: 50
    date: "2024-01-20"
    unitPrice: 195.99
  ) {
    stockIn {
      id
      quantity
      product {
        name
        quantity
      }
    }
  }
}
``` 