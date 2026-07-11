alter table site_settings enable row level security;
alter table page_sections enable row level security;
alter table services enable row level security;
alter table specialties enable row level security;
alter table resources enable row level security;
alter table leads enable row level security;
alter table demo_requests enable row level security;
alter table contact_messages enable row level security;

create policy "Public can read published services" on services for select using (is_published = true);
create policy "Public can read published specialties" on specialties for select using (is_published = true);
create policy "Public can read published resources" on resources for select using (is_published = true);
create policy "Public can submit demo requests" on demo_requests for insert with check (true);
create policy "Public can submit contact messages" on contact_messages for insert with check (true);

-- Create an app_metadata role claim or admin_members table before enabling production admin policies.
-- Example admin-only policy pattern:
-- create policy "Admins manage CMS" on page_sections for all using ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin') with check ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');

alter table newsletter_subscribers enable row level security;
create policy "Public can submit newsletter signups" on newsletter_subscribers for insert with check (true);
