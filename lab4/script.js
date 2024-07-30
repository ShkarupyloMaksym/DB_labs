use online_store

//-----------------------------------------------------------
//// 1) Створіть декілька товарів з різним набором властивостей

db.items.insertMany([
    {"category": "Laptop", "model": "MacBook Air", "producer": "Apple", "price": 999},
    {"category": "Phone", "model": "iPhone 14", "producer": "Apple", "price": 999},
    {"category": "Smart Speaker", "model": "Google Nest Audio", "producer": "Google", "price": 99},
    {"category": "Gaming Console", "model": "Xbox Series X", "producer": "Microsoft", "price": 499},
    {"category": "Router", "model": "Asus RT-AX88U", "producer": "Asus", "price": 349},
    {"category": "Fitness Tracker", "model": "Garmin Venu Sq", "producer": "Garmin", "price": 199},
    {"category": "Phone", "model": "Samsung Galaxy S22", "producer": "Samsung", "price": 999},
    {"category": "Phone", "model": "Google Pixel 6", "producer": "Google", "price": 599},
    {"category": "Phone", "model": "OnePlus 10 Pro", "producer": "OnePlus", "price": 799},
    {"category": "Phone", "model": "Xiaomi Mi 12", "producer": "Xiaomi", "price": 749},
]);
-----------------------------------------------------------
// 2) Напишіть запит, який виводить усі товари (відображення у JSON)

db.items.find().pretty();
//-----------------------------------------------------------
// 3)Підрахуйте скільки товарів у певної категорії

db.items.countDocuments({"category": "Phone"});
//-----------------------------------------------------------
// 4) Підрахуйте скільки є різних категорій товарів

db.items.distinct("category").length;
//-----------------------------------------------------------
// 5)Виведіть список всіх виробників товарів без повторів

db.items.distinct("producer");
//-----------------------------------------------------------
// 6)Напишіть запити, які вибирають товари за різними критеріям і їх сукупності: 
        //a) категорія та ціна (в проміжку) - конструкція $and, 
        
        db.items.find({
            $and: 
            [
                { "category": "Phone" },
                { "price": { $gte: 750, $lte: 1000 } }
            ]
        });
        //b) модель чи одна чи інша - конструкція $or,
        
        db.items.find({
            $or: 
            [
                { "model": "Google Pixel 6" },
                { "model": "Not Exists" }
            ]
        });
        //c) виробники з переліку - конструкція $in
        
        var producers = ["Xiaomi", "Samsung", "Google"];
        db.items.find({ "producer": { $in: producers } });
//-----------------------------------------------------------
// 7) Оновіть певні товари, змінивши існуючі значення і додайте нові властивості (характеристики) усім товарам за певним критерієм

db.items.updateMany(
    { "producer": "Xiaomi" }, // Criteria to select items produced by Apple
    { 
        $set: { "price": 100, "features": "Comunism" } // Change the price to 700 and set "features" to "Face ID"
    }
);
db.items.find().pretty();
//-----------------------------------------------------------
// 8) Знайдіть товари у яких є (присутнє поле) певні властивості

db.items.find({ "features": { $exists: true } });
//-----------------------------------------------------------
// 9) Для знайдених товарів збільшіть їх вартість на певну суму 

db.items.updateMany(
    { "features": { $exists: true } }, // Criteria to select items with the "features" field
    { 
        $inc: { "price": -10 }
    }
);
db.items.find().pretty();
//-----------------------------------------------------------



// 1) Створіть кілька замовлень з різними наборами товарів, але так щоб один з товарів був у декількох замовленнях

