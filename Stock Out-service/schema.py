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
                        name
                        min_stock
                    }}
                }}
            """}
        )
        data = response.json()
        return data["data"]["product"]
    except Exception as e:
        print("Error checking stock:", e)
        return None

# Mutation
class CreateStockOut(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        quantity_used = graphene.Int(required=True)
        usage_date = graphene.String(required=True)
        issued_to_service = graphene.String(required=True)
        related_id = graphene.String()
        notes = graphene.String()
        approved_by = graphene.String(required=True)

    stock_out = graphene.Field(lambda: StockOut)
    message = graphene.String()

    def mutate(self, info, product_id, quantity_used, usage_date, issued_to_service, approved_by, related_id=None, notes=None):
        # Validasi input
        if quantity_used <= 0:
            raise Exception("Jumlah penggunaan harus lebih dari 0")

        # Cek stok terlebih dahulu
        product_data = get_product_stock(product_id)
        if product_data is None:
            raise Exception("Gagal mengambil data stok produk.")
        
        available_stock = product_data["quantity"]
        if quantity_used > available_stock:
            raise Exception(f"Stok tidak mencukupi. Stok tersedia: {available_stock}")

        # Cek minimum stok
        min_stock = product_data.get("min_stock", 0)
        if (available_stock - quantity_used) < min_stock:
            raise Exception(f"Pengurangan stok akan membuat stok di bawah minimum ({min_stock})")

        # Simpan data ke database
        current_time = datetime.now()
        stock_out = StockOutModel(
            product_id=product_id,
            quantity_used=quantity_used,
            usage_date=datetime.strptime(usage_date, "%Y-%m-%d").date(),
            issued_to_service=issued_to_service,
            related_id=related_id,
            notes=notes,
            created_at=current_time,
            updated_at=current_time,
            status='completed',
            approved_by=approved_by
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
            message = f"Stok berhasil dikurangi. Sisa stok: {available_stock - quantity_used}"
        except Exception as e:
            print("Gagal mengurangi stok di inventory:", e)
            message = "Stok berhasil dicatat tapi gagal update di inventory"

        return CreateStockOut(stock_out=stock_out, message=message)

# Query
class Query(graphene.ObjectType):
    stock_out = graphene.Field(StockOut, id=graphene.Int(required=True))
    stock_outs = graphene.List(
        StockOut,
        product_id=graphene.Int(),
        issued_to_service=graphene.String(),
        start_date=graphene.String(),
        end_date=graphene.String(),
        status=graphene.String()
    )

    def resolve_stock_out(self, info, id):
        return StockOutModel.query.get(id)

    def resolve_stock_outs(self, info, product_id=None, issued_to_service=None, start_date=None, end_date=None, status=None):
        query = StockOutModel.query

        if product_id:
            query = query.filter(StockOutModel.product_id == product_id)
        if issued_to_service:
            query = query.filter(StockOutModel.issued_to_service == issued_to_service)
        if start_date:
            query = query.filter(StockOutModel.usage_date >= datetime.strptime(start_date, "%Y-%m-%d").date())
        if end_date:
            query = query.filter(StockOutModel.usage_date <= datetime.strptime(end_date, "%Y-%m-%d").date())
        if status:
            query = query.filter(StockOutModel.status == status)

        return query.order_by(StockOutModel.created_at.desc()).all()

# Schema
class Mutation(graphene.ObjectType):
    create_stock_out = CreateStockOut.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
