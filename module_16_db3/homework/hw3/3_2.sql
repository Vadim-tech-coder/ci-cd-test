SELECT pc.model, pc.price
FROM pc JOIN product ON pc.model=product.model
WHERE product.maker='B'
UNION
SELECT laptop.model, Laptop.price
FROM laptop JOIN product ON laptop.model=product.model
WHERE product.maker='B'
UNION
SELECT printer.model, printer.price
FROM printer JOIN product ON printer.model=product.model
WHERE product.maker='B'