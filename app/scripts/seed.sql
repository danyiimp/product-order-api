-- Seed example data for product order API database
-- Clear existing data (in reverse order of dependencies)
TRUNCATE TABLE public.order_item CASCADE;
TRUNCATE TABLE public."order" CASCADE;
TRUNCATE TABLE public.item CASCADE;
TRUNCATE TABLE public.category CASCADE;
TRUNCATE TABLE public.customer CASCADE;

-- Reset sequences
ALTER SEQUENCE IF EXISTS public.category_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS public.customer_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS public.item_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS public.order_id_seq RESTART WITH 1;

-- Insert Categories
INSERT INTO public.category (name, parent_id) VALUES
('Electronics', NULL),
('Computers', 1),
('Laptops', 2),
('Desktops', 2),
('Smartphones', 1),
('Clothing', NULL),
('Men''s Clothing', 6),
('Women''s Clothing', 6),
('Home & Garden', NULL),
('Furniture', 9);

-- Insert Customers
INSERT INTO public.customer (name, address) VALUES
('John Smith', '123 Main St, New York, NY 10001'),
('Emma Johnson', '456 Oak Ave, Los Angeles, CA 90001'),
('Michael Brown', '789 Pine Rd, Chicago, IL 60601'),
('Sarah Davis', '321 Elm St, Houston, TX 77001'),
('David Wilson', '654 Maple Dr, Phoenix, AZ 85001');

-- Insert Items
INSERT INTO public.item (name, quantity, price, category_id) VALUES
-- Electronics > Computers > Laptops
('MacBook Pro 16"', 15, 2499.99, 3),
('Dell XPS 13', 20, 1299.99, 3),
('ThinkPad X1 Carbon', 12, 1599.99, 3),
-- Electronics > Computers > Desktops
('iMac 27"', 8, 1999.99, 4),
('HP Pavilion Desktop', 10, 899.99, 4),
-- Electronics > Smartphones
('iPhone 15 Pro', 25, 999.99, 5),
('Samsung Galaxy S24', 30, 899.99, 5),
('Google Pixel 8', 18, 699.99, 5),
-- Clothing > Men's
('Men''s Cotton T-Shirt', 100, 19.99, 7),
('Men''s Denim Jeans', 50, 59.99, 7),
-- Clothing > Women's
('Women''s Summer Dress', 60, 79.99, 8),
('Women''s Yoga Pants', 75, 39.99, 8),
-- Home & Garden > Furniture
('Leather Sofa', 5, 1299.99, 10),
('Dining Table Set', 7, 899.99, 10),
('Office Chair', 20, 249.99, 10);

-- Insert Orders
INSERT INTO public."order" (customer_id, created_at) VALUES
(1, '2024-01-15 10:30:00+00'),
(1, '2024-02-20 14:45:00+00'),
(2, '2024-01-22 09:15:00+00'),
(3, '2024-02-05 16:20:00+00'),
(3, '2024-03-10 11:00:00+00'),
(4, '2024-02-28 13:30:00+00'),
(5, '2024-03-15 15:45:00+00'),
(2, '2024-03-20 10:00:00+00');

-- Insert Order Items
-- Order 1 (John Smith - Jan 15)
INSERT INTO public.order_item (order_id, item_id, quantity) VALUES
(1, 1, 1),  -- MacBook Pro
(1, 6, 1);  -- iPhone 15 Pro

-- Order 2 (John Smith - Feb 20)
INSERT INTO public.order_item (order_id, item_id, quantity) VALUES
(2, 9, 3),  -- T-Shirts
(2, 10, 2); -- Jeans

-- Order 3 (Emma Johnson - Jan 22)
INSERT INTO public.order_item (order_id, item_id, quantity) VALUES
(3, 11, 2), -- Summer Dress
(3, 12, 1); -- Yoga Pants

-- Order 4 (Michael Brown - Feb 5)
INSERT INTO public.order_item (order_id, item_id, quantity) VALUES
(4, 13, 1); -- Leather Sofa

-- Order 5 (Michael Brown - Mar 10)
INSERT INTO public.order_item (order_id, item_id, quantity) VALUES
(5, 2, 1),  -- Dell XPS 13
(5, 7, 1),  -- Samsung Galaxy
(5, 15, 1); -- Office Chair

-- Order 6 (Sarah Davis - Feb 28)
INSERT INTO public.order_item (order_id, item_id, quantity) VALUES
(6, 4, 1),  -- iMac
(6, 15, 2); -- Office Chairs

-- Order 7 (David Wilson - Mar 15)
INSERT INTO public.order_item (order_id, item_id, quantity) VALUES
(7, 14, 1), -- Dining Table Set
(7, 15, 4); -- Office Chairs

-- Order 8 (Emma Johnson - Mar 20)
INSERT INTO public.order_item (order_id, item_id, quantity) VALUES
(8, 8, 1),  -- Google Pixel
(8, 9, 5),  -- T-Shirts
(8, 12, 2); -- Yoga Pants

-- Verify data
SELECT 'Categories' as table_name, COUNT(*) as count FROM public.category
UNION ALL
SELECT 'Customers', COUNT(*) FROM public.customer
UNION ALL
SELECT 'Items', COUNT(*) FROM public.item
UNION ALL
SELECT 'Orders', COUNT(*) FROM public."order"
UNION ALL
SELECT 'Order Items', COUNT(*) FROM public.order_item;
