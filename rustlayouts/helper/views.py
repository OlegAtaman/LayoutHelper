from django.shortcuts import render
from PIL import Image
from django.http import JsonResponse
from django.templatetags.static import static

def mainpage(request):
    args_dirty = request.GET.dict()
    ctx = {'get_args':args_dirty}
    return render(request, 'helper/mainpage.html', ctx)

# Load PNG and create a binary mask
def load_image_as_mask(image_path):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    mask = []

    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = image.getpixel((x, y))  # a is the alpha channel (transparency)
            if a > 0:  # Non-transparent pixel
                row.append(1)
            else:
                row.append(0)
        mask.append(row)

    return mask, width, height

# Check if an item can be placed at (x_offset, y_offset) without overlapping walls or other items
def can_place_item(canvas_mask, item_mask, x_offset, y_offset, canvas_width, canvas_height):
    for y in range(len(item_mask)):
        for x in range(len(item_mask[y])):
            if item_mask[y][x] == 1:  # Only check non-transparent pixels
                if (y + y_offset >= canvas_height) or (x + x_offset >= canvas_width):
                    return False  # Out of bounds
                if canvas_mask[y + y_offset][x + x_offset] == 1:
                    return False  # Collision with existing item or wall
    return True

# Place item on the canvas by modifying the canvas mask
def place_item_on_canvas(canvas_mask, item_mask, x_offset, y_offset):
    for y in range(len(item_mask)):
        for x in range(len(item_mask[y])):
            if item_mask[y][x] == 1:
                canvas_mask[y + y_offset][x + x_offset] = 1  # Mark this space as occupied

def calculate_placement(request):
    # Initialize a blank canvas (400x400), filled with 0s (empty)
    canvas_width, canvas_height = 400, 400
    canvas_mask = [[0 for _ in range(canvas_width)] for _ in range(canvas_height)]

    # Predefine wall areas on the canvas (you could improve this by handling walls dynamically)
    walls = ['top_wall', 'left_wall', 'right_wall', 'bottom_wall']
    for wall in walls:
        wall_image = 'static/textures/metal_wall.png'  # Dynamically select based on user choice
        wall_mask, w_width, w_height = load_image_as_mask(wall_image)
        # Position walls on canvas based on their respective sides (e.g., top, left, etc.)

    # Get the items selected by the user and load them as masks
    items = request.GET.getlist('items[]')
    placed_items = []
    for item in items:
        item_image = 'static/textures/' + item + '.png'
        item_mask, item_width, item_height = load_image_as_mask(item_image)

        # Try to place the item on the canvas (greedy algorithm)
        placed = False
        for y in range(canvas_height):
            for x in range(canvas_width):
                if can_place_item(canvas_mask, item_mask, x, y, canvas_width, canvas_height):
                    place_item_on_canvas(canvas_mask, item_mask, x, y)
                    placed_items.append({
                        'item': item,
                        'x': x,
                        'y': y,
                        'width': item_width,
                        'height': item_height
                    })
                    placed = True
                    break
            if placed:
                break

    return JsonResponse({'placed_items': placed_items})
