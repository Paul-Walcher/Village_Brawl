import assets.ascii_assets as ascii_assets
import terminal_functions as terminal
import colorama

colorama.init()

terminal.clear()
print(ascii_assets.Village_Brawl_Headline)

terminal.text_rgb(255, 0, 0)
terminal.print_centered(ascii_assets.Village_Brawl_Headline)
terminal.color_reset()
print("\n"*5)
text = terminal.image_to_ascii(r"C:\Users\pycpp\OneDrive\Dokumente\MEGA\Village_Brawl\V1.0.0\Assets\Wood.png", 100)
print(text)
text = terminal.image_to_ascii(r"C:\Users\pycpp\OneDrive\Dokumente\MEGA\Village_Brawl\V1.0.0\Assets\Coin.png", 100)
terminal.print_centered(text, full=True)
