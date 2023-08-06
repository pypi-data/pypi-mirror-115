A basic Hypixel API wrapper

covering:
| /punishmentstats
| /key
| /player
| /resources/skyblock/skills
| /skyblock/auctions
| /skyblock/profile
| /friends
| /status
| /guild
| /counts

Quickstart
==========

1. Install hypy:
    .. code-block:: sh

        $ pip install hypy-hypixel
2. Create a Hypixel object::
    .. code-block:: py

        from hypy import Hypixel
        
        hypixel = Hypixel(api_key)
        await hypixel.setup()
    