db.orders.insertMany([
    {
        "order_number": 1,
        "date": ISODate("2024-05-11"),
        "total_sum": 849,
        "customer": {
            "name": "Michael",
            "surname": "Williams",
            "phones": [7654321, 2345678],
            "address": "101 Pine St, Somewhere, USA"
        },
        "payment": {
            "card_owner": "Julia Ivanova",
            "cardId": 87654321
        },
        "items": [
            ObjectId("664a59a4225c9bb32ebe1e0f"),
            ObjectId("664a59a4225c9bb32ebe1e10")
        ]
    },
    {
        "order_number": 2,
        "date": ISODate("2024-05-12"),
        "total_sum": 1997,
        "customer": {
            "name": "Sara",
            "surname": "Wilson",
            "phones": [7654321, 2345678],
            "address": "202 Spruce St, Somewhere, USA"
        },
        "payment": {
            "card_owner": "Julia Ivanova",
            "cardId": 87654321
        },
        "items": [
            ObjectId("664a59a4225c9bb32ebe1e12"),
            ObjectId("664a59a4225c9bb32ebe1e13"),
            ObjectId("664a59a4225c9bb32ebe1e14")
        ]
    },
    {
        "order_number": 3,
        "date": ISODate("2024-05-13"),
        "total_sum": 400,
        "customer": {
            "name": "Lucas",
            "surname": "Moore",
            "phones": [7654321, 2345678],
            "address": "303 Birch St, Somewhere, USA"
        },
        "payment": {
            "card_owner": "Julia Ivanova",
            "cardId": 87654321
        },
        "items": [
            ObjectId("664a59a4225c9bb32ebe1e17")
        ]
    },
    {
        "order_number": 4,
        "date": ISODate("2024-05-14"),
        "total_sum": 2750,
        "customer": {
            "name": "Natalie",
            "surname": "Miller",
            "phones": [7654321, 2345678],
            "address": "404 Fir St, Somewhere, USA"
        },
        "payment": {
            "card_owner": "Julia Ivanova",
            "cardId": 87654321
        },
        "items": [
            ObjectId("664a59a4225c9bb32ebe1e18"),
            ObjectId("664a59c9225c9bb32ebe1e19"),
            ObjectId("664a59c9225c9bb32ebe1e1a")
        ]
    },
    {
        "order_number": 5,
        "date": ISODate("2024-05-15"),
        "total_sum": 1200,
        "customer": {
            "name": "Oliver",
            "surname": "Garcia",
            "phones": [7654321, 2345678],
            "address": "505 Cedar St, Somewhere, USA"
        },
        "payment": {
            "card_owner": "Julia Ivanova",
            "cardId": 87654321
        },
        "items": [
            ObjectId("664a59c9225c9bb32ebe1e1d"),
            ObjectId("664a59c9225c9bb32ebe1e20")
        ]
    },
    {
        "order_number": 6,
        "date": ISODate("2024-05-16"),
        "total_sum": 1599,
        "customer": {
            "name": "Ethan",
            "surname": "Hernandez",
            "phones": [7654321, 2345678],
            "address": "606 Pine St, Somewhere, USA"
        },
        "payment": {
            "card_owner": "Julia Ivanova",
            "cardId": 87654321
        },
        "items": [
            ObjectId("664a59c9225c9bb32ebe1e20"),
            ObjectId("664a59c9225c9bb32ebe1e21")
        ]
    }
]);



//-----------------------------------------------------------
// 2) Виведіть всі замовлення
db.orders.find();

//-----------------------------------------------------------
// 3) Виведіть замовлення з вартістю більше певного значення
db.orders.find({ "total_sum": { $gt: 2000 } });


//-----------------------------------------------------------
// 4) Знайдіть замовлення зроблені одним замовником

db.orders.find({ "customer.name": "Natalie", "customer.surname": "Miller" });
//-----------------------------------------------------------
// 5) Знайдіть всі замовлення з певним товаром (товарами) (шукати можна по ObjectId)

var itemId = ObjectId("664a59c9225c9bb32ebe1e20");
db.orders.find({ "items": itemId });

