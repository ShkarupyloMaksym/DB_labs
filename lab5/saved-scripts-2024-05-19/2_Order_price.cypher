//2. Order price
//Підрахувати вартість конкретного Order

MATCH (:Order {id: 1})<-[:CONTAINS]-(item:Item)
RETURN SUM(item.price) AS total_cost;