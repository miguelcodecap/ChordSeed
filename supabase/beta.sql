-- Chordseed public beta: every signed-in user gets Pro free until paid plans launch.
-- (Already applied to the project on 2026-11-09.)
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.subscriptions (user_id, plan, status, current_period_end)
    values (new.id, 'pro', 'trialing', '2027-03-01') on conflict do nothing;
  insert into public.user_data (user_id) values (new.id) on conflict do nothing;
  return new;
end;
$$;
update public.subscriptions set plan = 'pro', status = 'trialing', current_period_end = '2027-03-01'
  where plan = 'free' and paddle_subscription_id is null;

-- To END the beta (when Paddle goes live), run:
-- update public.subscriptions set plan='free', status='none', current_period_end=null
--   where status='trialing' and paddle_subscription_id is null;
-- and restore handle_new_user() from schema.sql.
