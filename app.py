import streamlit as st
from supabase import create_client

# 1. Setup connection credentials
SUPABASE_URL = "https://yxdnobocoxrchfsxdyen.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4ZG5vYm9jb3hyY2hmc3hkeWVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIwMDU4NzcsImV4cCI6MjA5NzU4MTg3N30.U5EjJEUylm6P-k7xRmklPqZoUyp8_LBUnRByYyhnmUI"

# 2. Initialize database client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 3. App Title & UI elements
st.title("🚀 Model Experiment Tracker")
st.write("Log your local training runs directly into the cloud database.")

model_name = st.text_input("Model Name", "YOLOv8-v1")
accuracy = st.number_input("Validation Accuracy (%)", min_value=0.0, max_value=100.0, value=85.0)
notes = st.text_area("Experiment Notes", "Trained on local RTX 3050.")

# 4. Action button to send data
if st.button("Save Experiment"):
    data = {
        "model_name": model_name,
        "accuracy": accuracy,
        "notes": notes
    }
    try:
        response = supabase.table("experiments").insert(data).execute()
        st.success("✨ Successfully saved to Supabase cloud!")
    except Exception as e:
        st.error(f"❌ Failed to save: {e}")

# 5. Display existing data from the cloud
st.subheader("📊 Logged History")
try:
    response = supabase.table("experiments").select("*").execute()
    for row in response.data:
        st.write(f"- **{row['model_name']}**: {row['accuracy']}% | _ {row['notes']} _")
except Exception as e:
    st.write("Add your first experiment to see history here.")
