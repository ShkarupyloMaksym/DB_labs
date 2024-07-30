//9. Item pairs
// Знайти інші Items що купувались разом з конкретним Item (тобто всі Items що входять до Order-s разом з даними Item)

MATCH (item:Item {id: 3})
MATCH (item)-[:CONTAINS]-(:Order)
MATCH (:Order)-[:CONTAINS]-(related_item:Item)
WHERE related_item <> item
RETURN DISTINCT related_item;