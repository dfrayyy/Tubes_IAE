# Stock Out Service

A Flask-based GraphQL service for managing stock outgoing transactions.

## Features

- GraphQL API for managing stock outgoing transactions
- Integration with main inventory database
- Stock usage tracking
- Service allocation tracking
- Transaction history

## API Endpoints

The service is available at:
- GraphQL endpoint: http://localhost:5002/graphql
- GraphiQL interface: http://localhost:5002/graphql

## GraphQL Operations

### Query Examples

1. Get all stock out transactions:
```graphql
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
```

2. Get specific stock out transaction:
```graphql
query {
  stockOut(id: 1) {
    product {
      name
      quantity
    }
    quantityUsed
    usageDate
    issuedToService
  }
}
```

### Mutation Examples

1. Create stock out transaction:
```graphql
mutation {
  createStockOut(
    productId: 1
    quantityUsed: 5
    usageDate: "2024-01-21"
    issuedToService: "Repair Service"
    relatedId: "REP-001"
  ) {
    stockOut {
      id
      quantityUsed
      product {
        name
        quantity
      }
    }
  }
}
``` 