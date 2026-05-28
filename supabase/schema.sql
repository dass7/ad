-- Create groups table
CREATE TABLE IF NOT EXISTS public.groups (
  id SERIAL PRIMARY KEY,
  group_number INTEGER NOT NULL UNIQUE,
  group_name TEXT NOT NULL,
  members TEXT DEFAULT '',
  project_name TEXT DEFAULT '',
  last_updated TIMESTAMPTZ DEFAULT NOW(),
  updated_by_name TEXT DEFAULT '',
  updated_by_avatar TEXT DEFAULT ''
);

-- Create edit_logs table
CREATE TABLE IF NOT EXISTS public.edit_logs (
  id SERIAL PRIMARY KEY,
  user_qq TEXT NOT NULL,
  user_name TEXT NOT NULL,
  user_avatar TEXT DEFAULT '',
  group_number INTEGER NOT NULL,
  field TEXT NOT NULL,
  old_value TEXT DEFAULT '',
  new_value TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert the 9 groups
INSERT INTO public.groups (group_number, group_name) VALUES
  (1, '第一组'), (2, '第二组'), (3, '第三组'),
  (4, '第四组'), (5, '第五组'), (6, '第六组'),
  (7, '第七组'), (8, '第八组'), (9, '第九组')
ON CONFLICT (group_number) DO NOTHING;

-- Enable Row Level Security
ALTER TABLE public.groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.edit_logs ENABLE ROW LEVEL SECURITY;

-- RLS Policies: allow all reads
CREATE POLICY "Allow public read on groups" ON public.groups
  FOR SELECT USING (true);

CREATE POLICY "Allow public update on groups" ON public.groups
  FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Allow public read on logs" ON public.edit_logs
  FOR SELECT USING (true);

CREATE POLICY "Allow public insert on logs" ON public.edit_logs
  FOR INSERT WITH CHECK (true);

-- Enable real-time
ALTER PUBLICATION supabase_realtime ADD TABLE public.groups;
