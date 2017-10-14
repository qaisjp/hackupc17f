from datetime import date

def get_hacks():
    return [
        {
            "name": "HackSheffield",
            "location": "Sheffield, South Yorkshire, UK",
            "begins": date(2017,10,14),
            "ends": date(2017,10,15),
            "website": "https://website.org"
        },

        {
            "name": "HackBudapest",
            "location": "Budapest, Hungary",
            "begins": date(2017, 10, 21),
            "ends": date(2017, 10, 22),
            "website": "https://website.org"
        },

        {
            "name": "Do You Have The GUTS",
            "location": "Glasgow, UK",
            "begins": date(2017, 10, 27),
            "ends": date(2017, 10, 29),
            "website": "https://website.org"
        }
    ]

