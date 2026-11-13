-- Chordseed · Lumen assistant (Pro): daily message counter.
-- Paste into Supabase → SQL Editor → New query → Run. Safe to run more than once.

create table if not exists public.assistant_usage (
  user_id  uuid not null references auth.users(id) on delete cascade,
  day      date not null default (now() at time zone 'utc')::date,
  count    integer not null default 0,
  primary key (user_id, day)
);
alter table public.assistant_usage enable row level security;

drop policy if exists "read own assistant usage" on public.assistant_usage;
create policy "read own assistant usage" on public.assistant_usage
  for select using (auth.uid() = user_id);

-- Adds one message for the signed-in user today and returns today's total.
-- Called by the server (/api/assistant) with the user's own login token.
create or replace function public.assistant_bump()
returns integer language plpgsql security definer set search_path = public as $$
declare n integer;
begin
  if auth.uid() is null then raise exception 'not signed in'; end if;
  insert into public.assistant_usage (user_id, day, count)
    values (auth.uid(), (now() at time zone 'utc')::date, 1)
  on conflict (user_id, day) do update set count = public.assistant_usage.count + 1
  returning count into n;
  return n;
end;
$$;
revoke all on function public.assistant_bump() from public, anon;
grant execute on function public.assistant_bump() to authenticated;
