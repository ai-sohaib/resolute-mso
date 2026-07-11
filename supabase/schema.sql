create extension if not exists pgcrypto;

create table if not exists site_settings (id uuid primary key default gen_random_uuid(), setting_key text unique not null, setting_value jsonb not null default '{}'::jsonb, updated_at timestamptz default now());
create table if not exists page_sections (id uuid primary key default gen_random_uuid(), page_slug text not null, section_key text not null, title text, body text, sort_order int default 0, is_published boolean default true, updated_at timestamptz default now());
create table if not exists services (id uuid primary key default gen_random_uuid(), slug text unique not null, title text not null, summary text, bullets jsonb default '[]'::jsonb, icon text, sort_order int default 0, is_published boolean default true);
create table if not exists specialties (id uuid primary key default gen_random_uuid(), slug text unique not null, title text not null, description text, pain_points jsonb default '[]'::jsonb, support text, services jsonb default '[]'::jsonb, icon text, sort_order int default 0, is_published boolean default true);
create table if not exists resources (id uuid primary key default gen_random_uuid(), slug text unique not null, tag text, title text not null, excerpt text, body text, is_published boolean default true, created_at timestamptz default now());
create table if not exists leads (id uuid primary key default gen_random_uuid(), name text, email text, service_interest text, source text default 'website', created_at timestamptz default now());
create table if not exists demo_requests (id uuid primary key default gen_random_uuid(), name text not null, email text not null, services_interested text not null, created_at timestamptz default now());
create table if not exists contact_messages (id uuid primary key default gen_random_uuid(), name text not null, email text not null, phone text, organization text, service_interest text, message text not null, created_at timestamptz default now());

create table if not exists newsletter_subscribers (id uuid primary key default gen_random_uuid(), email text not null, source text default 'website_footer', created_at timestamptz default now());
