import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import desc, asc
from models import Product as ProductModel
from models import Supplier as SupplierModel
from database import db_session

# Object Types
class Product(SQLAlchemyObjectType):
    price_idr = graphene.String(description="Price in IDR format")
    
    class Meta:
        model = ProductModel

class Supplier(SQLAlchemyObjectType):
    class Meta:
        model = SupplierModel

# Input Types for Filtering
class ProductFilter(graphene.InputObjectType):
    name = graphene.String()
    supplier_id = graphene.Int()
    min_quantity = graphene.Int()
    max_quantity = graphene.Int()
    min_price = graphene.Float()
    max_price = graphene.Float()

# Pagination Input
class PaginationInput(graphene.InputObjectType):
    page = graphene.Int(default_value=1)
    per_page = graphene.Int(default_value=10)

# Sorting Input
class SortInput(graphene.InputObjectType):
    field = graphene.String()
    order = graphene.String()

# Query
class Query(graphene.ObjectType):
    products = graphene.List(
        Product,
        filter=graphene.Argument(ProductFilter),
        pagination=graphene.Argument(PaginationInput),
        sort=graphene.Argument(SortInput)
    )
    product = graphene.Field(Product, id=graphene.Int())
    
    suppliers = graphene.List(
        Supplier,
        pagination=graphene.Argument(PaginationInput),
        sort=graphene.Argument(SortInput)
    )
    supplier = graphene.Field(Supplier, id=graphene.Int())

    def resolve_products(self, info, filter=None, pagination=None, sort=None):
        query = ProductModel.query

        if filter:
            if filter.name:
                query = query.filter(ProductModel.name.ilike(f"%{filter.name}%"))
            if filter.supplier_id:
                query = query.filter(ProductModel.supplier_id == filter.supplier_id)
            if filter.min_quantity is not None:
                query = query.filter(ProductModel.quantity >= filter.min_quantity)
            if filter.max_quantity is not None:
                query = query.filter(ProductModel.quantity <= filter.max_quantity)
            if filter.min_price is not None:
                query = query.filter(ProductModel.unit_price >= filter.min_price)
            if filter.max_price is not None:
                query = query.filter(ProductModel.unit_price <= filter.max_price)

        if sort:
            if sort.order.lower() == 'desc':
                query = query.order_by(desc(getattr(ProductModel, sort.field)))
            else:
                query = query.order_by(asc(getattr(ProductModel, sort.field)))

        if pagination:
            query = query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)

        return query.all()

    def resolve_product(self, info, id):
        return ProductModel.query.get(id)

    def resolve_suppliers(self, info, pagination=None, sort=None):
        query = SupplierModel.query

        if sort:
            if sort.order.lower() == 'desc':
                query = query.order_by(desc(getattr(SupplierModel, sort.field)))
            else:
                query = query.order_by(asc(getattr(SupplierModel, sort.field)))

        if pagination:
            query = query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)

        return query.all()

    def resolve_supplier(self, info, id):
        return SupplierModel.query.get(id)

# Mutations
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        supplier_id = graphene.Int(required=True)
        quantity = graphene.Int()
        unit_price = graphene.Float()

    product = graphene.Field(lambda: Product)

    def mutate(self, info, name, supplier_id, description=None, quantity=0, unit_price=None):
        product = ProductModel(
            name=name,
            description=description,
            supplier_id=supplier_id,
            quantity=quantity,
            unit_price=unit_price
        )
        db_session.add(product)
        db_session.commit()
        return CreateProduct(product=product)

class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()
        supplier_id = graphene.Int()
        quantity = graphene.Int()
        unit_price = graphene.Float()

    product = graphene.Field(lambda: Product)

    def mutate(self, info, id, name=None, description=None, supplier_id=None, quantity=None, unit_price=None):
        product = ProductModel.query.get(id)
        if not product:
            raise Exception('Product not found')

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if supplier_id is not None:
            product.supplier_id = supplier_id
        if quantity is not None:
            product.quantity = quantity
        if unit_price is not None:
            product.unit_price = unit_price

        db_session.commit()
        return UpdateProduct(product=product)

class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        product = ProductModel.query.get(id)
        if not product:
            raise Exception('Product not found')

        db_session.delete(product)
        db_session.commit()
        return DeleteProduct(success=True)

class CreateSupplier(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        contact_info = graphene.String()
        address = graphene.String()

    supplier = graphene.Field(lambda: Supplier)

    def mutate(self, info, name, contact_info=None, address=None):
        supplier = SupplierModel(
            name=name,
            contact_info=contact_info,
            address=address
        )
        db_session.add(supplier)
        db_session.commit()
        return CreateSupplier(supplier=supplier)

class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
    create_supplier = CreateSupplier.Field()

schema = graphene.Schema(query=Query, mutation=Mutation) 