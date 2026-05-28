-- ============================================================
--  组队报名表 · Supabase 数据库初始化脚本
--  在 Supabase Dashboard → SQL Editor 里粘贴运行
-- ============================================================

-- 1. 创建表
CREATE TABLE IF NOT EXISTS public.groups (
  id            INTEGER       PRIMARY KEY,
  members       TEXT          NOT NULL DEFAULT '',
  project       TEXT          NOT NULL DEFAULT '',
  last_editor   TEXT          NOT NULL DEFAULT '',
  last_modified TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- 2. 插入9个固定组（已存在则跳过）
INSERT INTO public.groups (id) VALUES
  (1),(2),(3),(4),(5),(6),(7),(8),(9)
ON CONFLICT (id) DO NOTHING;

-- 3. 开启行级安全（RLS）
ALTER TABLE public.groups ENABLE ROW LEVEL SECURITY;

-- 4. 任何人可读
CREATE POLICY "public_select"
  ON public.groups FOR SELECT
  USING (true);

-- 5. 任何人可更新（学生填表场景，不需要鉴权）
CREATE POLICY "public_update"
  ON public.groups FOR UPDATE
  USING (true)
  WITH CHECK (true);

-- 6. 开启 Realtime（让多人实时同步）
ALTER PUBLICATION supabase_realtime ADD TABLE public.groups;
