# Groceries Backend Service

A Django REST Framework-based service for managing products, categories, customers, and orders with:

- **OpenID Connect authentication** for secure user login
- **Hierarchical product categories** using `django-mptt`
- **Africa's Talking SMS** notifications for customers
- **Email alerts** for administrators
- **Interactive API documentation** via `drf-yasg`

---

## **Implemented Solution Overview**

This backend powers a grocery ordering application with the following workflow:

1. **Customer Login**  
   Customers authenticate via OpenID Connect and receive a token for subsequent requests.

2. **Browse & Select Products**  
   Products are organized in a multi-level category structure using MPTT. The API exposes endpoints to browse categories and products.

3. **Place an Order**  
   Customers add products to their cart and submit an order. The backend:
   - Creates an `Order` record
   - Associates `OrderItem` entries for each product
   - Calculates the total amount

4. **Notifications**  
   Upon order creation:
   - An **SMS** is sent to the customer confirming their order (via Africa’s Talking)
   - An **email** is sent to the administrator with the order details

5. **Order Completion**  
   Customers can mark their order as complete, updating the status in the database.

---

## **System Sequence Diagram**

![System Sequence Diagram](https://github.com/user-attachments/assets/98497669-56b5-4b57-97cc-2d6bb16a00ad)

---

## **Key Features**
- **Authentication**: OpenID Connect for secure login
- **Products & Categories**: MPTT-based hierarchical category structure
- **Order Management**: Create, track, and complete orders
- **Notifications**: SMS for customers, email for admins
- **API Documentation**: `/swagger/` and `/redoc/` endpoints via `drf-yasg`

---

## **Setup**

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/groceries-backend.git
cd groceries-backend
