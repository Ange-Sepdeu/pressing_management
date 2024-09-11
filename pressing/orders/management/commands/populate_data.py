from django.core.management.base import BaseCommand
from orders.models import Region, Town, Quarter

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        self.populate()

    def populate(self):
        data = {
            "Adamawa Region": {
                "towns": ["Ngaoundéré", "Yako", "Tibati", "Belel"],
                "quarters": [
                    "Mbéré", "Mbidou", "Njaména", "N'Djom", "N'Kongsamba", 
                    "N'Koutou", "N'Koung", "N'Kongsamba-Ville"
                ]
            },
            "Centre Region": {
                "towns": ["Yaoundé", "Mbalmayo", "Mfou", "Obala"],
                "quarters": [
                    "Bastos", "Essos", "Etoudi", "Mvog-Mbi", "Tsinga", 
                    "Nkol-Eton", "Nkol-Ndongo", "Nkol-N'Doung"
                ]
            },
            "East Region": {
                "towns": ["Bertoua", "Douala", "Garoua-Boulaï", "Batouri"],
                "quarters": [
                    "Biteng", "Douala 3", "Makélé", "New Bell", 
                    "PK 18", "PK 20", "PK 23", "PK 25"
                ]
            },
            "Far North Region": {
                "towns": ["Maroua", "Mokolo", "Kousséri", "Yele"],
                "quarters": [
                    "Doumana", "Far Far", "Grand Mosque", "Sabon Gari", 
                    "Tinsou", "Djoum", "Ngaoundéré-Ville", "N'Kongsamba-Ville"
                ]
            },
            "Littoral Region": {
                "towns": ["Douala", "Limbé", "Kribi", "Edéa"],
                "quarters": [
                    "Akwa", "Bonanjo", "Deido", "New Bell", 
                    "PK 18", "PK 20", "PK 23", "PK 25"
                ]
            },
            "North Region": {
                "towns": ["Garoua", "Guider", "Ngaoundéré", "Yako"],
                "quarters": [
                    "Doumana", "Far Far", "Grand Mosque", "Sabon Gari", 
                    "Tinsou", "Djoum", "Ngaoundéré-Ville", "N'Kongsamba-Ville"
                ]
            },
            "Northwest Region": {
                "towns": ["Bamenda", "Batibo", "Bambui", "Ndu"],
                "quarters": [
                    "Bambili", "Mankon", "Mile 3", "Old Town", 
                    "West End", "N'Kongsamba-Ville", "N'Koutou", "N'Koung"
                ]
            },
            "South Region": {
                "towns": ["Ebolowa", "Kribi", "Djembé", "Campo"],
                "quarters": [
                    "Awaé", "M'Ebolowa", "M'Eton", "N'Doung", 
                    "N'Kongsamba", "N'Koutou", "N'Koung", "N'Kongsamba-Ville"
                ]
            },
            "Southwest Region": {
                "towns": ["Buea", "Kumba", "Limbé", "Tiko"],
                "quarters": [
                    "Bonduma", "Great Soppo", "Mile 4", "Molyko", 
                    "Small Soppo", "N'Kongsamba-Ville", "N'Koutou", "N'Koung"
                ]
            },
            "West Region": {
                "towns": ["Bafoussam", "Bandjoun", "Menoua", "Dschang"],
                "quarters": [
                    "Commercial Avenue", "Ndoungue", "N'Kongsamba", 
                    "Old Town", "Sabon Gari", "N'Kongsamba-Ville", 
                    "N'Koutou", "N'Koung"
                ]
            }
        }

        # Insert data into the database
        for region_name, info in data.items():
            region, created = Region.objects.get_or_create(name=region_name)
            for town_name in info["towns"]:
                town, created = Town.objects.get_or_create(name=town_name, region=region)
                for quarter_name in info["quarters"]:
                    Quarter.objects.get_or_create(name=quarter_name, town=town)

        self.stdout.write(self.style.SUCCESS("Data inserted successfully!"))