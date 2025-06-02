import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import desc, asc
from models import Category as CategoryModel
from models import Supplier as SupplierModel
from models import Product as ProductModel
from models import StockIn as StockInModel
from models import StockOut as StockOutModel
from models import InventoryUser as InventoryUserModel
from database import db_session

# Object Types
class Category(SQLAlchemyObjectType):
    class Meta:
        model = CategoryModel

class Supplier(SQLAlchemyObjectType):
    class Meta:
        model = SupplierModel

class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel

class StockIn(SQLAlchemyObjectType):
    class Meta:
        model = StockInModel

class StockOut(SQLAlchemyObjectType):
    class Meta:
        model = StockOutModel

class InventoryUser(SQLAlchemyObjectType):
    class Meta:
        model = InventoryUserModel

# Input Types for Filtering
class ProductFilter(graphene.InputObjectType):
    name = graphene.String()
    category_id = graphene.Int()
    supplier_id = graphene.Int()
    min_quantity = graphene.Int()
    max_quantity = graphene.Int()
    min_price = graphene.Float()
    max_price = graphene.Float()

class StockFilter(graphene.InputObjectType):
    product_id = graphene.Int()
    start_date = graphene.Date()
    end_date = graphene.Date()
    min_quantity = graphene.Int()
    max_quantity = graphene.Int()

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
    # Basic queries
    categories = graphene.List(
        Category,
        pagination=graphene.Argument(PaginationInput),
        sort=graphene.Argument(SortInput)
    )
    category = graphene.Field(Category, id=graphene.Int())
    
    suppliers = graphene.List(
        Supplier,
        pagination=graphene.Argument(PaginationInput),
        sort=graphene.Argument(SortInput)
    )
    supplier = graphene.Field(Supplier, id=graphene.Int())
    
    products = graphene.List(
        Product,
        filter=graphene.Argument(ProductFilter),
        pagination=graphene.Argument(PaginationInput),
        sort=graphene.Argument(SortInput)
    )
    product = graphene.Field(Product, id=graphene.Int())
    
    stock_ins = graphene.List(
        StockIn,
        filter=graphene.Argument(StockFilter),
        pagination=graphene.Argument(PaginationInput),
        sort=graphene.Argument(SortInput)
    )
    stock_in = graphene.Field(StockIn, id=graphene.Int())
    
    stock_outs = graphene.List(
        StockOut,
        filter=graphene.Argument(StockFilter),
        pagination=graphene.Argument(PaginationInput),
        sort=graphene.Argument(SortInput)
    )
    stock_out = graphene.Field(StockOut, id=graphene.Int())

    def resolve_categories(self, info, pagination=None, sort=None):
        query = CategoryModel.query

        if sort:
            if sort.order.lower() == 'desc':
                query = query.order_by(desc(getattr(CategoryModel, sort.field)))
            else:
                query = query.order_by(asc(getattr(CategoryModel, sort.field)))

        if pagination:
            query = query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)

        return query.all()

    def resolve_category(self, info, id):
        return CategoryModel.query.get(id)

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

    def resolve_products(self, info, filter=None, pagination=None, sort=None):
        query = ProductModel.query

        if filter:
            if filter.name:
                query = query.filter(ProductModel.name.ilike(f"%{filter.name}%"))
            if filter.category_id:
                query = query.filter(ProductModel.category_id == filter.category_id)
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

    def resolve_stock_ins(self, info, filter=None, pagination=None, sort=None):
        query = StockInModel.query

        if filter:
            if filter.product_id:
                query = query.filter(StockInModel.product_id == filter.product_id)
            if filter.start_date:
                query = query.filter(StockInModel.date >= filter.start_date)
            if filter.end_date:
                query = query.filter(StockInModel.date <= filter.end_date)
            if filter.min_quantity is not None:
                query = query.filter(StockInModel.quantity >= filter.min_quantity)
            if filter.max_quantity is not None:
                query = query.filter(StockInModel.quantity <= filter.max_quantity)

        if sort:
            if sort.order.lower() == 'desc':
                query = query.order_by(desc(getattr(StockInModel, sort.field)))
            else:
                query = query.order_by(asc(getattr(StockInModel, sort.field)))

        if pagination:
            query = query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)

        return query.all()

    def resolve_stock_in(self, info, id):
        return StockInModel.query.get(id)

    def resolve_stock_outs(self, info, filter=None, pagination=None, sort=None):
        query = StockOutModel.query

        if filter:
            if filter.product_id:
                query = query.filter(StockOutModel.product_id == filter.product_id)
            if filter.start_date:
                query = query.filter(StockOutModel.usage_date >= filter.start_date)
            if filter.end_date:
                query = query.filter(StockOutModel.usage_date <= filter.end_date)
            if filter.min_quantity is not None:
                query = query.filter(StockOutModel.quantity_used >= filter.min_quantity)
            if filter.max_quantity is not None:
                query = query.filter(StockOutModel.quantity_used <= filter.max_quantity)

        if sort:
            if sort.order.lower() == 'desc':
                query = query.order_by(desc(getattr(StockOutModel, sort.field)))
            else:
                query = query.order_by(asc(getattr(StockOutModel, sort.field)))

        if pagination:
            query = query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)

        return query.all()

    def resolve_stock_out(self, info, id):
        return StockOutModel.query.get(id)

