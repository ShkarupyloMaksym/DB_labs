//populate
MATCH (n)
DETACH DELETE n;

CREATE (i1:Item {id: 1, name: "Math", price: 400}),
       (i2:Item {id: 2, name: "IT", price: 1000}),
       (i3:Item {id: 3, name: "Biology", price: 200});

CREATE (c1:Customer {id: 1, name: "Oleh"}),
       (c2:Customer {id: 2, name: "Ivan"}),
       (c3:Customer {id: 3, name: "Maks"});

CREATE (o1:Order {id: 1, date: date("2024-06-01")}),
       (o2:Order {id: 2, date: date("2024-06-02")}),
       (o3:Order {id: 3, date: date("2024-06-03")});

MATCH (c1:Customer {id: 1}), (o1:Order {id: 1})
MERGE (c1)-[:BOUGHT]->(o1);

MATCH (c1:Customer {id: 2}), (o2:Order {id: 2})
MERGE (c1)-[:BOUGHT]->(o2);

MATCH (c2:Customer {id: 2}), (o3:Order {id: 3})
MERGE (c2)-[:BOUGHT]->(o3);

MATCH (i1:Item {id: 1}), (o1:Order {id: 1})
MERGE (i1)-[:CONTAINS]->(o1);

MATCH (i2:Item {id: 2}), (o1:Order {id: 1})
MERGE (i2)-[:CONTAINS]->(o1);

MATCH (i2:Item {id: 2}), (o2:Order {id: 2})
MERGE (i2)-[:CONTAINS]->(o2);

MATCH (i3:Item {id: 3}), (o3:Order {id: 3})
MERGE (i3)-[:CONTAINS]->(o3);

MATCH (c1:Customer {id: 1}), (i1:Item {id: 1})
MERGE (c1)-[:VIEW]->(i1);

MATCH (c1:Customer {id: 3}), (i1:Item {id: 1})
MERGE (c1)-[:VIEW]->(i1);

MATCH (c1:Customer {id: 2}), (i3:Item {id: 3})
MERGE (c1)-[:VIEW]->(i3);
