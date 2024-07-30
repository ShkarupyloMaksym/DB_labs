//4. Item of Customer
// Знайти всі Items куплені конкретним Customer (через його Orders)

MATCH (:Customer {id: 1})-[:BOUGHT]->(:Order)<-[:CONTAINS]-(item:Item)
RETURN DISTINCT item;