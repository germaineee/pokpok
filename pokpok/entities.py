import pygame 
import random

class MainCharacter: 
    def __init__(self, x, y, image): 
        self.x = x 
        self.y = y 
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.inventory = Inventory(250, 500, 64, 5)

    def move(self, dx, dy): 
        self.x += dx 
        self.y += dy

        if self.x < 0: 
            self.x = 0  
        if self.y < 0: 
            self.y = 0
        if self.x > 800 - self.width: 
            self.x = 800 - self.width
        if self.y > 500 - self.height:
            self.y = 500 - self.height
    
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        self.inventory.draw(window)

class Bok(MainCharacter):
    pass

class Mario(MainCharacter):
    pass

class KFC(MainCharacter):
    pass

class Ghost:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.speed = 1 # The speed of the ghost
        self.direction = random.choice([(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)])
        self.timer = 60 

    def move(self):
        # Random movement (up, down, left, right)
        dx, dy = self.direction
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Keep the ghost within bounds of the window
        if self.x < 0: 
            self.x = 0  
        if self.y < 0: 
            self.y = 0
        if self.x > 800 - self.width: 
            self.x = 800 - self.width
        if self.y > 500 - self.height:
            self.y = 500 - self.height

        self.timer -= 1
        if self.timer < 0:
            self.direction = random.choice([(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)])
            self.timer = 60

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class Mario(MainCharacter):
    pass

class Item:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()


    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
   
class Bone(Item):
    pass

class Cucumber(Item):
    def __str__(self):
        return "Cucumber"

class Fire(Item):
    def __str__(self):
        return "Fire"

class Mushroom(Item):
    def __str__(self):
        return "Mushroom"

class Drumstick(Item):
    def __str__(self):
        return "Drumstick"

class Egg(Item):
    def __str__(self):
        return "Egg"

class Fish(Item):
    def __str__(self):
        return "Fish"

class Rice(Item):
    def __str__(self):
        return "Rice"

class Bin(Item):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.message = ""
        self.message_timer = 0

class ChickenRice(Item):
    def __str__(self):
        return "Chicken Rice"
    
class Pill(Item):
    def __str__(self):
        return "Pill"

class Inventory:
    def __init__(self, x, y, slot_size, max_slots):
        self.x = x
        self.y = y
        self.slot_size = slot_size
        self.max_slots = max_slots
        self.items = []
        self.message = ""
        self.message_timer = 0
        self.selected_item_index = 0

    def add_item(self, item):
        if len(self.items) < self.max_slots:
            self.items.append(item)
            return True
        else:
            self.message = "Inventory full!"
            self.message_timer = 500
            return False
        

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.message = f"Removed {item} from inventory!"
            self.message_timer = 200
        else: 
            self.message = "Item not found!"
            self.message_timer = 200

    def cycle_inventory(self, direction):
        # This method cycles through the inventory, either forwards or backwards
        if len(self.items) == 0:  # Accessing items in inventory
            return  # No inventory to cycle
        self.selected_item_index += direction
        # Wrap around the index if it goes out of bounds
        if self.selected_item_index < 0:
            self.selected_item_index = 0
        elif self.selected_item_index >= len(self.items):
            self.selected_item_index = len(self.items) - 1

    def draw(self, window):
        for i in range(self.max_slots):
            slot_x = self.x + (i * self.slot_size)
            slot_y = self.y

            # Draw slot background 
            pygame.draw.rect(window, (255, 255, 255), (slot_x, slot_y, self.slot_size, self.slot_size), 2)

        # Draw empty slots
        for i, item in enumerate(self.items):
            if i >= self.max_slots:
                break 
            slot_x = self.x + (i * self.slot_size)
            slot_y = self.y

            # Draw item
            if item.image:
                item_rect = item.image.get_rect(center=(slot_x + self.slot_size // 2, slot_y + self.slot_size // 2))
                window.blit(item.image, item_rect)
            if i == self.selected_item_index:
                pygame.draw.rect(window, (255, 255, 0), (slot_x, slot_y, self.slot_size, self.slot_size), 4)
            
            # Display message
            if self.message_timer > 0:
                font = pygame.font.Font(None, 36)
                message = font.render(self.message, True, (255, 8, 0))
                text_rect = message.get_rect(center=(400, 470))
                window.blit(message, text_rect)
                self.message_timer -= 1

class Button():
    def __init__(self, x, y, text_input):
        self.x = x
        self.y = y
        self.text_input = text_input
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(self.text_input, True, (255, 25, 255))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))  # Center the text
        self.rect = pygame.Rect(
            self.text_rect.x, self.text_rect.y, self.text_rect.width, self.text_rect.height
        )  # Rectangle for hitbox

    def update(self, window):
        window.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom) :

            return True

        return False

def check_collision(bok, item):
    bok_rect = pygame.Rect(bok.x, bok.y, bok.width, bok.height)
    item_rect = pygame.Rect(item.x, item.y, item.width, item.height)
    return bok_rect.colliderect(item_rect)

def check_collision(bok, ghost):
        # Check if the ghost collides with Bok (the chicken)
        ghost_rect = pygame.Rect(ghost.x, ghost.y, ghost.width, ghost.height)
        bok_rect = pygame.Rect(bok.x, bok.y, bok.width, bok.height)
        return ghost_rect.colliderect(bok_rect)
