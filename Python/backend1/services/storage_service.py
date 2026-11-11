from database.supabase_client import supabase



def save_hologram(
    image_name,
    rgb_data,
    width,
    height
):

    # Insert hologram metadata
    hologram = (
        supabase
        .table("holograms")
        .insert({
            "image_name": image_name,
            "width": width,
            "height": height,
            "total_frames": 1,
            "status": "completed"
        })
        .execute()
    )


    hologram_id = hologram.data[0]["id"]


    # Insert LED frame data
    (
        supabase
        .table("led_frames")
        .insert({
            "hologram_id": hologram_id,
            "frame_number": 1,
            "led_data": rgb_data
        })
        .execute()
    )


    return hologram_id




# Dashboard data
def get_dashboard_stats():

    result = (
        supabase
        .table("holograms")
        .select("*")
        .execute()
    )


    total = len(result.data)


    return {
        "total_holograms": total,
        "total_uploads": total,
        "cloud_storage": "Supabase",
        "esp32_status": "Offline"
    }





def get_all_holograms():

    result = (
        supabase
        .table("holograms")
        .select("*")
        .execute()
    )


    return result.data





def get_led_frames(hologram_id):

    result = (
        supabase
        .table("led_frames")
        .select("*")
        .eq("hologram_id", hologram_id)
        .execute()
    )


    return result.data





def get_hologram_details(hologram_id):

    hologram = (
        supabase
        .table("holograms")
        .select("*")
        .eq("id", hologram_id)
        .execute()
    )


    frames = (
        supabase
        .table("led_frames")
        .select("*")
        .eq("hologram_id", hologram_id)
        .execute()
    )


    return {
        "hologram": hologram.data[0] if hologram.data else None,
        "frames": frames.data
    }
def delete_hologram(hologram_id):

    # delete LED frames first
    supabase.table("led_frames")\
        .delete()\
        .eq("hologram_id", hologram_id)\
        .execute()


    # delete hologram record
    result = (
        supabase
        .table("holograms")
        .delete()
        .eq("id", hologram_id)
        .execute()
    )

    return result.data