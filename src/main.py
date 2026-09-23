
"""
Village Brawl
"""

import assets.ascii_assets as ascii_assets
import terminal_functions as terminal

terminal.clear()
print(ascii_assets.Village_Brawl_Headline)
print("\n"*5)
text = terminal.image_to_ascii(r"C:\Users\pycpp\OneDrive\Dokumente\MEGA\Village_Brawl\V1.0.0\Assets\Wood.png", 100)
print(text)
