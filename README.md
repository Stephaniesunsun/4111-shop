Wei Sun - COLUMBIA UNIVERSITY: ws2614

Wenxi Chen - COLUMBIA UNIVERSITY: wc2746

Course Name - Introduction to Databases

Subject Code - COMS 4111

# 4111-shop

1.PostgreSQL account: ws2614

2.URL: http://34.148.151.155:8111/

3.Target functions
  For customer:
  1. Sign up/ login
  2. Show all the products
  3. Show all the orders have been made by customer
  4. Query product information (by product name, brand, size)
  5. Add product to shopping cart
  6. Check out page: show order detail, customer information, payment methods, shipping
  information, etc

  For employees:
  1. Login using employee id
  2. Add/ delete /edit product information
  3. Show all the orders have been made by customer
  4. Edit stock information
  a. If stock for a product is empty, we don’t show the product on page
  4. Can see all the customer, order information

The above functions are all achieved in our application, besides we add a query supply_company based on product_id function for employees to utilize the supply_company entities.

4.We enable the search of products with keywords in brand or name and products with exact size the customers are searching for. We used a simple 'or' logic and string containment search in the backend to filter all the products we need.
Meanwhile the application enables employees to query product suppliers by joining product table, stock table and supply_company table. Also employees can update the product information and the app provides entity options they want to update based on the column information in the database.
