# Sistem Manajemen Inventory

Sistem manajemen inventory yang dibangun menggunakan microservices architecture dengan Flask, GraphQL, dan PostgreSQL.

## Arsitektur Sistem

Sistem terdiri dari 3 microservices:
1. **Inventory Service** - Manajemen produk, kategori, dan supplier
2. **Stock In Service** - Manajemen stok masuk dan pembelian
3. **Stock Out Service** - Manajemen stok keluar dan penggunaan

## Teknologi yang Digunakan

- **Backend**: Python Flask
- **API**: GraphQL
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Package Manager**: pip

## Prasyarat

Sebelum instalasi, pastikan sistem Anda memiliki:
1. Python 3.9 atau lebih baru
2. Docker dan Docker Compose
3. Git

## Cara Instalasi

1. Clone repository ini:
bash
git clone https://github.com/[username]/Sistem-manajemen-inventory.git
cd Sistem-manajemen-inventory


2. Build dan jalankan dengan Docker:
bash
docker-compose up --build


Atau jika ingin menjalankan secara lokal (development):

1. Buat virtual environment:
bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate


2. Install dependencies:
bash
pip install -r requirements.txt


3. Jalankan masing-masing service:
bash
# Terminal 1 - Inventory Service
cd Inventory-service
python app.py

# Terminal 2 - Stock In Service
cd Stock in-service
python app.py

# Terminal 3 - Stock Out Service
cd Stock Out-service
python app.py


## Endpoints
Setelah service berjalan, Anda dapat mengakses:
- Inventory Service: http://localhost:5000/graphql
- Stock In Service: http://localhost:5001/graphql
- Stock Out Service: http://localhost:5002/graphql

## Contoh Penggunaan GraphQL
### 1. Manajemen Kategori

graphql
# Membuat kategori baru
mutation {
  createCategory(
    name: "Electronics",
    description: "Electronic components and devices"
  ) {
    category {
      id
      name
    }
  }
}

# Query semua kategori
query {
  categories {
    id
    name
    description
  }
}


### 2. Manajemen Supplier

graphql
# Membuat supplier baru
mutation {
  createSupplier(
    name: "PT Elektronik Jaya",
    contactInfo: "sales@elektronikjaya.com",
    address: "Jl. Elektronik No. 123"
  ) {
    supplier {
      id
      name
    }
  }
}

# Query supplier dengan pagination
query {
  suppliers(
    pagination: {
      page: 1,
      perPage: 10
    }
  ) {
    id
    name
    contactInfo
  }
}


### 3. Manajemen Produk

graphql
# Membuat produk baru
mutation {
  createProduct(
    name: "Laptop Gaming",
    description: "High-end gaming laptop",
    categoryId: 1,
    supplierId: 1,
    quantity: 10,
    unitPrice: 15000000
  ) {
    product {
      id
      name
      quantity
    }
  }
}

# Query produk dengan filter
query {
  products(
    filter: {
      categoryId: 1,
      minPrice: 1000000,
      maxPrice: 20000000
    }
  ) {
    id
    name
    unitPrice
    quantity
  }
}


### 4. Manajemen Stok

graphql
# Record stok masuk
mutation {
  createStockIn(
    productId: 1,
    quantity: 5,
    date: "2024-01-23",
    unitPrice: 14500000
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

# Record stok keluar
mutation {
  createStockOut(
    productId: 1,
    quantityUsed: 2,
    usageDate: "2024-01-24",
    issuedToService: "Sales"
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


## Fitur-fitur

1. **Inventory Service**:
   - Manajemen kategori produk
   - Manajemen supplier
   - Manajemen produk
   - Tracking stok real-time
   - Filter dan pencarian produk
   - Pagination dan sorting

2. **Stock In Service**:
   - Record stok masuk
   - Update stok otomatis
   - Tracking harga pembelian
   - History pembelian

3. **Stock Out Service**:
   - Record stok keluar
   - Validasi stok tersedia
   - Tracking penggunaan
   - History penggunaan


## Struktur Direktori

Sistem-manajemen-inventory/
├── Inventory-service/
│   ├── app.py
│   ├── models.py
│   ├── schema.py
│   └── requirements.txt
├── Stock in-service/
│   ├── app.py
│   ├── models.py
│   ├── schema.py
│   └── requirements.txt
├── Stock Out-service/
│   ├── app.py
│   ├── models.py
│   ├── schema.py
│   └── requirements.txt
├── docker-compose.yml
├── requirements.txt
└── README.md
