-- =====================================================================
-- Chordseed · database schema for Supabase
-- Paste everything into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once.
-- =====================================================================

-- 1) Subscription status per user. Only the server (Paddle webhook) can change it.
create table if not exists public.subscriptions (
  user_id                 uuid primary key references auth.users(id) on delete cascade,
  plan                    text not null default 'free' check (plan in ('free','pro')),
  status                  text not null default 'none',      -- none | trialing | active | past_due | canceled
  current_period_end      timestamptz,
  paddle_customer_id      text,
  paddle_subscription_id  text,
  updated_at              timestamptz not null default now()
);

-- 2) Everything the app keeps for a user, as one synced document.
create table if not exists public.user_data (
  user_id     uuid primary key default auth.uid() references auth.users(id) on delete cascade,
  saved       jsonb not null default '[]'::jsonb,   -- saved progressions
  songs       jsonb not null default '[]'::jsonb,   -- full songs (parts + order) · Pro
  learn       jsonb not null default '{}'::jsonb,   -- lessons passed
  prefs       jsonb not null default '{}'::jsonb,   -- instrument, style, language…
  updated_at  timestamptz not null default now()
);

alter table public.subscriptions enable row level security;
alter table public.user_data     enable row level security;

-- 3) Is this user Pro right now?
create or replace function public.is_pro(uid uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.subscriptions s
    where s.user_id = uid and s.plan = 'pro'
      and s.status in ('active','trialing','past_due')
      and (s.current_period_end is null or s.current_period_end > now())
  );
$$;

-- 4) Row Level Security: each user only sees and edits their own rows.
drop policy if exists "own subscription" on public.subscriptions;
create policy "own subscription" on public.subscriptions
  for select to authenticated using (user_id = auth.uid());

drop policy if exists "read own data"   on public.user_data;
drop policy if exists "insert own data" on public.user_data;
drop policy if exists "update own data" on public.user_data;
create policy "read own data"   on public.user_data for select to authenticated using (user_id = auth.uid());
create policy "insert own data" on public.user_data for insert to authenticated with check (user_id = auth.uid());
create policy "update own data" on public.user_data for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());

-- 5) Table permissions for the Data API (automatic exposure is off).
grant usage on schema public to authenticated;
grant select on public.subscriptions to authenticated;
grant select, insert, update on public.user_data to authenticated;
grant execute on function public.is_pro(uuid) to authenticated;

-- 6) Free-plan limits enforced on the server (cannot be bypassed from the browser).
create or replace function public.enforce_plan_limits()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  new.updated_at := now();
  if not public.is_pro(new.user_id) then
    if jsonb_array_length(coalesce(new.saved, '[]'::jsonb)) > 5 then
      raise exception 'FREE_LIMIT_SAVED' using hint = 'Free plan keeps up to 5 progressions.';
    end if;
    if jsonb_array_length(coalesce(new.songs, '[]'::jsonb)) > 0 then
      if tg_op = 'INSERT' then
        raise exception 'PRO_ONLY_SONGS' using hint = 'Saving full songs to the cloud is part of Pro.';
      elsif new.songs is distinct from old.songs then
        raise exception 'PRO_ONLY_SONGS' using hint = 'Saving full songs to the cloud is part of Pro.';
      end if;
    end if;
  end if;
  return new;
end;
$$;

drop trigger if exists user_data_limits on public.user_data;
create trigger user_data_limits before insert or update on public.user_data
  for each row execute function public.enforce_plan_limits();

-- 7) When someone signs up, create their rows automatically.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.subscriptions (user_id) values (new.id) on conflict do nothing;
  insert into public.user_data (user_id)     values (new.id) on conflict do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- 8) Users who signed up before this script ran also get their rows.
insert into public.subscriptions (user_id) select id from auth.users on conflict do nothing;
insert into public.user_data (user_id)     select id from auth.users on conflict do nothing;