# Mutations
class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    category = graphene.Field(lambda: Category)

    def mutate(self, info, name, description=None):
        category = CategoryModel(name=name, description=description)
        db_session.add(category)
        db_session.commit()
        return CreateCategory(category=category)

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

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        category_id = graphene.Int(required=True)
        supplier_id = graphene.Int(required=True)
        quantity = graphene.Int()
        unit_price = graphene.Float()

    product = graphene.Field(lambda: Product)

    def mutate(self, info, name, category_id, supplier_id, description=None, quantity=0, unit_price=None):
        product = ProductModel(
            name=name,
            description=description,
            category_id=category_id,
            supplier_id=supplier_id,
            quantity=quantity,
            unit_price=unit_price
        )
        db_session.add(product)
        db_session.commit()
        return CreateProduct(product=product)

class CreateStockIn(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
        date = graphene.Date(required=True)
        unit_price = graphene.Float()

    stock_in = graphene.Field(lambda: StockIn)

    def mutate(self, info, product_id, quantity, date, unit_price=None):
        product = ProductModel.query.get(product_id)
        if not product:
            raise Exception('Product not found')

        stock_in = StockInModel(
            product_id=product_id,
            quantity=quantity,
            date=date,
            unit_price=unit_price
        )
        
        product.quantity += quantity
            
        db_session.add(stock_in)
        db_session.commit()
        return CreateStockIn(stock_in=stock_in)

class CreateStockOut(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        quantity_used = graphene.Int(required=True)
        usage_date = graphene.Date(required=True)
        issued_to_service = graphene.String()
        related_id = graphene.String()

    stock_out = graphene.Field(lambda: StockOut)

    def mutate(self, info, product_id, quantity_used, usage_date, issued_to_service=None, related_id=None):
        product = ProductModel.query.get(product_id)
        if not product:
            raise Exception('Product not found')
            
        if product.quantity < quantity_used:
            raise Exception('Insufficient stock quantity')

        stock_out = StockOutModel(
            product_id=product_id,
            quantity_used=quantity_used,
            usage_date=usage_date,
            issued_to_service=issued_to_service,
            related_id=related_id
        )
        
        product.quantity -= quantity_used
            
        db_session.add(stock_out)
        db_session.commit()
        return CreateStockOut(stock_out=stock_out)

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_supplier = CreateSupplier.Field()
    create_product = CreateProduct.Field()
    create_stock_in = CreateStockIn.Field()
    create_stock_out = CreateStockOut.Field()

schema = graphene.Schema(query=Query, mutation=Mutation) 