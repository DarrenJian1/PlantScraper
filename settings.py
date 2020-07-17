import os

SLEEP_INTERVAL = 60 # 1 minute(s)

BLACKLIST_WORDS = ['certificate', 't-shirt', 'tote bag', 'nse tropicals', 'tetrasperma', 
                    'obliqua','titanum', 'anthurium gracile','rhaphidophora decursiva']
WHITELIST_WORDS = ['monstera deliciosa', 'verrucosum', 'squamiferum', 'plowmanii', 
                    'pastazanum', 'nangaritense','melanochrysum','hastatum','gloriosum',
                    'giganteum', 'fibrosum','69686','pink princess','florida ghost',
                    'el choco red','fantasy', 'monstera albo','monstera deliciosa area',
                    'warocqueanum','veitchii','magnificum','crystallinum','pendulifolium',
                    'forgetii','selby','pictum tri color', 'ficus triangularis']

LOGEES_SEARCH = ["https://www.logees.com/variegated-arrowhead-vine-syngonium-podophyllum-albo-variegatum.html",
                "https://www.logees.com/variegated-mexican-breadfruit-monstera-deliciosa-variegata.html",
                "https://www.logees.com/philodendron-pink-princess-philodendron-erubescens.html",
                "https://www.logees.com/mini-monstera-monstera-minima-4-inch.html"]

GABRIELLA_SEARCH = ["https://www.gabriellaplants.com/collections/philodendron/products/4-pink-princess-philodendron",
                    "https://www.gabriellaplants.com/products/4-variegated-nepthytis-emerald-gem-green-variegation",
                    "https://www.gabriellaplants.com/products/4-jessenia-pothos",
                    "https://www.gabriellaplants.com/collections/philodendron/products/4-gabby-philodendron-sport",
                    "https://www.gabriellaplants.com/collections/growing/products/4-variegated-emerald-gem-syngonium-arrow-head-house-plant-nephthytis",
                    "https://www.gabriellaplants.com/collections/growing/products/3-philodendron-rio",
                    "https://www.gabriellaplants.com/products/rio-philodendron-4-original-consistent-collectors-version-of-brasil-philodendron-silver-variegation",
                    "https://www.gabriellaplants.com/collections/home-page/products/4-white-butterfly-syngonium"]