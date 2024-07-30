//6. Customer price
// Знайти для Customer на яку загальну суму він придбав товарів (через його Order)

MATCH (:Customer {id: 1})-[:BOUGHT]->(:Order)<-[:CONTAINS]-(item:Item)
RETURN SUM(item.price) AS total_amount_spent;