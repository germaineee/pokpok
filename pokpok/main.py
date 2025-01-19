import pygame
import sys
from entities import *
import random 

pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Help Bok Reunite with His Family")

def main_menu():
    background_image = pygame.image.load("assets/main_bg.png")

    while True:
        mouse_position = pygame.mouse.get_pos()

        window.blit(background_image, (0, 0))

        mainmenu_text = pygame.font.Font(None, 36).render("MAIN MENU", True, (255, 255, 255))

        mainmenu_rect = mainmenu_text.get_rect(center=(400, 300))

        PLAY_BUTTON = Button(400, 350, "PLAY GAME")

        CONTROL_BUTTON = Button(400, 400, "CONTROLS")

        window.blit(mainmenu_text, mainmenu_rect)

        for button in [PLAY_BUTTON, CONTROL_BUTTON]:
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_position):
                    play()
                if CONTROL_BUTTON.checkForInput(mouse_position):
                    controls()
        
        pygame.display.update()

def play():
    bok_image = pygame.transform.scale(pygame.image.load("assets/bok.png"), (32, 32))
    cucumber_image = pygame.transform.scale(pygame.image.load("assets/cucumber.png"), (32, 32))
    rice_image = pygame.transform.scale(pygame.image.load("assets/rice.png"), (32, 32))
    drumstick_image = pygame.transform.scale(pygame.image.load("assets/drumstick.png"), (32, 32))
    bin_image = pygame.transform.scale(pygame.image.load("assets/bin.png"), (64, 64))
    fire_image = pygame.transform.scale(pygame.image.load("assets/fire.png"), (64, 64))
    mushroom_image = pygame.transform.scale(pygame.image.load("assets/mushroom.png"), (32, 32))
    mario_image = pygame.transform.scale(pygame.image.load("assets/mario.png"), (50, 50))
    chickenrice_image = pygame.transform.scale(pygame.image.load("assets/chicken_rice.png"), (64, 64))
    kfc_image = pygame.transform.scale(pygame.image.load("assets/kfc.png"), (50, 50))
    ghost_image= pygame.transform.scale(pygame.image.load("assets/ghost.png"), (64, 64))
    pill_image = pygame.transform.scale(pygame.image.load("assets/pill.png"), (50, 50))

    # Create characters and items 
    main_char = Bok(10, 10, bok_image)
    ghost = Ghost(790, 590, ghost_image)

    items = []

    for _ in range(3):
        x, y = random.randint(0, WIDTH - cucumber_image.get_width()), random.randint(0, 500 - cucumber_image.get_height())
        items.append(Cucumber(x, y, cucumber_image))

    for _ in range(2):
        x, y = random.randint(0, WIDTH - rice_image.get_width()), random.randint(0, 500 - rice_image.get_height())
        items.append(Rice(x, y, rice_image))

    for _ in range(2):
        x, y = random.randint(0, WIDTH - mushroom_image.get_width()), random.randint(0, 500 - mushroom_image.get_height())
        items.append(Mushroom(x, y, mushroom_image))

    x, y = random.randint(0, WIDTH - drumstick_image.get_width()), random.randint(0, 500 - drumstick_image.get_height())
    items.append(Drumstick(x, y, drumstick_image))

    bin = Bin(WIDTH - bin_image.get_width() - 10, 500 - bin_image.get_height() - 10, bin_image)
    items.append(bin)

    items.append(Fire((WIDTH -fire_image.get_width()) // 2, (500 - fire_image.get_height()) // 2, fire_image))

    clock = pygame.time.Clock()
    running = True
    bin_collision = False
    fire_collision = False

    # Set up game loop 
    thrown = 0 

    game_over = False
    die = 0
  
    while running: 
        clock.tick(90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if bin_collision:
                    if event.key == pygame.K_a:
                        main_char.inventory.cycle_inventory(-1)
                    if event.key == pygame.K_d:
                        main_char.inventory.cycle_inventory(1)
                    if event.key == pygame.K_SPACE:
                        if main_char.inventory.items and thrown == 0:
                            selected_item = main_char.inventory.items[main_char.inventory.selected_item_index]
                            main_char.inventory.remove_item(selected_item)
                            # print(f"Threw {selected_item} into the bin!")
                            thrown = 1
                            if isinstance(selected_item, Cucumber):
                                x, y = random.randint(0, WIDTH - cucumber_image.get_width()), random.randint(0, 500 - cucumber_image.get_height())
                                items.append(Cucumber(x ,y , cucumber_image))
                            if isinstance(selected_item, Mushroom):
                                x, y = random.randint(0, WIDTH - mushroom_image.get_width()), random.randint(0, 500 - mushroom_image.get_height())
                                items.append(Mushroom(x ,y , mushroom_image))
                            if isinstance(selected_item, Rice):
                                x, y = random.randint(0, WIDTH - rice_image.get_width()), random.randint(0, 500 - rice_image.get_height())
                                items.append(Rice(x ,y , rice_image))
                            if isinstance(selected_item, Drumstick):
                                x, y = random.randint(0, WIDTH - drumstick_image.get_width()), random.randint(0, 500 - drumstick_image.get_height())
                                items.append(Drumstick(x ,y , drumstick_image))
                            if (not main_char.inventory.items) or (main_char.inventory.selected_item_index == 0):
                                main_char.inventory.selected_item_index = 0
                            else:
                                main_char.inventory.selected_item_index -= 1
                        else:
                            print("No items to throw!")
                            main_char.inventory.message = "No items to throw!"
                            main_char.inventory.message_timer = 200
                if fire_collision:
                    if event.key == pygame.K_c:
                        if main_char.inventory.items:
                            # Check for mushroom
                            if any(isinstance(item, Mushroom) for item in main_char.inventory.items):
                                mario = Mario(main_char.x, main_char.y, mario_image)
                                mario.inventory = main_char.inventory
                                main_char = mario
                                x, y = random.randint(0, WIDTH - pill_image.get_width()), random.randint(0, 500 - pill_image.get_height())
                                items.append(Pill(x, y, pill_image))
                                
                            # Check if Main Character has all ingredients for chicken rice
                            elif isinstance(main_char, Bok) and any(isinstance(item, Cucumber) for item in main_char.inventory.items) and any(isinstance(item, Rice) for item in main_char.inventory.items) and any(isinstance(item, Drumstick) for item in main_char.inventory.items):
                                for item in main_char.inventory.items:
                                    if isinstance(item, Cucumber):
                                        main_char.inventory.items.remove(item)
                                        break
                                for item in main_char.inventory.items:
                                    if isinstance(item, Rice):
                                        main_char.inventory.items.remove(item)
                                        break
                                for item in main_char.inventory.items:
                                    if isinstance(item, Drumstick):
                                        main_char.inventory.items.remove(item)
                                        break
                                items.append(ChickenRice(400, 300, chickenrice_image))
                if event.key == pygame.K_p:
                    pause()
                    
            pygame.display.update()


                    
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_SPACE) and (thrown == 1):
                    thrown = 0


        # Move 
        if not game_over:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT]:
                dx = -2
            if keys[pygame.K_RIGHT]:
                dx = 2
            if keys[pygame.K_UP]:
                dy = -2
            if keys[pygame.K_DOWN]:
                dy = 2

            main_char.move(dx, dy)
            ghost.move()

        else:
            over()
            running = False

        bin_collision = False

        # Check for collisions with items
        for item in items[:]: # Create shallow copy so removing does not affect loop
            if check_collision(main_char, item) and main_char.inventory:
                if isinstance(item, Bin):
                    bin_collision = True

                if isinstance(item, Fire):
                    fire_collision = True
                    
                if isinstance(item, Fire) or isinstance(item, Bin):
                    continue # Don't pick up if fire or bin

                elif main_char.inventory.add_item(item):
                    items.remove(item)

                if isinstance(item, ChickenRice) and not isinstance(main_char, Mario): # Don't let Mario craft things
                    kfc = KFC(main_char.x, main_char.y, kfc_image)
                    main_char.inventory.remove_item(item)
                    kfc.inventory = main_char.inventory
                    main_char = kfc

                if isinstance(item, Pill) and isinstance(main_char, Mario):
                    bok = Bok(main_char.x, main_char.y, bok_image)
                    main_char.inventory.remove_item(item)
                    bok.inventory = main_char.inventory
                    main_char = bok

        if check_collision(main_char, ghost) and die == 0:
            game_over = True
            die = 1
          
        # Render game screen   
        window.fill((193, 208, 244))
        main_char.draw(window)
        for item in items:
            item.draw(window)

        ghost.draw(window)
            
                
        pygame.display.update()

def controls():
    window.fill((115, 194, 251))

    up_arrow = pygame.transform.scale(pygame.image.load("assets/up.png"), (40, 40))
    down_arrow = pygame.transform.scale(pygame.image.load("assets/down.png"), (40, 40))
    left_arrow = pygame.transform.scale(pygame.image.load("assets/left.png"), (40, 40))
    right_arrow = pygame.transform.scale(pygame.image.load("assets/right.png"), (40, 40))
    a_key = pygame.transform.scale(pygame.image.load("assets/a.png"), (40, 40))
    d_key = pygame.transform.scale(pygame.image.load("assets/d.png"), (40, 40))
    c_key = pygame.transform.scale(pygame.image.load("assets/c.png"), (40, 40))
    spacebar = pygame.transform.scale(pygame.image.load("assets/spacebar.png"), (125, 125))

    while True:
        mouse_position = pygame.mouse.get_pos()

        # Show CONTROL header text on page
        controls_text = pygame.font.Font(None, 36).render("CONTROLS", True, (255, 255, 255))
        controls_rect = controls_text.get_rect(center=(400, 50))
        window.blit(controls_text, controls_rect)

        CONTROLS_BACK = Button(45, 20, "BACK")
        CONTROLS_BACK.update(window)

        # Render "move using arrows"
        move_text = pygame.font.Font(None, 28).render("Move Up, Down, Left, Right", True, (255, 255, 255))
        move_rect = move_text.get_rect(center=(475, 150))
        window.blit(move_text, move_rect)

        window.blit(up_arrow, (225, 100)) 
        window.blit(left_arrow, (175, 150)) 
        window.blit(down_arrow, (225, 150)) 
        window.blit(right_arrow, (275, 150))

        # Render "Select items"
        select_text = pygame.font.Font(None, 28).render("Select Items Left or Right at Bin", True, (255, 255, 255))
        select_rect = select_text.get_rect(center=(475, 270))
        window.blit(select_text, select_rect)

        window.blit(a_key, (250, 250)) 
        window.blit(d_key, (200, 250)) 

        # Render "Craft items"
        craft_text = pygame.font.Font(None, 28).render("Craft Items at Fireplace", True, (255, 255, 255))
        craft_rect = craft_text.get_rect(center=(450, 380))
        window.blit(craft_text, craft_rect)

        window.blit(c_key, (225, 360)) 
        
        # Render "Discard items"
        discard_text = pygame.font.Font(None, 28).render("Discard Item at Bin", True, (255, 255, 255))
        discard_rect = discard_text.get_rect(center=(450, 490))
        window.blit(discard_text, discard_rect)

        window.blit(spacebar, (185, 430))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTROLS_BACK.checkForInput(mouse_position):
                    main_menu()
        
        pygame.display.update()

def over():
    window.fill((0, 0, 0))

    while True:
        over_text = pygame.font.Font(None, 36).render("Game Over", True, (255, 255, 255))
        restart_text = pygame.font.Font(None, 28).render("Press Enter to Restart", True, (255, 255, 255))
        window.blit(over_text, (340, 200))
        window.blit(restart_text, (300, 250))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                play()
                return
            

def pause():

    resume_button_rect = pygame.Rect(300, 250, 200, 50)  # Position and size of "Resume" button
    restart_button_rect = pygame.Rect(300, 350, 200, 50)  # Position and size of "Restart" button

    while True:
        mouse_position = pygame.mouse.get_pos()
        window.fill((0, 0, 0))
        pause_text = pygame.font.Font(None, 28).render("GAME PAUSED", True, (255, 255, 255))
        window.blit(pause_text, (325, 200))
        RESUME_BUTTON = Button(400, 250, "RESUME GAME")

        RESTART_BUTTON = Button(400, 400, "RESTART GAME")

        for button in [RESUME_BUTTON, RESTART_BUTTON]:
            button.update(window)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(mouse_position):
                    return
                if RESTART_BUTTON.checkForInput(mouse_position):
                    play()
        
main_menu()