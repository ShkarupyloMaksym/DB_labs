//7. bought time
// Знайті скільки разів кожен товар був придбаний, відсортувати за цим значенням

MATCH (ords:Order)<-[:CONTAINS]-(items:Item)
RETURN items.name, count(items.name) as items_count
ORDER BY items_count DESC