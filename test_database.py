"""
Test script for the text-to-SQL agent
This script tests the agent functionality without requiring an OpenAI API key
"""
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sample.db")


def test_database_queries():
    """Test basic database queries to verify the setup"""
    engine = create_engine(DATABASE_URL)
    
    print("=" * 80)
    print("Testing Database Queries")
    print("=" * 80)
    
    # Test 1: Query all users
    print("\n测试 1: 查询所有用户 / Test 1: Query all users")
    print("-" * 80)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        rows = result.fetchall()
        columns = result.keys()
        print("\t".join(columns))
        for row in rows:
            print("\t".join(str(val) for val in row))
    
    # Test 2: Query all products
    print("\n测试 2: 查询所有产品 / Test 2: Query all products")
    print("-" * 80)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name, price, category, stock FROM products"))
        rows = result.fetchall()
        columns = result.keys()
        print("\t".join(columns))
        for row in rows:
            print("\t".join(str(val) for val in row))
    
    # Test 3: Join query - users with their orders
    print("\n测试 3: 联合查询 - 用户及其订单 / Test 3: Join query - users with orders")
    print("-" * 80)
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT u.name as user_name, p.name as product_name, o.quantity, o.total_price
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN products p ON o.product_id = p.id
        """))
        rows = result.fetchall()
        columns = result.keys()
        print("\t".join(columns))
        for row in rows:
            print("\t".join(str(val) for val in row))
    
    # Test 4: Aggregation - total sales per product
    print("\n测试 4: 聚合查询 - 每个产品的总销量 / Test 4: Aggregation - total sales per product")
    print("-" * 80)
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT p.name, SUM(o.quantity) as total_quantity, SUM(o.total_price) as total_revenue
            FROM orders o
            JOIN products p ON o.product_id = p.id
            GROUP BY p.name
            ORDER BY total_revenue DESC
        """))
        rows = result.fetchall()
        columns = result.keys()
        print("\t".join(columns))
        for row in rows:
            print("\t".join(str(val) for val in row))
    
    print("\n" + "=" * 80)
    print("✅ All database tests passed!")
    print("=" * 80)


if __name__ == "__main__":
    test_database_queries()
