import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import StockIn as StockInModel
from database import db_session
from datetime import datetime
import requests

# GraphQL Type
class StockIn(SQLAlchemyObjectType):
    class Meta:
        model = StockInModel

# Fungsi bantu: Ambil data produk dari inventory-service
def get_product_info(product_id):
    try:
        response = requests.post(
            "http://inventory-service:5000/graphql",
            json={"query": f"""
                query {{
                    product(id: {product_id}) {{
                        id
                        quantity
                        name
                    }}
                }}
            """}
        )
        data = response.json()
        return data["data"]["product"]
    except Exception as e:
        print("Gagal mengambil data produk:", e)
        return None

# Mutation untuk mencatat stock in
class RecordStockIn(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
        date = graphene.String(required=True)
        unit_price = graphene.Float(required=True)

    stock_in = graphene.Field(lambda: StockIn)
    message = graphene.String()

    def mutate(self, info, product_id, quantity, date, unit_price):
        if quantity <= 0 or unit_price <= 0:
            raise Exception("Kuantitas dan harga harus lebih besar dari 0")

        product = get_product_info(product_id)
        if not product:
            raise Exception("Produk tidak ditemukan pada layanan inventory")

        stock_in = StockInModel(
            product_id=product_id,
            quantity=quantity,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            unit_price=unit_price
        )
        db_session.add(stock_in)
        db_session.commit()

        # Tambahkan stok di inventory-service
        try:
            updated_quantity = product["quantity"] + quantity
            requests.post(
                "http://inventory-service:5000/graphql",
                json={"query": f"""
                    mutation {{
                        updateProduct(id: {product_id}, quantity: {updated_quantity}) {{
                            product {{ id quantity }}
                        }}
                    }}
                """}
            )
            message = f"Stok produk berhasil ditambahkan. Stok baru: {updated_quantity}"
        except Exception as e:
            print("Gagal update stok di inventory-service:", e)
            message = "Transaksi dicatat, namun gagal update stok di inventory"

        return RecordStockIn(stock_in=stock_in, message=message)

# Query
class Query(graphene.ObjectType):
    stock_in = graphene.Field(StockIn, id=graphene.Int(required=True))
    stock_ins = graphene.List(
        StockIn,
        product_id=graphene.Int(),
        start_date=graphene.String(),
        end_date=graphene.String()
    )

    def resolve_stock_in(self, info, id):
        return StockInModel.query.get(id)

    def resolve_stock_ins(self, info, product_id=None, start_date=None, end_date=None):
        query = StockInModel.query

        if product_id:
            query = query.filter(StockInModel.product_id == product_id)
        if start_date:
            query = query.filter(StockInModel.date >= datetime.strptime(start_date, "%Y-%m-%d").date())
        if end_date:
            query = query.filter(StockInModel.date <= datetime.strptime(end_date, "%Y-%m-%d").date())

        return query.order_by(StockInModel.date.desc()).all()

# Mutation
class Mutation(graphene.ObjectType):
    record_stock_in = RecordStockIn.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
