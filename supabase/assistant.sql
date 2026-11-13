-- Chordseed · Lumen assistant: question counters.
-- Paste into Supabase → SQL Editor → New query → Run. Safe to run more than once.
--   Guests (no account): 4 questions in total per device (and at most 30 per connection per day).
--   Signed-in free users: 10 more questions in total.
--   Paid Pro: 40 questions per day.

-- Signed-in users: daily count + lifetime total.
create table if not exists public.assistant_usage (
  user_id  uuid not null references auth.users(id) on delete cascade,
  day      date not null default (now() at time zone 'utc')::date,
  count    integer not null default 0,
  primary key (user_id, day)
);
create table if not exists public.assistant_user_total (
  user_id  uuid primary key references auth.users(id) on delete cascade,
  total    integer not null default 0
);
alter table public.assistant_usage enable row level security;
alter table public.assistant_user_total enable row level security;
drop policy if exists "read own assistant usage" on public.assistant_usage;
create policy "read own assistant usage" on public.assistant_usage for select using (auth.uid() = user_id);
drop policy if exists "read own assistant total" on public.assistant_user_total;
create policy "read own assistant total" on public.assistant_user_total for select using (auth.uid() = user_id);

drop function if exists public.assistant_bump();
create function public.assistant_bump()
returns json language plpgsql security definer set search_path = public as $$
declare d integer; t integer;
begin
  if auth.uid() is null then raise exception 'not signed in'; end if;
  insert into public.assistant_usage (user_id, day, count) values (auth.uid(), (now() at time zone 'utc')::date, 1)
    on conflict (user_id, day) do update set count = public.assistant_usage.count + 1 returning count into d;
  insert into public.assistant_user_total (user_id, total) values (auth.uid(), 1)
    on conflict (user_id) do update set total = public.assistant_user_total.total + 1 returning total into t;
  return json_build_object('today', d, 'total', t);
end;
$$;
revoke all on function public.assistant_bump() from public, anon;
grant execute on function public.assistant_bump() to authenticated;

-- Guests: lifetime count per device and a daily safety cap per connection (both hashed by the server; no IPs stored).
create table if not exists public.assistant_guest_device (
  h      text primary key,
  total  integer not null default 0
);
create table if not exists public.assistant_guest_ip (
  h      text not null,
  day    date not null default (now() at time zone 'utc')::date,
  count  integer not null default 0,
  primary key (h, day)
);
alter table public.assistant_guest_device enable row level security;
alter table public.assistant_guest_ip enable row level security;
drop function if exists public.assistant_bump_guest(text);
drop function if exists public.assistant_bump_guest(text, text);
drop table if exists public.assistant_guest;
create function public.assistant_bump_guest(dev text, ip text)
returns json language plpgsql security definer set search_path = public as $$
declare a integer; b integer;
begin
  if dev is null or length(dev) < 32 or ip is null or length(ip) < 32 then raise exception 'bad key'; end if;
  insert into public.assistant_guest_device (h, total) values (dev, 1)
    on conflict (h) do update set total = public.assistant_guest_device.total + 1 returning total into a;
  insert into public.assistant_guest_ip (h, day, count) values (ip, (now() at time zone 'utc')::date, 1)
    on conflict (h, day) do update set count = public.assistant_guest_ip.count + 1 returning count into b;
  delete from public.assistant_guest_ip where day < (now() at time zone 'utc')::date - 2;
  return json_build_object('device', a, 'ip_today', b);
end;
$$;
revoke all on function public.assistant_bump_guest(text, text) from public;
grant execute on function public.assistant_bump_guest(text, text) to anon, authenticated;
