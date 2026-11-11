// =============================
// Supabase Configuration
// =============================

// Replace these with your own Supabase Project URL and Anon Key
const SUPABASE_URL = "https://yzgzcohxhybgpmjaszda.supabase.co";

const SUPABASE_ANON_KEY ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6Z3pjb2h4aHliZ3BtamFzemRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ2MTE2NTcsImV4cCI6MjEwMDE4NzY1N30.NHIs8hxXywWgTDkpb7PW86FX_4swazC6ziw02b-4WHE";

// Create Supabase Client
const supabase = window.supabase.createClient(
    SUPABASE_URL,
    SUPABASE_ANON_KEY
);

// Test Connection
console.log("Supabase Connected");
console.log(supabase);