//5. Item num of Customer
// Знайти загальну кількість Items куплені конкретним Customer (через його Order)

MATCH (:Customer {id: 1})-[:BOUGHT]->(:Order)<-[:CONTAINS]-(item:Item)
RETURN COUNT(DISTINCT item) AS total_items_bought;
