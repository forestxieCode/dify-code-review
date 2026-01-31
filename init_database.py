"""
Initialize sample database for testing the text-to-SQL agent
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sample.db")

Base = declarative_base()


class User(Base):
    """User table"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    orders = relationship("Order", back_populates="user")


class Product(Base):
    """Product table"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50))
    stock = Column(Integer, default=0)
    
    # Relationship
    orders = relationship("Order", back_populates="product")


class Order(Base):
    """Order table"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")


def init_database():
    """Initialize database with sample data"""
    print("Creating database...")
    engine = create_engine(DATABASE_URL)
    
    # Drop all tables if they exist
    Base.metadata.drop_all(engine)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Add sample users
    users = [
        User(name="张三", email="zhangsan@example.com", age=28),
        User(name="李四", email="lisi@example.com", age=32),
        User(name="王五", email="wangwu@example.com", age=25),
        User(name="赵六", email="zhaoliu@example.com", age=35),
    ]
    session.add_all(users)
    
    # Add sample products
    products = [
        Product(name="笔记本电脑", price=5999.00, category="电子产品", stock=50),
        Product(name="机械键盘", price=499.00, category="电子产品", stock=100),
        Product(name="显示器", price=1299.00, category="电子产品", stock=30),
        Product(name="鼠标", price=99.00, category="电子产品", stock=200),
        Product(name="办公椅", price=899.00, category="家具", stock=25),
    ]
    session.add_all(products)
    
    # Commit to get IDs
    session.commit()
    
    # Add sample orders
    orders = [
        Order(user_id=1, product_id=1, quantity=1, total_price=5999.00),
        Order(user_id=1, product_id=2, quantity=2, total_price=998.00),
        Order(user_id=2, product_id=3, quantity=1, total_price=1299.00),
        Order(user_id=3, product_id=4, quantity=3, total_price=297.00),
        Order(user_id=4, product_id=5, quantity=1, total_price=899.00),
        Order(user_id=2, product_id=1, quantity=1, total_price=5999.00),
    ]
    session.add_all(orders)
    
    # Commit all changes
    session.commit()
    session.close()
    
    print("✅ Database initialized successfully!")
    print(f"   - Created {len(users)} users")
    print(f"   - Created {len(products)} products")
    print(f"   - Created {len(orders)} orders")


if __name__ == "__main__":
    init_database()
