import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import StockOut as StockOutModel
from database import db_session
from datetime import datetime
import requests

# GraphQL Type
class StockOut(SQLAlchemyObjectType):
    class Meta:
        model = StockOutModel

# Fungsi bantu: Ambil stok produk dari inventory-service
def get_product_stock(product_id):
    try:
        response = requests.post(
            "http://inventory-service:5000/graphql",
            json={"query": f"""
                query {{
                    product(id: {product_id}) {{
                        id
                        quantity
                    }}
                }}
            """}
        )
        data = response.json()
        return data["data"]["product"]["quantity"]
    except Exception as e:
        print("Error checking stock:", e)
        return None

# Mutation
class CreateStockOut(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        quantity_used = graphene.Int(required=True)
        usage_date = graphene.String(required=True)
        issued_to_service = graphene.String()
        related_id = graphene.String()

    stock_out = graphene.Field(lambda: StockOut)

    def mutate(self, info, product_id, quantity_used, usage_date, issued_to_service=None, related_id=None):
        # Cek stok terlebih dahulu
        available_stock = get_product_stock(product_id)
        if available_stock is None:
            raise Exception("Gagal mengambil data stok produk.")
        if quantity_used > available_stock:
            raise Exception("Stok tidak mencukupi untuk transaksi ini.")

        # Simpan data ke database
        stock_out = StockOutModel(
            product_id=product_id,
            quantity_used=quantity_used,
            usage_date=datetime.strptime(usage_date, "%Y-%m-%d").date(),
            issued_to_service=issued_to_service,
            related_id=related_id
        )
        db_session.add(stock_out)
        db_session.commit()

        # Kirim permintaan update stok ke inventory-service
        try:
            requests.post(
                "http://inventory-service:5000/graphql",
                json={"query": f"""
                    mutation {{
                        updateProduct(id: {product_id}, quantity: {available_stock - quantity_used}) {{
                            product {{ id quantity }}
                        }}
                    }}
                """}
            )
        except Exception as e:
            print("Gagal mengurangi stok di inventory:", e)

        return CreateStockOut(stock_out=stock_out)

# Query
class Query(graphene.ObjectType):
    stock_out = graphene.Field(StockOut, id=graphene.Int(required=True))
    stock_outs = graphene.List(
        StockOut,
        product_id=graphene.Int(),
        issued_to_service=graphene.String(),
        start_date=graphene.String(),
        end_date=graphene.String()
    )

    def resolve_stock_out(self, info, id):
        return StockOutModel.query.get(id)

    def resolve_stock_outs(self, info, product_id=None, issued_to_service=None, start_date=None, end_date=None):
        query = StockOutModel.query

        if product_id:
            query = query.filter(StockOutModel.product_id == product_id)
        if issued_to_service:
            query = query.filter(StockOutModel.issued_to_service == issued_to_service)
        if start_date:
            query = query.filter(StockOutModel.usage_date >= datetime.strptime(start_date, "%Y-%m-%d").date())
        if end_date:
            query = query.filter(StockOutModel.usage_date <= datetime.strptime(end_date, "%Y-%m-%d").date())

        return query.all()

# Schema
class Mutation(graphene.ObjectType):
    create_stock_out = CreateStockOut.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
