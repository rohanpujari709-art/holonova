from supabase import create_client, Client


SUPABASE_URL = "https://yzgzcohxhybgpmjaszda.supabase.co"

SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6Z3pjb2h4aHliZ3BtamFzemRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ2MTE2NTcsImV4cCI6MjEwMDE4NzY1N30.NHIs8hxXywWgTDkpb7PW86FX_4swazC6ziw02b-4WHE"


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_ANON_KEY
)