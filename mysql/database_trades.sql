use db;

CREATE TABLE trades(
    trade_id int not null AUTO_INCREMENT,
    item_name varchar(1000),
    sell_price float,
    buy_price float,
    profit float,
    PRIMARY KEY (trade_id)
);

INSERT INTO trades(item_name, sell_price, buy_price, profit)
VALUES("teste", 3.55, 1.55, 2);