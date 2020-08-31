import os

SLEEP_INTERVAL = 7 # 1 minute(s)

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

WEBHOOK_URL = "https://hooks.slack.com/services/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"

BLACKLIST_WORDS = ['certificate', 't-shirt', 'tote bag', 'nse tropicals', 'tetrasperma', 
                    'obliqua','titanum', 'anthurium gracile','rhaphidophora decursiva',
                    'makoyana','ficus triangularis','spagmoss','birkin','philodendron grazielae',
                    'silver dragon','thaumatophyllum','alocasia maharani']
WHITELIST_WORDS = ['monstera deliciosa', 'verrucosum', 'squamiferum', 'plowmanii', 
                    'pastazanum', 'nangaritense','melanochrysum','hastatum','gloriosum',
                    'giganteum', 'fibrosum','69686','pink princess','florida ghost',
                    'el choco red','fantasy', 'monstera albo','monstera deliciosa area',
                    'warocqueanum','veitchii','magnificum','crystallinum','pendulifolium',
                    'forgetii','selby','pictum tri color', 'ficus triangularis']

LOGEES_SEARCH = ["https://www.logees.com/alocasia-frydek-alocasia-micholitziana-frydek.html",
                "https://www.logees.com/variegated-arrowhead-vine-syngonium-podophyllum-albo-variegatum.html",
                "https://www.logees.com/variegated-mexican-breadfruit-monstera-deliciosa-variegata.html",
                "https://www.logees.com/philodendron-pink-princess-philodendron-erubescens.html",
                "https://www.logees.com/black-gold-philodendron-philodendron-melanochrysum-2181.html"]

GABRIELLA_SEARCH = ["https://www.gabriellaplants.com/collections/popular/products/4-rhaphidophora-tetrasperma",
                    "https://www.gabriellaplants.com/collections/home-page/products/4-alocasia-serendipity",
                    "https://www.gabriellaplants.com/collections/philodendron/products/4-pink-princess-philodendron",
                    "https://www.gabriellaplants.com/products/6-burgundy-princess-1",
                    "https://www.gabriellaplants.com/products/4-burgundy-princess",
                    "https://www.gabriellaplants.com/products/5-philodendron-burgundy-princess",
                    "https://www.gabriellaplants.com/products/4-variegated-nepthytis-emerald-gem-green-variegation",
                    "https://www.gabriellaplants.com/products/4-jessenia-pothos",
                    "https://www.gabriellaplants.com/products/4-gabby-philodendron-sport",
                    "https://www.gabriellaplants.com/products/4-variegated-emerald-gem-syngonium-arrow-head-house-plant-nephthytis",
                    "https://www.gabriellaplants.com/products/3-philodendron-rio",
                    "https://www.gabriellaplants.com/products/rio-philodendron-4-original-consistent-collectors-version-of-brasil-philodendron-silver-variegation",
                    "https://www.gabriellaplants.com/products/3-scindapsus-treubii-moonlight",
                    "https://www.gabriellaplants.com/products/4-scindapsus-treubii-moonlight"]