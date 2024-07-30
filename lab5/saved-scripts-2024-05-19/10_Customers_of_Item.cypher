//10. Customers of Item
// Знайти Customers які купили даний конкретний Item

MATCH (item:Item {id: 2})-[:CONTAINS]-(order:Order)-[:BOUGHT]-(customer:Customer)
RETURN DISTINCT customer;