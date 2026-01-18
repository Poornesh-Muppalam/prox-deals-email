drop table if exists deals cascade;
drop table if exists products cascade;
drop table if exists retailers cascade;
drop table if exists users cascade;

create table retailers (
  id bigserial primary key,
  name text not null unique
);

create table products (
  id bigserial primary key,
  name text not null,
  size text not null default '',
  category text not null default '',
  unique (name, size, category)
);

create table deals (
  id bigserial primary key,
  retailer_id bigint not null references retailers(id) on delete cascade,
  product_id bigint not null references products(id) on delete cascade,
  price numeric(10,2) not null,
  start_date date not null,
  end_date date not null,
  created_at timestamptz not null default now(),
  unique (retailer_id, product_id, start_date)
);

create table users (
  id bigserial primary key,
  name text,
  email text not null unique,
  preferred_retailers text[] not null default '{}'
);
