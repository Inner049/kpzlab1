CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "email" varchar(255) UNIQUE NOT NULL,
  "password_hash" varchar(255) NOT NULL,
  "name" varchar(100) NOT NULL,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "categories" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer NOT NULL,
  "name" varchar(100) NOT NULL,
  "color" varchar(7) DEFAULT '#000000',
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "expenses" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer NOT NULL,
  "category_id" integer NOT NULL,
  "amount" decimal(10,2) NOT NULL,
  "description" text,
  "expense_date" date NOT NULL,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "budgets" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer NOT NULL,
  "category_id" integer NOT NULL,
  "amount" decimal(10,2) NOT NULL,
  "month" integer NOT NULL,
  "year" integer NOT NULL,
  "created_at" timestamp DEFAULT (now())
);

-- Додавання зовнішніх ключів (Foreign Keys)
ALTER TABLE "categories" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "expenses" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "expenses" ADD FOREIGN KEY ("category_id") REFERENCES "categories" ("id");
ALTER TABLE "budgets" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "budgets" ADD FOREIGN KEY ("category_id") REFERENCES "categories" ("id");

-- Створення індексів для прискорення пошуку
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_expenses_user_id ON expenses(user_id);
CREATE INDEX idx_expenses_category_id ON expenses(category_id);
CREATE INDEX idx_expenses_date ON expenses(expense_date);
CREATE INDEX idx_budgets_user_month_year ON budgets(user_id, month, year);