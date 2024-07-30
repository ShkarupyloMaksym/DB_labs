//1. Item from order
//Знайти Items які входять в конкретний Order (за Order id) 

MATCH (:Order {id: 1})<-[:CONTAINS]-(item:Item)
RETURN item;