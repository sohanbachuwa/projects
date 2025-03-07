Overview*
This Python program simulates a trading platform. It manages buy and sell orders, facilitates matching of orders, and logs transactions. The goal is to replicate a basic trading system using an in-memory order book.
#Key Components*
1. **`Order` Class**:
    - Represents an individual order in the system.
    - Each order has attributes such as:
        - `ticker`: Stock identifier like "AAPL".
        - `quantity`: Number of shares.
        - `price`: Price per share.
        - `order_type`: Indicates if it is a BUY or SELL.
        - `timestamp`: Creation time of the order.

2. **`OrderBook` Class**:
    - Manages all buy and sell orders.
    - Responsible for:
        - Storing and organizing orders.
        - Matching compatible BUY and SELL orders.
        - Logging completed transactions.

    - Includes locking mechanisms to ensure thread-safe operations.

3. **Functions**:
    - **`simulate_trading` **: Runs the trading simulation, processing and matching orders.
    - **`display_order_book_stats` **: Provides details about active orders in the order book.
    - **`main` **: The entry point that brings everything together.

## **How It Works**
1. **Order Addition**:
    - Users can add BUY or SELL orders by specifying their details.

2. **Order Matching**:
    - Orders are matched based on price and quantity:
        - A SELL order matches if its price meets or is less than a BUY order’s price.

    - If matched, transactions are logged, and the orders are removed from the active lists.

3. **Simulation Execution**:
    - The simulation processes orders dynamically.
    - Users can view order book statistics at any point.
