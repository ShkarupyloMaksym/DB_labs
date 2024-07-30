//3. Order of Customer
//Знайти всі Orders конкретного Customer

MATCH (customer:Customer {id: 1})-[:BOUGHT]->(order:Order)
RETURN order;