//-----------------------------------------------------------
// 6) Додайте в усі замовлення з певним товаром ще один товар і збільште існуючу вартість замовлення на деяке значення Х
//
db.orders.updateMany(
    { "items": ObjectId("664a59c9225c9bb32ebe1e20") },
    {
        $push: { "items": ObjectId("664a59c9225c9bb32ebe1e1d") },
        $inc: { "total_sum": 100 }
    }
);
//-----------------------------------------------------------
// 7) Виведіть кількість товарів в певному замовленні
//
var orderIdToCount = ObjectId("664a59c9225c9bb32ebe1e1d"); 
var order = db.orders.findOne({ "_id": orderIdToCount });
if (order) {
    var itemCount = order.items.length;
    print("Order ID: " + order._id);
    print("Number of items in order: " + itemCount);
} else {
    print("Order not found with the specified ID.");
}
//-----------------------------------------------------------
// 8) Виведіть тільки інформацію про кастомера і номери кредитної карт, для замовлень вартість яких перевищує певну суму

db.orders.find(
    { "total_sum": { $gt: 2000 } },
    { "_id": 0, "customer.name": 1, "customer.surname": 1, "customer.phones": 1, "payment.card_owner": 1 }
);
//-----------------------------------------------------------
// 9) Видаліть товар з замовлень, зроблених за певний період дат
var startDate = new Date("2024-05-15");
var endDate = new Date("2024-05-18");

db.orders.updateMany(
    { "date": { $gte: startDate, $lte: endDate } },
    { $pull: { "items": { $exists: true } } }
);

db.orders.find()
//-----------------------------------------------------------
// 10) Перейменуйте у всіх замовлення ім'я (прізвище) замовника
//
db.orders.updateMany(
    {},
    { $set: { "customer.surname": "Usyk" } }
);

db.orders.find()

// 11) Знайдіть замовлення зроблені одним замовником, і виведіть тільки інформацію про кастомера та товари у замовлені підставивши заміст ObjectId("***") назви товарів та їх вартість (аналог join-а між таблицями orders та items).

db.orders.aggregate([
  { $match: { "customer.name": "Oliver", "customer.surname": "Usyk" } },
  { $unwind: "$items" },
  {
    $lookup: {
      from: "items",
      localField: "items",
      foreignField: "_id",
      as: "itemDetails"
    }
  },
  {
    $group: {
      _id: "$_id",
      customer: { $first: "$customer" },
      items: { $push: "$itemDetails" },
      total_sum: { $first: "$total_sum" }
    }
  },
  {
    $project: {
      _id: 0,
      customer: 1,
      items: { $arrayElemAt: ["$items", 0] },
      total_sum: 1
    }
  }
]);
//-----------------------------------------------------------
// 12) Створіть Сapped collection яка б містила 5 останніх відгуків на наш інтернет-магазин. Структуру запису визначити самостійно.
db.createCollection("reviews", { capped: true, size: 100000, max: 5 });
db.reviews.insertMany([
  { 
    "customer_name": "Daniel Jones",
    "rating": 4,
    "comment": "Products are reliable and support is helpful.",
    "date": ISODate("2024-05-10")
  },
  { 
    "customer_name": "Sara Wilson",
    "rating": 5,
    "comment": "Perfect experience, everything arrived on time!",
    "date": ISODate("2024-05-09")
  },
  { 
    "customer_name": "Lucas Moore",
    "rating": 2,
    "comment": "Delayed shipping, and customer service could be better.",
    "date": ISODate("2024-05-08")
  },
  { 
    "customer_name": "Natalie Miller",
    "rating": 5,
    "comment": "Couldn’t be happier with the purchase! Top-notch.",
    "date": ISODate("2024-05-07")
  },
  { 
    "customer_name": "Oliver Garcia",
    "rating": 3,
    "comment": "Decent prices, but the product quality is just average.",
    "date": ISODate("2024-05-06")
  }
]);

db.reviews.find().sort({ date: -1 });
